"""Simple tests for PawPal+ core behaviors."""

from datetime import datetime

from pawpal_system import Pet, Task


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
