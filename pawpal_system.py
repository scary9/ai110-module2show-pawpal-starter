"""PawPal+ core class skeletons.

Generated from diagrams/uml.mmd. Method bodies are left as stubs
(`NotImplementedError`) so the scheduling logic can be filled in during
implementation.

Design decisions baked into this skeleton:
- Single-owner model: one Owner cares for their Pets (README scenario).
- Entity classes (Owner, Pet) use identity equality (eq=False) so two pets
  with the same name are still distinct objects and are hashable.
- DailyPlan derives its pets from its tasks (single source of truth) and owns
  its own generate/display logic. The app itself is the "assistant" that
  generates plans, so it is not modeled as a class.
- Task records which CareNeed it satisfies (for coverage checks). The owner is
  assumed responsible for carrying out the tasks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class TimeSlot:
    """A window of time an owner is available (value object)."""

    start: datetime
    end: datetime

    def overlaps(self, other: "TimeSlot") -> bool:
        return self.start < other.end and other.start < self.end


@dataclass
class CareNeed:
    """A recurring care requirement for a pet (e.g. walk, meds, groom)."""

    type: str
    frequency: int  # times per day
    duration_minutes: int


@dataclass(eq=False)
class Pet:
    """A pet with care needs and a priority.

    priority: higher int = more urgent.
    eq=False -> identity semantics (two same-named pets stay distinct) and
    hashable, so pets can live in sets / dict keys.
    """

    name: str
    species: str
    priority: int = 0
    care_needs: list[CareNeed] = field(default_factory=list)

    def update_priority(self, level: int) -> None:
        raise NotImplementedError

    def feed(self) -> None:
        raise NotImplementedError

    def walk(self) -> None:
        raise NotImplementedError

    def groom(self) -> None:
        raise NotImplementedError

    def play(self) -> None:
        raise NotImplementedError


@dataclass(eq=False)
class Owner:
    """The pet owner the plan is built around.

    Their availability + preferences are the constraints the plan respects.
    """

    name: str
    preferred_time: datetime | None = None
    preferences: list[str] = field(default_factory=list)
    availability: list[TimeSlot] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def remove_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def update_availability(self, slots: list[TimeSlot]) -> None:
        raise NotImplementedError

    def update_preferences(self, prefs: list[str]) -> None:
        raise NotImplementedError


@dataclass
class Task:
    """A single scheduled action within a daily plan.

    care_need -> which CareNeed this task satisfies (for coverage checks).
    """

    action: str
    start_time: datetime
    duration_minutes: int
    pet: Pet
    care_need: CareNeed | None = None
    priority: int = 0

    @property
    def end_time(self) -> datetime:
        """Computed end so conflict detection is simple interval math."""
        raise NotImplementedError

    def conflicts_with(self, other: "Task") -> bool:
        raise NotImplementedError


@dataclass
class DailyPlan:
    """A calendar-style plan of tasks for the owner on a given day.

    Owns its own generation/display logic -- the app is the "assistant".
    """

    date: date
    owner: Owner
    tasks: list[Task] = field(default_factory=list)

    @property
    def pets(self) -> set[Pet]:
        """Derived from tasks -> single source of truth (no duplicate list)."""
        return {task.pet for task in self.tasks}

    @classmethod
    def generate(cls, owner: Owner, day: date) -> "DailyPlan":
        """Expand the owner's pets' CareNeeds into Tasks that fit their slots."""
        raise NotImplementedError

    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        raise NotImplementedError

    def fits_constraints(self) -> bool:
        """Checks tasks against the owner's availability."""
        raise NotImplementedError

    def display(self) -> str:
        """Render the plan in a calendar-like, readable format."""
        raise NotImplementedError
