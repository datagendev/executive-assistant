#!/usr/bin/env python3
"""Test calling MCP tools from Python code using DataGen SDK"""

from datagen_sdk import DatagenClient
from concurrent.futures import ThreadPoolExecutor
import time

def main():
    # Initialize client (uses DATAGEN_API_KEY from environment)
    client = DatagenClient()

    # Example 1: Sequential calls
    print("=" * 60)
    print("SEQUENTIAL EXECUTION")
    print("=" * 60)

    start = time.time()

    print("\n📅 Getting current time from Google Calendar...")
    time_result = client.execute_tool("composio_GOOGLECALENDAR_GET_CURRENT_DATE_TIME")
    print(f"   Current time: {time_result['current_datetime']}")

    print("\n📅 Getting calendar info...")
    # Note: This might fail if no calendar_id specified, but demonstrates the API
    try:
        calendar_result = client.execute_tool("composio_GOOGLECALENDAR_CALENDAR_LIST_LIST")
        print(f"   Found {len(calendar_result.get('items', []))} calendars")
    except Exception as e:
        print(f"   Calendar list: {str(e)[:100]}...")

    sequential_time = time.time() - start
    print(f"\n⏱️  Sequential execution: {sequential_time:.2f}s")

    # Example 2: Parallel calls using ThreadPoolExecutor
    print("\n" + "=" * 60)
    print("PARALLEL EXECUTION")
    print("=" * 60)

    start = time.time()

    def call_tool(tool_name, params=None):
        return client.execute_tool(tool_name, params or {})

    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit parallel calls
        futures = {
            'time': executor.submit(call_tool, "composio_GOOGLECALENDAR_GET_CURRENT_DATE_TIME"),
            'calendar': executor.submit(call_tool, "composio_GOOGLECALENDAR_CALENDAR_LIST_LIST"),
        }

        # Collect results
        for name, future in futures.items():
            try:
                result = future.result()
                print(f"\n✅ {name}: Success")
            except Exception as e:
                print(f"\n❌ {name}: {str(e)[:100]}...")

    parallel_time = time.time() - start
    print(f"\n⏱️  Parallel execution: {parallel_time:.2f}s")
    print(f"🚀 Speedup: {sequential_time/parallel_time:.2f}x faster")

    print("\n" + "=" * 60)
    print("✅ MCP tools work great inside Python code!")
    print("=" * 60)

if __name__ == "__main__":
    main()
