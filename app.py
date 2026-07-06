from datetime import date, datetime

import streamlit as st
from pawpal_system import DailyPlan, Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Build the owner, pets, and tasks with direct method calls (same as main.py).
# Seed once and store in the session "vault" using key membership so reruns
# reuse the same object instead of re-adding the pets/tasks.
if "owner" not in st.session_state:
    today = date.today()

    owner = Owner(name="Sam")

    biscuit = Pet(name="Biscuit", species="Golden Retriever")
    mittens = Pet(name="Mittens", species="Cat")
    owner.add_pet(biscuit)
    owner.add_pet(mittens)

    biscuit.add_task(Task("Morning walk", datetime(today.year, today.month, today.day, 8, 0), 30, priority="high"))
    mittens.add_task(Task("Feeding", datetime(today.year, today.month, today.day, 9, 0), 10, priority="high"))
    biscuit.add_task(Task("Dinner", datetime(today.year, today.month, today.day, 18, 0), 15, priority="medium"))

    st.session_state.owner = owner
owner = st.session_state.owner

st.divider()

# --- Current Pets & Tasks ------------------------------------------------
# Read straight from the Owner object so the UI always reflects real state.
st.subheader("Current Pets & Tasks")
if owner.pets:
    # Filter controls backed by Owner.filter_tasks so the table reflects the
    # same logic the scheduler uses -- no parallel filtering in the UI.
    col_pet, col_status = st.columns(2)
    pet_choice = col_pet.selectbox(
        "Pet", ["All"] + [pet.name for pet in owner.pets]
    )
    status_choice = col_status.selectbox("Status", ["All", "To do", "Done"])

    pet_name = None if pet_choice == "All" else pet_choice
    done = {"All": None, "To do": False, "Done": True}[status_choice]

    # Show tasks sorted by start time for a clean, calendar-like table.
    tasks = sorted(
        owner.filter_tasks(done=done, pet_name=pet_name),
        key=lambda t: t.start_time,
    )
    if tasks:
        rows = [
            {
                "Time": t.start_time.strftime("%H:%M"),
                "Task": t.description,
                "Pet": t.pet.name if t.pet else "?",
                "Duration": f"{t.duration_minutes} min",
                "Priority": t.priority.capitalize(),
                "Frequency": t.frequency.capitalize(),
                "Status": "✅ Done" if t.done else "⏳ To do",
            }
            for t in tasks
        ]
        st.table(rows)
        st.caption(f"{len(tasks)} task(s) shown.")
    else:
        st.caption("No tasks match the current filters.")
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Build Schedule ------------------------------------------------------
st.subheader("Build Schedule")
if st.button("Generate schedule"):
    # generate() already places tasks by priority and keeps them sorted by
    # time; sort_by_time() is called defensively in case the plan is edited.
    plan = DailyPlan.generate(owner, date.today())
    plan.sort_by_time()

    # Render the time-ordered plan as a table instead of raw text.
    if plan.tasks:
        st.table(
            [
                {
                    "Time": t.start_time.strftime("%H:%M"),
                    "Task": t.description,
                    "Pet": t.pet.name if t.pet else "?",
                    "Duration": f"{t.duration_minutes} min",
                    "Priority": t.priority.capitalize(),
                    "Done": "✅" if t.done else "",
                }
                for t in plan.tasks
            ]
        )
    else:
        st.caption("No tasks could be scheduled for today.")

    # Surface the class's own conflict detection instead of re-deriving it here.
    warning = plan.conflict_warning()
    if warning:
        st.warning(warning)
        # Break the conflicts out individually so each overlap is scannable.
        for a, b, kind in plan.time_conflicts():
            a_pet = a.pet.name if a.pet else "?"
            b_pet = b.pet.name if b.pet else "?"
            label = "same pet" if kind == "same-pet" else "different pets"
            st.caption(
                f"⚠️ {a.start_time:%H:%M} {a.description} ({a_pet}) overlaps "
                f"{b.start_time:%H:%M} {b.description} ({b_pet}) — {label}"
            )
    elif plan.fits_constraints():
        st.success("✅ Conflict-free plan — every task fits the owner's availability.")
    else:
        st.info("No time conflicts, but some tasks fall outside availability windows.")
