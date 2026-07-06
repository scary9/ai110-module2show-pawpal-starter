"""Demo: build a day of pet care tasks and print today's schedule."""

from datetime import date, datetime

from cli_display import render_conflict_warning, render_plan
from pawpal_system import DailyPlan, Owner, Pet, Task

today = date.today()

owner = Owner(name="Sam")

biscuit = Pet(name="Biscuit", species="Golden Retriever")
mittens = Pet(name="Mittens", species="Cat")
owner.add_pet(biscuit)
owner.add_pet(mittens)

# Added out of time order on purpose to check the plan sorts them.
biscuit.add_task(Task("Dinner", datetime(today.year, today.month, today.day, 18, 0), 15, priority="medium"))
mittens.add_task(Task("Feeding", datetime(today.year, today.month, today.day, 8, 0), 10, priority="high"))
biscuit.add_task(Task("Morning walk", datetime(today.year, today.month, today.day, 8, 0), 30, priority="high"))

plan = DailyPlan(date=today, owner=owner, tasks=owner.all_tasks())
plan.sort_by_time()

print(render_plan(plan))
warning = render_conflict_warning(plan)
if warning:
    print(warning)
