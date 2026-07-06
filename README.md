# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule
Daily plan for Sam — 2026-07-03
  [ ] 08:00 — Morning walk for Biscuit (30 min) [priority: high]
  [ ] 09:00 — Feeding for Mittens (10 min) [priority: high]
  [ ] 18:00 — Dinner for Biscuit (15 min) [priority: medium]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
================================================= test session starts ==================================================
platform darwin -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/shaylacary/ai110/projects/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 12 items                                                                                                     

tests/test_pawpal.py ............                                                                                [100%]

================================================== 12 passed in 0.02s ==================================================
5 Stars
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `DailyPlan.generate`, `DailyPlan.sort_by_time` | By priority, then by start time. |
| Filtering | `Owner.filter_tasks` | By completion status and/or pet name. |
| Conflict handling | `DailyPlan.time_conflicts`, `DailyPlan.conflict_warning` | Flags overlapping tasks as same- or different-pet; warns instead of crashing. |
| Recurring tasks | `Task.mark_complete`, `Task.next_occurrence` | Daily/weekly tasks spawn the next occurrence when completed. |

## 🎨 Output Formatting

Terminal output is rendered by `cli_display.py` (kept separate from the domain model):

- **Table** — `render_plan` lays the plan out as a bordered table using [`tabulate`](https://pypi.org/project/tabulate/).
- **Emojis** — `task_emoji` picks an emoji by task type (🚶 walk, 🍽️ feed, 💊 meds…).
- **Color** — priority (🔴/🟡/🟢) and status (✅/⏳) are ANSI-colored; auto-disabled when output isn't a terminal.

`tabulate` is the only added dependency; everything else uses the standard library.

## 📸 Demo Walkthrough

**Features:** Sorting by time · Priority ordering · Conflict warnings · Filtering by pet/status · Daily & weekly recurrence

Follow along in the app (`app.py`):

1. **Start with the seeded owner and pets** — owner *Sam* with *Biscuit* (Golden Retriever) and *Mittens* (Cat).
2. **View pets and tasks** in a table, and filter by pet or status (All / To do / Done).
3. **Click "Generate schedule"** to build today's plan.
4. **See the plan sorted by time** — tasks entered out of order come out chronologically, high priority first.
5. **Read the conflict warning** — the overlapping 08:00 walk and feeding are flagged as a *different-pet* conflict instead of crashing.

Sample CLI output (`python main.py`):

```
Today's Schedule
Daily plan for Sam — 2026-07-05
  [ ] 08:00 — Morning walk for Biscuit (30 min) [priority: high]
  [ ] 08:00 — Feeding for Mittens (10 min) [priority: high]
  [ ] 18:00 — Dinner for Biscuit (15 min) [priority: medium]
⚠️  1 scheduling conflict(s) detected:
  • 08:00 Morning walk (Biscuit) overlaps 08:00 Feeding (Mittens) — different pets
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
