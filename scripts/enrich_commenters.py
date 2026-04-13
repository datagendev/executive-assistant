"""Enrich LinkedIn commenters concurrently with durable checkpointing.

Usage:
    python scripts/enrich_commenters.py tmp/commenter_slugs.json

Reads a JSON array of {slug, name, headline} objects.
Fetches each profile via get_linkedin_person_data, saving progress
to a checkpoint file after every batch. Safe to interrupt and resume.

Rate limit: 60 requests per minute (1/sec), with up to 5 concurrent workers.
"""
import os
import sys
import json
import time
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from datagen_sdk import DatagenClient

# --- Config ---
MAX_WORKERS = 3
RATE_LIMIT_RPM = 50  # stay under 60 rpm API limit
RETRY_ATTEMPTS = 2
RETRY_DELAY = 3


class RateLimiter:
    """Token bucket rate limiter. Call acquire() before each request."""

    def __init__(self, rpm):
        self.interval = 60.0 / rpm  # seconds between requests
        self.lock = threading.Lock()
        self.last_time = 0.0

    def acquire(self):
        with self.lock:
            now = time.time()
            wait = self.last_time + self.interval - now
            if wait > 0:
                time.sleep(wait)
            self.last_time = time.time()


def load_checkpoint(path):
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def save_checkpoint(path, data, lock):
    with lock:
        with open(path, "w") as f:
            json.dump(data, f)


def fetch_profile(slug, rate_limiter):
    """Fetch a single LinkedIn profile. Returns (slug, profile_dict)."""
    client = DatagenClient()
    for attempt in range(RETRY_ATTEMPTS):
        rate_limiter.acquire()
        try:
            result = client.execute_tool("get_linkedin_person_data", {
                "linkedin_url": f"https://linkedin.com/in/{slug}",
            })
            if isinstance(result, dict):
                return slug, result
            return slug, {"raw": result}
        except Exception as e:
            if attempt < RETRY_ATTEMPTS - 1:
                time.sleep(RETRY_DELAY)
            else:
                return slug, {"error": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/enrich_commenters.py <commenter_slugs.json>")
        sys.exit(1)

    input_path = sys.argv[1]
    with open(input_path) as f:
        commenters = json.load(f)

    total = len(commenters)
    print(f"Loaded {total} commenters from {input_path}")
    print(f"Rate limit: {RATE_LIMIT_RPM} rpm, {MAX_WORKERS} workers")

    # Checkpoint lives next to input file
    base = os.path.splitext(input_path)[0]
    checkpoint_path = f"{base}_checkpoint.json"
    output_path = f"{base}_enriched.json"

    # Load existing progress
    checkpoint = load_checkpoint(checkpoint_path)
    already_done = set(checkpoint.keys())
    remaining = [c for c in commenters if c["slug"] not in already_done]

    print(f"Checkpoint: {len(already_done)}/{total} done, {len(remaining)} remaining")
    if remaining:
        est_min = len(remaining) / RATE_LIMIT_RPM
        print(f"Estimated time: ~{est_min:.1f} min")

    if not remaining:
        print("All profiles already enriched. Writing output.")
        write_output(commenters, checkpoint, output_path)
        return

    lock = threading.Lock()
    rate_limiter = RateLimiter(RATE_LIMIT_RPM)
    completed = len(already_done)
    failed = 0
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {
            pool.submit(fetch_profile, c["slug"], rate_limiter): c
            for c in remaining
        }

        for future in as_completed(futures):
            slug, result = future.result()
            completed += 1

            if result and "error" not in result:
                checkpoint[slug] = result
                elapsed = time.time() - start_time
                rate = (completed - len(already_done)) / elapsed if elapsed > 0 else 0
                eta = (total - completed) / rate if rate > 0 else 0
                print(f"  [{completed}/{total}] {slug} OK ({rate:.1f}/s, ~{eta:.0f}s left)")
            else:
                failed += 1
                err = result.get("error", "unknown") if result else "no response"
                checkpoint[slug] = {"error": err}
                print(f"  [{completed}/{total}] {slug} FAILED: {err}")

            # Save checkpoint every 10 profiles
            if (completed - len(already_done)) % 10 == 0:
                save_checkpoint(checkpoint_path, checkpoint, lock)

    # Final checkpoint save
    save_checkpoint(checkpoint_path, checkpoint, lock)

    elapsed = time.time() - start_time
    enriched = completed - len(already_done)
    print(f"\nDone: {enriched} profiles in {elapsed:.1f}s ({enriched/elapsed:.1f}/s)")
    print(f"Total: {completed}/{total} enriched, {failed} failed")
    print(f"Checkpoint: {checkpoint_path}")

    write_output(commenters, checkpoint, output_path)


def write_output(commenters, checkpoint, output_path):
    """Merge commenter list with enriched profiles and write output."""
    results = []
    for c in commenters:
        slug = c["slug"]
        profile = checkpoint.get(slug, {})
        entry = {
            "slug": slug,
            "name": c.get("name", ""),
            "linkedin_url": f"https://linkedin.com/in/{slug}",
        }
        if "error" in profile:
            entry["enrichment_error"] = profile["error"]
        else:
            # Profile data may be nested under "person"
            p = profile.get("person", profile)
            for key in ("headline", "summary", "location", "followersCount",
                        "firstName", "lastName", "skills", "languages"):
                if key in p:
                    entry[key] = p[key]
            # Flatten current position
            cur = p.get("currentPosition", {})
            if cur:
                entry["title"] = cur.get("title", "")
                entry["company"] = cur.get("companyName", "")
            # Flatten experience to list of {title, company, dates}
            if "experience" in p:
                entry["experience"] = [
                    {"title": e.get("title", ""), "company": e.get("companyName", ""),
                     "start": (e.get("startEndDate") or {}).get("start", ""),
                     "end": (e.get("startEndDate") or {}).get("end", "")}
                    for e in p["experience"][:5]
                ]
        results.append(entry)

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    ok = sum(1 for r in results if "enrichment_error" not in r and len(r) > 3)
    print(f"Output: {output_path} ({ok} enriched, {len(results) - ok} missing)")


if __name__ == "__main__":
    main()
