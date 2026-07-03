"""PawPal+ core implementation.

Four classes model the domain:
- Task     : a single care activity for a pet (description, time, frequency,
             completion status).
- Pet      : the animal's details plus the tasks it needs.
- Owner    : manages multiple pets and is the single access point to all of
             their tasks; owns the scheduling constraints (availability,
             preferences).
- DailyPlan: pulls the owner's tasks and arranges them into a conflict-free,
             availability-respecting schedule for one day, and displays it.

Design notes:
- Owner and Pet use identity equality (eq=False): two same-named pets are
  still distinct, and instances stay hashable.
- Task also uses identity equality so remove_task removes the exact object,
  and its back-reference to its pet is excluded from repr to avoid the
  Pet<->Task print cycle.
- DailyPlan reaches tasks only through Owner.all_tasks() (Law of Demeter),
  never by walking pets directly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

# Priority levels, ordered most-urgent first. Used to sort tasks when building
# a plan (lower rank number = scheduled earlier when there's competition).
PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


@dataclass(eq=False)
class Task:
    """A single care activity for a pet.

    priority : "high", "medium", or "low".
    frequency: recurrence label, e.g. "daily" or "weekly".
    done     : completion status.
    """

    description: str
    start_time: datetime
    duration_minutes: int
    frequency: str = "daily"
    priority: str = "medium"
    done: bool = False
    # Back-reference set when the task is attached to a pet. Excluded from
    # repr to avoid infinite recursion with Pet.tasks.
    pet: "Pet | None" = field(default=None, repr=False)

    @property
    def end_time(self) -> datetime:
        """When the activity finishes -- keeps conflict checks simple."""
        return self.start_time + timedelta(minutes=self.duration_minutes)

    def conflicts_with(self, other: "Task") -> bool:
        """True if this task's time window overlaps another's."""
        return self.start_time < other.end_time and other.start_time < self.end_time

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.done = True

    def mark_incomplete(self) -> None:
        """Mark this task as not done."""
        self.done = False


@dataclass(eq=False)
class Pet:
    """A pet's details and the tasks it needs.

    priority: "high", "medium", or "low" (used to break ties between pets).
    """

    name: str
    species: str
    priority: str = "medium"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task, wiring its back-reference to this pet."""
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Detach a task from this pet."""
        self.tasks.remove(task)
        task.pet = None

    def get_tasks(self) -> list[Task]:
        """A copy of this pet's tasks (callers can't mutate the list)."""
        return list(self.tasks)

    def update_priority(self, level: str) -> None:
        """Set this pet's priority ("high", "medium", or "low")."""
        self.priority = level


@dataclass(eq=False)
class Owner:
    """The pet owner: manages pets and exposes all their tasks.

    availability: (start, end) datetime windows the owner is free.
    """

    name: str
    preferred_time: datetime | None = None
    preferences: list[str] = field(default_factory=list)
    availability: list[tuple[datetime, datetime]] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's care."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's care."""
        self.pets.remove(pet)

    def update_availability(self, slots: list[tuple[datetime, datetime]]) -> None:
        """Replace the owner's free-time windows."""
        self.availability = list(slots)

    def update_preferences(self, prefs: list[str]) -> None:
        """Replace the owner's care preferences."""
        self.preferences = list(prefs)

    def all_tasks(self) -> list[Task]:
        """Single access point: flatten every task across all pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class DailyPlan:
    """A conflict-free daily schedule built from the owner's tasks."""

    date: date
    owner: Owner
    tasks: list[Task] = field(default_factory=list)

    @property
    def pets(self) -> set[Pet]:
        """Pets appearing in the plan -- derived from the scheduled tasks."""
        return {task.pet for task in self.tasks if task.pet is not None}

    @classmethod
    def generate(cls, owner: Owner, day: date) -> "DailyPlan":
        """Build a plan: pull the owner's tasks, then greedily place the
        highest-priority ones that fit the owner's availability without
        overlapping already-placed tasks.
        """
        plan = cls(date=day, owner=owner)
        # Higher priority first; tie-break by earlier start time.
        candidates = sorted(
            owner.all_tasks(),
            key=lambda t: (PRIORITY_RANK.get(t.priority, 1), t.start_time),
        )
        for task in candidates:
            plan.add_task(task)
        plan.tasks.sort(key=lambda t: t.start_time)
        return plan

    def add_task(self, task: Task) -> bool:
        """Add a task only if it fits availability and creates no conflict.

        Returns True if scheduled, False if it was skipped.
        """
        if not self._fits(task):
            return False
        self.tasks.append(task)
        self.tasks.sort(key=lambda t: t.start_time)
        return True

    def remove_task(self, task: Task) -> None:
        """Remove a task from the plan."""
        self.tasks.remove(task)

    def fits_constraints(self) -> bool:
        """True if every scheduled task is within availability and no two
        tasks overlap.
        """
        for i, task in enumerate(self.tasks):
            if not self._within_availability(task):
                return False
            for other in self.tasks[i + 1:]:
                if task.conflicts_with(other):
                    return False
        return True

    def display(self) -> str:
        """Render the plan in a calendar-like, readable format."""
        header = f"Daily plan for {self.owner.name} — {self.date.isoformat()}"
        lines = [header]
        if not self.tasks:
            lines.append("  (no tasks scheduled)")
            return "\n".join(lines)
        for task in sorted(self.tasks, key=lambda t: t.start_time):
            pet_name = task.pet.name if task.pet else "?"
            check = "x" if task.done else " "
            when = task.start_time.strftime("%H:%M")
            lines.append(
                f"  [{check}] {when} — {task.description} for {pet_name} "
                f"({task.duration_minutes} min) [priority: {task.priority}]"
            )
        return "\n".join(lines)

    # --- internal scheduling helpers -------------------------------------

    def _within_availability(self, task: Task) -> bool:
        """True if the task fits entirely inside one availability window.

        With no availability set, the owner is treated as always free.
        """
        if not self.owner.availability:
            return True
        return any(
            start <= task.start_time and task.end_time <= end
            for start, end in self.owner.availability
        )

    def _fits(self, task: Task) -> bool:
        """True if the task is within availability and conflicts with nothing
        already scheduled.
        """
        if not self._within_availability(task):
            return False
        return not any(task.conflicts_with(existing) for existing in self.tasks)
