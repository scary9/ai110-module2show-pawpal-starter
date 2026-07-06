# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to implement an algorithmic capability — a "next available slot"
feature — for the PawPal+ scheduling system.

**What did the agent do?**

- Read `pawpal_system.py`, `main.py`, and `tests/test_pawpal.py` first to learn the
  existing design and conventions.
- Added a `next_available_slot(duration_minutes, after=None)` method to the
  `DailyPlan` class in `pawpal_system.py`. It returns the earliest datetime where a
  task of the requested length fits, respecting both the owner's availability windows
  and the tasks already scheduled in the plan. The algorithm sweeps each availability
  window once, advancing a cursor past any blocking task until a gap large enough
  opens, and returns `None` if nothing fits.
- Added 5 tests to `tests/test_pawpal.py` covering: filling a gap between tasks,
  skipping past a too-large blocker, honoring the `after` argument, honoring an
  availability window, and returning `None` when the window is too short.
- Ran the full test suite (`python3 -m pytest tests/`) and a manual end-to-end demo
  script to confirm the feature behaves correctly.

**Files modified:**

- `pawpal_system.py` — added the `next_available_slot` method to `DailyPlan`.
- `tests/test_pawpal.py` — added 5 tests for the new feature.

**What did you have to verify or fix manually?**

- On the first test run, 2 of the new tests failed. The failures exposed that my
  *test expectations* were wrong, not the code: with no `after` argument the search
  starts at midnight, and the whole morning before the first task is free, so the
  method correctly returned 00:00 instead of a gap between tasks. The agent corrected
  the tests to pass an explicit `after` time so the gap-filling logic was actually
  exercised, then re-ran the suite — all 17 tests passed.
- The agent flagged a design decision for review: with no `after` given, "next slot"
  defaults to searching from midnight, which can land in the early-morning hours. It
  noted this could instead start from the owner's `preferred_time` or a work-day start
  if preferred.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
