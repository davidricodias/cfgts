"""Slide 13/16: presupuesto."""

from __future__ import annotations

import numpy as np
from common import ACCENT, INK, MUTED, WARM, ThemedSlide, body
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    LaggedStart,
    Line,
    Rectangle,
    Text,
    VGroup,
    Write,
)

ITEMS = [
    ("Personal", 10250.00, ACCENT),
    ("Recursos materiales y software", 656.25, MUTED),
    ("Costes indirectos", 115.28, MUTED),
]
TOTAL = 11021.53

BAR_SCALE = 7.0 / TOTAL
ROW_STEP = 0.72
BAR_ORIGIN_X = -1.4


def _amount(value: float) -> str:
    return f"{value:,.2f} \u20ac".replace(",", "@").replace(".", ",").replace("@", ".")


class PresupuestoSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Presupuesto")

        rows = VGroup()
        for index, (name, amount, color) in enumerate(ITEMS):
            y = -index * ROW_STEP
            bar = Rectangle(
                width=max(amount * BAR_SCALE, 0.04),
                height=0.3,
                color=color,
                fill_opacity=0.9,
                stroke_width=0,
            )
            bar.move_to(np.array([BAR_ORIGIN_X + bar.width / 2, y, 0.0]))
            label = Text(name, font_size=22, color=INK)
            label.next_to(np.array([BAR_ORIGIN_X, y, 0.0]), LEFT, buff=0.35)
            value = Text(_amount(amount), font_size=21, color=color).next_to(bar, RIGHT, buff=0.25)
            rows.add(VGroup(label, bar, value))

        axis = Line(
            np.array([BAR_ORIGIN_X, 0.45, 0.0]),
            np.array([BAR_ORIGIN_X, -len(ITEMS) * ROW_STEP + 0.3, 0.0]),
            color=MUTED,
            stroke_width=2,
        )
        chart = VGroup(axis, rows).next_to(head, DOWN, buff=0.9)

        self.play(FadeIn(axis), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(row, shift=RIGHT * 0.3) for row in rows], lag_ratio=0.25),
            run_time=1.8,
        )

        self.next_slide()
        share = body(
            " El coste de personal supone el 93 %",
            font_size=26,
            width=60,
            color=WARM,
        ).next_to(chart, DOWN, buff=0.6)
        self.play(Write(share))

        self.next_slide()
        total = Text(
            f"Total estimado: {_amount(TOTAL)}",
            font_size=34,
            color=ACCENT,
            weight="BOLD",
        ).next_to(share, DOWN, buff=0.55)
        self.play(FadeIn(total, shift=UP * 0.25))
