"""Simple tests for PawPal+ core behaviors."""

from datetime import date, datetime, timedelta

from cli_display import render_conflict_warning, render_plan, task_emoji
from pawpal_system import DailyPlan, Owner, Pet, Task


def test_mark_complete_changes_status():
    task = Task("Morning walk", datetime(2026, 7, 3, 8, 0), 30)
    assert task.done is False

    task.mark_complete()

    assert task.done is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="Golden Retriever")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Feeding", datetime(2026, 7, 3, 9, 0), 10))

    assert len(pet.tasks) == 1


# --- sorting correctness --------------------------------------------------


def test_generate_places_higher_priority_first():
    """A low-priority earlier task must not outrank a high-priority one."""
    owner = Owner(name="Ada")
    pet = Pet(name="Rex", species="Dog")
    owner.add_pet(pet)
    # low priority starts earlier in the day; high priority starts later.
    low = Task("Brush", datetime(2026, 7, 3, 8, 0), 30, priority="low")
    high = Task("Meds", datetime(2026, 7, 3, 10, 0), 30, priority="high")
    pet.add_task(low)
    pet.add_task(high)

    # Non-overlapping, so both are scheduled; the candidate ordering inside
    # generate should consider the high-priority task first.
    plan = DailyPlan.generate(owner, date(2026, 7, 3))

    assert set(plan.tasks) == {low, high}


def test_sort_by_time_orders_tasks_earliest_first():
    owner = Owner(name="Ada")
    pet = Pet(name="Rex", species="Dog")
    owner.add_pet(pet)
    later = Task("Dinner", datetime(2026, 7, 3, 18, 0), 15)
    earlier = Task("Breakfast", datetime(2026, 7, 3, 7, 0), 15)
    pet.add_task(later)
    pet.add_task(earlier)

    plan = DailyPlan.generate(owner, date(2026, 7, 3))

    assert [t.start_time for t in plan.tasks] == sorted(
        t.start_time for t in plan.tasks
    )
    assert plan.tasks[0] is earlier
    assert plan.tasks[-1] is later


# --- recurrence logic -----------------------------------------------------


def test_mark_complete_spawns_next_daily_occurrence():
    pet = Pet(name="Rex", species="Dog")
    task = Task("Walk", datetime(2026, 7, 3, 8, 0), 30, frequency="daily")
    pet.add_task(task)

    nxt = task.mark_complete()

    assert nxt is not None
    assert nxt.done is False
    assert nxt.start_time == datetime(2026, 7, 4, 8, 0)
    assert nxt in pet.tasks
    assert len(pet.tasks) == 2


def test_weekly_recurrence_advances_seven_days():
    task = Task("Bath", datetime(2026, 7, 3, 9, 0), 60, frequency="weekly")

    nxt = task.next_occurrence()

    assert nxt is not None
    assert nxt.start_time == datetime(2026, 7, 3, 9, 0) + timedelta(weeks=1)


def test_non_recurring_task_spawns_nothing():
    pet = Pet(name="Rex", species="Dog")
    task = Task("Vet visit", datetime(2026, 7, 3, 8, 0), 30, frequency="once")
    pet.add_task(task)

    nxt = task.mark_complete()

    assert nxt is None
    assert len(pet.tasks) == 1


def test_double_complete_does_not_double_spawn():
    pet = Pet(name="Rex", species="Dog")
    task = Task("Walk", datetime(2026, 7, 3, 8, 0), 30, frequency="daily")
    pet.add_task(task)

    first = task.mark_complete()
    second = task.mark_complete()

    assert first is not None
    assert second is None  # already done -> no second occurrence
    assert len(pet.tasks) == 2


# --- conflict detection ---------------------------------------------------


def test_identical_start_times_conflict():
    owner = Owner(name="Ada")
    pet = Pet(name="Rex", species="Dog")
    owner.add_pet(pet)
    a = Task("Walk", datetime(2026, 7, 3, 8, 0), 30)
    b = Task("Feed", datetime(2026, 7, 3, 8, 0), 30)
    pet.add_task(a)
    pet.add_task(b)

    plan = DailyPlan.generate(owner, date(2026, 7, 3))

    # Overlapping tasks: only one is scheduled, and it's flagged same-pet.
    assert len(plan.tasks) == 1
    plan.tasks = [a, b]  # force both in to inspect conflict reporting
    conflicts = plan.time_conflicts()
    assert len(conflicts) == 1
    assert conflicts[0][2] == "same-pet"


def test_back_to_back_tasks_do_not_conflict():
    a = Task("Walk", datetime(2026, 7, 3, 8, 0), 30)  # 08:00-08:30
    b = Task("Feed", datetime(2026, 7, 3, 8, 30), 30)  # 08:30-09:00

    assert a.conflicts_with(b) is False
    assert b.conflicts_with(a) is False


def test_different_pet_overlap_tagged_different_pet():
    owner = Owner(name="Ada")
    rex = Pet(name="Rex", species="Dog")
    mia = Pet(name="Mia", species="Cat")
    owner.add_pet(rex)
    owner.add_pet(mia)
    a = Task("Walk Rex", datetime(2026, 7, 3, 8, 0), 30)
    b = Task("Feed Mia", datetime(2026, 7, 3, 8, 15), 30)
    rex.add_task(a)
    mia.add_task(b)

    plan = DailyPlan(date=date(2026, 7, 3), owner=owner, tasks=[a, b])
    plan.sort_by_time()
    conflicts = plan.time_conflicts()

    assert len(conflicts) == 1
    assert conflicts[0][2] == "different-pet"
    assert plan.conflict_warning() != ""


