"""Demo: build a day of pet care tasks and print today's schedule."""

from datetime import date, datetime

from pawpal_system import DailyPlan, Owner, Pet, Task

today = date.today()

owner = Owner(name="Sam")

biscuit = Pet(name="Biscuit", species="Golden Retriever")
mittens = Pet(name="Mittens", species="Cat")
owner.add_pet(biscuit)
owner.add_pet(mittens)

biscuit.add_task(Task("Morning walk", datetime(today.year, today.month, today.day, 8, 0), 30, priority="high"))
mittens.add_task(Task("Feeding", datetime(today.year, today.month, today.day, 9, 0), 10, priority="high"))
biscuit.add_task(Task("Dinner", datetime(today.year, today.month, today.day, 18, 0), 15, priority="medium"))

plan = DailyPlan.generate(owner, today)

print("Today's Schedule")
print(plan.display())
