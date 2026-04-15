"""Scene transition helper functions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Transition:
    """Represents a transition style and duration."""

    name: str
    duration: float = 0.6


def fade(duration: float = 0.6) -> Transition:
    """Create a fade transition."""
    return Transition(name="fade", duration=duration)


def slide(direction: str = "left", duration: float = 0.6) -> Transition:
    """Create a slide transition."""
    direction = direction.lower()
    if direction not in {"left", "right"}:
        raise ValueError("direction must be 'left' or 'right'")
    return Transition(name=f"slide-{direction}", duration=duration)


def cross_dissolve(duration: float = 0.6) -> Transition:
    """Create a cross dissolve transition."""
    return Transition(name="cross-dissolve", duration=duration)
