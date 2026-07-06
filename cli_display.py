"""User-friendly terminal rendering for PawPal+ plans.

Kept separate from ``pawpal_system.py`` so the domain model stays free of
presentation concerns (ANSI colors, emojis, table layout). The core classes
never import this module; this module imports them.

Highlights:
- Emojis per task type, chosen from keywords in the task description.
- Color-coded priority (red/yellow/green) and status (done/to-do).
- A structured table via ``tabulate`` (with a plain fallback if it's absent).
- Color auto-disables when stdout isn't a terminal, so piping to a file or
  redirecting into logs doesn't leave escape sequences behind.
"""

from __future__ import annotations

import sys

from pawpal_system import DailyPlan

try:
    from tabulate import tabulate

    _HAVE_TABULATE = True
except ImportError:  # pragma: no cover - exercised only without the dependency
    _HAVE_TABULATE = False


# ANSI style codes. Minimal on purpose; only what the renderer uses.
_ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "cyan": "\033[36m",
}

# Emoji per task type, matched by keyword against the description. First match
# wins, so list the more specific keywords earlier.
_TASK_EMOJI = [
    (("walk", "stroll"), "🚶"),
    (("feed", "food", "dinner", "breakfast", "lunch", "meal"), "🍽️"),
    (("water",), "💧"),
    (("med", "pill", "medicine", "medication", "vaccin"), "💊"),
    (("vet", "checkup", "appointment"), "🏥"),
    (("bath", "wash"), "🛁"),
    (("brush", "groom", "nail"), "✂️"),
    (("play", "fetch", "toy"), "🎾"),
    (("train",), "🎓"),
    (("sleep", "nap", "bed"), "😴"),
]
_DEFAULT_EMOJI = "🐾"

# Emoji + ANSI color per priority level.
_PRIORITY_STYLE = {
    "high": ("🔴", "red"),
    "medium": ("🟡", "yellow"),
    "low": ("🟢", "green"),
}


def task_emoji(description: str) -> str:
    """Pick an emoji for a task from keywords in its description."""
    text = description.casefold()
    for keywords, emoji in _TASK_EMOJI:
        if any(word in text for word in keywords):
            return emoji
    return _DEFAULT_EMOJI


def _use_color(color: bool | None) -> bool:
    """Resolve whether to emit ANSI color. None means auto-detect a TTY."""
    if color is None:
        return sys.stdout.isatty()
    return color


def _paint(text: str, *styles: str, enabled: bool) -> str:
    """Wrap text in ANSI styles when enabled, else return it unchanged."""
    if not enabled or not styles:
        return text
    codes = "".join(_ANSI[s] for s in styles)
    return f"{codes}{text}{_ANSI['reset']}"


def render_plan(plan: DailyPlan, color: bool | None = None) -> str:
    """Render a DailyPlan as a colorful, emoji-annotated CLI table.

    color : True/False forces ANSI color on/off; None (default) auto-detects
            whether stdout is a terminal.
    """
    enabled = _use_color(color)
    title = _paint(
        f"🐾 Daily plan for {plan.owner.name} — {plan.date.isoformat()}",
        "bold",
        "cyan",
        enabled=enabled,
    )
    if not plan.tasks:
        return f"{title}\n  (no tasks scheduled)"

    rows = []
    for t in sorted(plan.tasks, key=lambda task: task.start_time):
        pet = t.pet.name if t.pet else "?"
        p_emoji, p_color = _PRIORITY_STYLE.get(t.priority, ("⚪", "dim"))
        status = (
            _paint("✅ done", "green", enabled=enabled)
            if t.done
            else _paint("⏳ to do", "yellow", enabled=enabled)
        )
        rows.append(
            [
                t.start_time.strftime("%H:%M"),
                f"{task_emoji(t.description)} {t.description}",
                pet,
                f"{t.duration_minutes} min",
                _paint(f"{p_emoji} {t.priority.capitalize()}", p_color, enabled=enabled),
                status,
            ]
        )

    headers = ["Time", "Task", "Pet", "Duration", "Priority", "Status"]
    if _HAVE_TABULATE:
        table = tabulate(rows, headers=headers, tablefmt="rounded_outline")
    else:  # pragma: no cover - exercised only without the dependency
        table = _plain_table(headers, rows)
    return f"{title}\n{table}"


def render_conflict_warning(plan: DailyPlan, color: bool | None = None) -> str:
    """The plan's conflict warning, painted red when color is enabled.

    Returns an empty string when the plan is conflict-free.
    """
    warning = plan.conflict_warning()
    if not warning:
        return ""
    return _paint(warning, "red", enabled=_use_color(color))


def _plain_table(headers, rows) -> str:  # pragma: no cover - fallback path
    """Minimal pipe-separated table used when ``tabulate`` isn't installed."""
    lines = [" | ".join(headers), "-+-".join("-" * len(h) for h in headers)]
    lines.extend(" | ".join(str(cell) for cell in row) for row in rows)
    return "\n".join(lines)