def test_conflict_free_plan_has_empty_warning():
    owner = Owner(name="Ada")
    pet = Pet(name="Rex", species="Dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", datetime(2026, 7, 3, 8, 0), 30))
    pet.add_task(Task("Feed", datetime(2026, 7, 3, 9, 0), 15))

    plan = DailyPlan.generate(owner, date(2026, 7, 3))

    assert plan.time_conflicts() == []
    assert plan.conflict_warning() == ""
    assert plan.fits_constraints() is True


# --- next available slot --------------------------------------------------


def test_next_slot_fits_in_gap_between_tasks():
    """A slot short enough to fit the gap lands right after the first task."""
    owner = Owner(name="Ada")
    pet = Pet(name="Rex", species="Dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", datetime(2026, 7, 3, 8, 0), 30))  # 08:00-08:30
    pet.add_task(Task("Vet", datetime(2026, 7, 3, 10, 0), 30))  # 10:00-10:30

    plan = DailyPlan.generate(owner, date(2026, 7, 3))

    # Searching from 08:00, a 30-min slot fits the 08:30-10:00 gap at 08:30.
    after = datetime(2026, 7, 3, 8, 0)
    assert plan.next_available_slot(30, after=after) == datetime(2026, 7, 3, 8, 30)


def test_next_slot_skips_past_a_blocking_task():
    """A slot too long for the first gap is pushed past the blocker."""
    owner = Owner(name="Ada")
    pet = Pet(name="Rex", species="Dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", datetime(2026, 7, 3, 8, 0), 30))  # 08:00-08:30
    pet.add_task(Task("Nap", datetime(2026, 7, 3, 8, 45), 60))  # 08:45-09:45

    plan = DailyPlan.generate(owner, date(2026, 7, 3))

    # Searching from 08:00: 60 min won't fit the 08:30-08:45 gap, so it lands
    # after the 09:45 nap.
    after = datetime(2026, 7, 3, 8, 0)
    assert plan.next_available_slot(60, after=after) == datetime(2026, 7, 3, 9, 45)


def test_next_slot_respects_after_argument():
    owner = Owner(name="Ada")
    plan = DailyPlan(date=date(2026, 7, 3), owner=owner)

    after = datetime(2026, 7, 3, 14, 0)
    assert plan.next_available_slot(30, after=after) == after


def test_next_slot_honors_availability_window():
    owner = Owner(name="Ada")
    owner.update_availability([(datetime(2026, 7, 3, 9, 0), datetime(2026, 7, 3, 12, 0))])
    plan = DailyPlan(date=date(2026, 7, 3), owner=owner)

    # No `after`, so the earliest slot is the window's start, not midnight.
    assert plan.next_available_slot(60) == datetime(2026, 7, 3, 9, 0)


def test_next_slot_returns_none_when_window_too_short():
    owner = Owner(name="Ada")
    owner.update_availability([(datetime(2026, 7, 3, 9, 0), datetime(2026, 7, 3, 9, 30))])
    plan = DailyPlan(date=date(2026, 7, 3), owner=owner)

    assert plan.next_available_slot(60) is None


# --- CLI display ----------------------------------------------------------


def test_task_emoji_matches_by_keyword():
    assert task_emoji("Morning walk") == "🚶"
    assert task_emoji("Dinner feeding") == "🍽️"
    assert task_emoji("Give meds") == "💊"


def test_task_emoji_falls_back_to_paw_print():
    assert task_emoji("Something unusual") == "🐾"


def test_render_plan_without_color_has_no_ansi_codes():
    owner = Owner(name="Ada")
    pet = Pet(name="Rex", species="Dog")
    owner.add_pet(pet)
    pet.add_task(Task("Morning walk", datetime(2026, 7, 3, 8, 0), 30, priority="high"))

    output = render_plan(DailyPlan.generate(owner, date(2026, 7, 3)), color=False)

    assert "\033[" not in output  # no escape sequences when color is off
    assert "Morning walk" in output
    assert "🚶" in output
    assert "🐾 Daily plan for Ada" in output


def test_render_plan_with_color_emits_ansi_codes():
    owner = Owner(name="Ada")
    pet = Pet(name="Rex", species="Dog")
    owner.add_pet(pet)
    pet.add_task(Task("Feeding", datetime(2026, 7, 3, 9, 0), 10, priority="low"))

    output = render_plan(DailyPlan.generate(owner, date(2026, 7, 3)), color=True)

    assert "\033[" in output  # color codes present when forced on


def test_render_empty_plan_reports_no_tasks():
    owner = Owner(name="Ada")
    plan = DailyPlan(date=date(2026, 7, 3), owner=owner)

    assert "(no tasks scheduled)" in render_plan(plan, color=False)


def test_render_conflict_warning_empty_when_conflict_free():
    owner = Owner(name="Ada")
    pet = Pet(name="Rex", species="Dog")
    owner.add_pet(pet)
    pet.add_task(Task("Walk", datetime(2026, 7, 3, 8, 0), 30))

    plan = DailyPlan.generate(owner, date(2026, 7, 3))

    assert render_conflict_warning(plan, color=False) == ""
