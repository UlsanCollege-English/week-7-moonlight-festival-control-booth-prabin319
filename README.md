# Week 7 Homework: Moonlight Festival Control Booth

## Summary

This homework uses Python's `heapq` module to manage festival alerts by priority.
The control booth receives alerts with different urgency levels and must handle
the most critical ones first. I implemented four functions: basic priority ordering,
stable ordering for ties, top-k selection, and a non-destructive peek. Each
function uses a min-heap so the most urgent alert is always retrieved efficiently.

---

## Approach

### `order_festival_alerts`

* I pushed each `(priority, title)` tuple into a min-heap using `heapq.heappush`.
* Each heap item looked like `(priority, title)` — Python compares tuples left to right, so the smallest priority number rises to the top automatically.
* I popped items one by one with `heapq.heappop` and appended each title to the result list, which gives them in priority order.

### `order_festival_alerts_stable`

* I stored `(priority, index, title)` in the heap instead of just `(priority, title)`.
* When two alerts share the same priority, Python compares the second element — the arrival index — which is always unique and preserves input order automatically.
* Input order mattered because the spec requires earlier-arriving alerts to be handled first among ties.

### `top_k_festival_alerts`

* I used `heapq.nsmallest(k, indexed)` where `indexed` is a list of `(priority, index, title)` tuples. `nsmallest` keeps a heap of size k while scanning all n alerts, returning the k smallest efficiently.
* If `k <= 0` I return `[]` immediately. If `k >= len(alerts)`, `nsmallest` naturally returns everything — no special case needed.
* The `index` field ensures stable ordering for ties, matching the expected output exactly.

### `peek_next_festival_alert`

* I made a shallow copy of the input list with `list(alerts)` so the original is never touched.
* I called `heapq.heapify` on the copy to rearrange it into a valid min-heap in O(n).
* In a min-heap, `heap[0]` is always the smallest element, so I read it directly without popping — the original list stays unchanged.

---

## Complexity

### `order_festival_alerts`

* **Time:** O(n log n) — each of the n `heappush` and `heappop` calls costs O(log n).
* **Space:** O(n) — the heap holds all n alerts at once.
* **Why:** Every alert must enter and leave the heap once, and each operation rebalances in O(log n).

### `order_festival_alerts_stable`

* **Time:** O(n log n) — same as above; adding the index field does not change the asymptotic cost.
* **Space:** O(n) — the heap holds all n `(priority, index, title)` tuples.
* **Why:** The index is just an integer added to each tuple; it does not add extra iterations or memory beyond the n items already stored.

### `top_k_festival_alerts`

* **Time:** O(n log k) — `heapq.nsmallest` scans all n alerts but only maintains an internal heap of size k, so each comparison costs O(log k).
* **Space:** O(k) — only k items are kept in the heap at any time.
* **Why:** This is more efficient than pushing all n items when k is much smaller than n.

### `peek_next_festival_alert`

* **Time:** O(n) — `heapq.heapify` rearranges n items in linear time; reading `heap[0]` is O(1).
* **Space:** O(n) — a full copy of the input list is made to avoid modifying the original.
* **Why:** Heapify is O(n) rather than O(n log n) because it uses a bottom-up sifting algorithm. The copy is necessary to satisfy the no-mutation requirement.

---

## Edge-case checklist

### `order_festival_alerts`

* [x] empty input
* [x] one alert
* [x] multiple different priorities

### `order_festival_alerts_stable`

* [x] same-priority tie
* [x] all same priority
* [x] empty input

### `top_k_festival_alerts`

* [x] `k = 0`
* [x] `k > len(alerts)`
* [x] duplicate priorities
* [x] empty input

### `peek_next_festival_alert`

* [x] empty input
* [x] normal case

---

## Test notes

* Stable ordering for ties was verified by checking that alerts with the same priority appear in their original input order, not just that the right set of titles is present.
* `peek_next_festival_alert` has a dedicated test that calls the function and then checks that the original list is byte-for-byte identical to a copy made before the call.
* `top_k_festival_alerts` with `k > len(alerts)` was tested to confirm it returns all alerts in priority order rather than raising an error.

---

## Assistance & Sources

### AI used?

* [ ] No
* [x] Yes

If yes, what did it help with?

Claude helped explain how tuple comparison works in Python heaps, suggested using `(priority, index, title)` to handle tie-breaking, and reviewed the complexity analysis for correctness.

### Other sources

* Python docs: https://docs.python.org/3/library/heapq.html
* Course cheat sheet (Week 7)

---

## Reflection

What was hardest?

* Understanding why `heapq.nsmallest` with duplicate priorities could return items in a different order than expected, and realising I needed to add an index to guarantee stability in `top_k_festival_alerts` too — not just in the stable version.

What do you understand better now?

* How Python compares tuples element by element, and how that behaviour can be used deliberately to control heap ordering without writing any custom comparison logic.