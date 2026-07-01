"""PawPal+ core class skeletons.

Generated from diagrams/uml.mmd. Method bodies are left as `pass`/TODO
so the scheduling logic can be filled in during implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class TimeSlot:
    """A window of time an owner is available."""

    start: time
    end: time


@dataclass
class CareNeed:
    """A recurring care requirement for a pet (e.g. walk, meds, groom)."""

    type: str
    frequency: int  # times per day
    duration_minutes: int


@dataclass
class Owner:
    """A pet owner with scheduling preferences and constraints."""

    name: str
    preferred_time: time | None = None
    preferences: list[str] = field(default_factory=list)
    availability: list[TimeSlot] = field(default_factory=list)
    pets: list["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        raise NotImplementedError

    def remove_pet(self, pet: "Pet") -> None:
        raise NotImplementedError

    def update_availability(self, slots: list[TimeSlot]) -> None:
        raise NotImplementedError

    def update_preferences(self, prefs: list[str]) -> None:
        raise NotImplementedError


@dataclass
class Pet:
    """A pet with care needs, an assigned set of owners, and a priority."""

    name: str
    species: str
    priority: int = 0
    care_needs: list[CareNeed] = field(default_factory=list)
    assigned_owners: list[Owner] = field(default_factory=list)

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


@dataclass
class Task:
    """A single scheduled action for a pet within a daily plan."""

    action: str
    start_time: time
    duration_minutes: int
    pet: Pet
    priority: int = 0


@dataclass
class DailyPlan:
    """A calendar-style plan of tasks for a set of pets on a given day."""

    date: date
    pets: list[Pet] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        raise NotImplementedError

    def remove_task(self, task: Task) -> None:
        raise NotImplementedError

    def fits_constraints(self, owner: Owner) -> bool:
        raise NotImplementedError
