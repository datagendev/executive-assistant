#!/usr/bin/env python3
"""Smoke test for RateLimiter class."""
import time
import threading

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


def test_rate_limiter():
    """Test that rate limiter enforces correct timing."""
    print("Testing RateLimiter with 50 RPM (1.2s interval)...")

    limiter = RateLimiter(50)
    times = []

    # Make 5 requests
    for i in range(5):
        start = time.time()
        limiter.acquire()
        times.append(time.time())
        print(f"  Request {i+1}: {time.time():.3f}")

    # Check intervals
    print("\nInterval analysis:")
    for i in range(1, len(times)):
        interval = times[i] - times[i-1]
        expected = 1.2  # 60/50 = 1.2 seconds
        print(f"  Request {i} -> {i+1}: {interval:.3f}s (expected ~{expected:.1f}s)")

        # Allow 50ms tolerance for timing jitter
        if abs(interval - expected) > 0.05:
            print(f"    ⚠️  WARNING: Interval off by {abs(interval - expected):.3f}s")
        else:
            print(f"    ✓ OK")

    total_time = times[-1] - times[0]
    expected_total = 4 * 1.2  # 4 intervals between 5 requests
    print(f"\nTotal time: {total_time:.2f}s (expected ~{expected_total:.1f}s)")

    if abs(total_time - expected_total) < 0.2:
        print("✅ Rate limiter is working correctly")
        return True
    else:
        print(f"❌ Rate limiter failed: off by {abs(total_time - expected_total):.2f}s")
        return False


def test_concurrent():
    """Test that rate limiter is thread-safe."""
    print("\nTesting thread safety with 3 concurrent workers...")

    limiter = RateLimiter(50)
    times = []
    lock = threading.Lock()

    def worker(worker_id):
        for i in range(2):
            limiter.acquire()
            with lock:
                t = time.time()
                times.append(t)
                print(f"  Worker {worker_id} request {i+1}: {t:.3f}")

    start = time.time()
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # 6 total requests with 3 workers should take ~6s (5 intervals at 1.2s each)
    total_time = time.time() - start
    expected = 5 * 1.2  # 5 intervals
    print(f"\nConcurrent test: {total_time:.2f}s (expected ~{expected:.1f}s)")

    # Check that intervals are respected globally
    times.sort()
    violations = 0
    for i in range(1, len(times)):
        interval = times[i] - times[i-1]
        if interval < 1.15:  # Allow small tolerance
            violations += 1

    if violations == 0:
        print("✅ Thread-safe: all intervals respected")
        return True
    else:
        print(f"❌ Thread-safety failed: {violations} intervals too short")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("RATE LIMITER SMOKE TEST")
    print("=" * 60)

    result1 = test_rate_limiter()
    result2 = test_concurrent()

    print("\n" + "=" * 60)
    if result1 and result2:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 60)
