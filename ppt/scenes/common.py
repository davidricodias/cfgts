"""Shared palette/helpers for the ppt/ slide scripts.

Prose uses Pango `Text` (native accent support); only equations use
`MathTex`, so no Spanish text ever goes through the LaTeX toolchain.
"""

from __future__ import annotations

import textwrap

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    Line,
    ManimColor,
    MathTex,
    Mobject,
    Text,
    VGroup,
    Write,
)
from manim_slides import Slide

BG = "#F2F4FF"
INK = "#12163A"
MUTED = "#525C82"
ACCENT = "#1F52C4"
WARM = "#C4451F"
GREEN = "#1F7A4C"


def wrap(text: str, width: int = 46) -> str:
    """Textwrap because `Text` does not wrap on its own."""
    return "\n".join(textwrap.wrap(text, width=width))


def body(text: str, *, font_size: int = 28, width: int = 46, color: str = INK) -> Text:
    return Text(wrap(text, width), font_size=font_size, color=color, line_spacing=1.15)


def bullets(items: list[str], *, font_size: int = 28, width: int = 46) -> VGroup:
    return VGroup(
        *[
            Text(f"\u2022 {wrap(item, width)}", font_size=font_size, color=INK, line_spacing=1.15)
            for item in items
        ]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)


def eq(*tex: str, font_size: int = 38, color: str = INK) -> MathTex:
    """`MathTex` renders white by default, invisible on this light background."""
    return MathTex(*tex, font_size=font_size, color=color)


def fit_below(group: Mobject, reference: Mobject, *, buff: float = 0.6, bottom: float = -3.9):
    """Place `group` under `reference`, shrinking it if it would overflow `bottom`."""
    available = reference.get_bottom()[1] - buff - bottom
    if group.height > available:
        group.scale(available / group.height)
    group.next_to(reference, DOWN, buff=buff)
    return group


class ThemedSlide(Slide):
    """Light-background slide with a consistent animated heading."""

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = ManimColor(BG)

    def show_heading(self, text: str, *, font_size: int = 38) -> VGroup:
        label = Text(text, font_size=font_size, color=ACCENT, weight="BOLD")
        rule = Line(
            label.get_corner(DOWN + LEFT),
            label.get_corner(DOWN + RIGHT),
            color=ACCENT,
            stroke_width=3,
        ).shift(DOWN * 0.2)
        group = VGroup(label, rule).to_edge(UP, buff=0.45)
        self.play(Write(label), Create(rule), run_time=1.0)
        return group
