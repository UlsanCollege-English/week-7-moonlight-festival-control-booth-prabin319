"""
Week 7: Moonlight Festival Control Booth

Use Python's heapq module to solve priority queue problems.
"""

from __future__ import annotations

import heapq


def order_festival_alerts(alerts: list[tuple[int, str]]) -> list[str]:
    """
    Return alert titles in the order they should be handled.

    Each alert is a tuple:
        (priority, title)

    Smaller priority numbers should be handled first.

    Time:  O(n log n) — each heappush and heappop is O(log n)
    Space: O(n) — heap stores all n alerts
    """
    heap = []
    for priority, title in alerts:
        heapq.heappush(heap, (priority, title))

    result = []
    while heap:
        priority, title = heapq.heappop(heap)
        result.append(title)

    return result


def order_festival_alerts_stable(alerts: list[tuple[int, str]]) -> list[str]:
    """
    Return alert titles in the order they should be handled.

    If two alerts have the same priority, keep the original input order
    (stable — first in, first out among ties).

    We store (priority, index, title) so that when priorities are equal,
    Python compares index next, which breaks the tie by arrival order.

    Time:  O(n log n)
    Space: O(n)
    """
    heap = []
    for index, (priority, title) in enumerate(alerts):
        heapq.heappush(heap, (priority, index, title))

    result = []
    while heap:
        priority, index, title = heapq.heappop(heap)
        result.append(title)

    return result


def top_k_festival_alerts(alerts: list[tuple[int, str]], k: int) -> list[str]:
    """
    Return the titles of the k most urgent alerts, from most to less urgent.

    If k <= 0, return [].
    If k >= len(alerts), return all alerts in priority order.

    We use (priority, index, title) to guarantee stable ordering for ties.

    Time:  O(n log k) — heapq.nsmallest keeps a heap of size k
    Space: O(k)
    """
    if k <= 0:
        return []

    indexed = [(priority, i, title) for i, (priority, title) in enumerate(alerts)]
    top = heapq.nsmallest(k, indexed)
    return [title for priority, i, title in top]


def peek_next_festival_alert(alerts: list[tuple[int, str]]) -> str | None:
    """
    Return the title of the next alert to handle without permanently
    changing the original input.

    If alerts is empty, return None.

    We make a copy of the list before heapifying so the original is untouched.

    Time:  O(n) — heapify is O(n)
    Space: O(n) — copy of the input
    """
    if not alerts:
        return None

    heap = list(alerts)       # shallow copy — original is safe
    heapq.heapify(heap)       # rearrange copy into a heap in O(n)
    priority, title = heap[0] # heap[0] is always the smallest element
    return title