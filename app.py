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
    for pet in owner.pets:
        st.markdown(f"**{pet.name}** ({pet.species}) — priority: {pet.priority}")
        if pet.tasks:
            for t in pet.tasks:
                st.write(
                    f"- {t.start_time.strftime('%H:%M')} — {t.description} "
                    f"({t.duration_minutes} min) [{t.priority}]"
                )
        else:
            st.caption("No tasks yet.")
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Build Schedule ------------------------------------------------------
st.subheader("Build Schedule")
if st.button("Generate schedule"):
    plan = DailyPlan.generate(owner, date.today())
    st.text(plan.display())
