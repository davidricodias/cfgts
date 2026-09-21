"""Slide 17/20: presupuesto."""

from __future__ import annotations

from common import ACCENT, MUTED, ThemedSlide, reveal_staggered, row_label, value_bar, vertical_axis
from manim import (
    DOWN,
    RIGHT,
    UP,
    FadeIn,
    Text,
    VGroup,
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
            bar = value_bar(amount, y, color, origin_x=BAR_ORIGIN_X, scale=BAR_SCALE, height=0.3, min_width=0.04)
            label = row_label(name, BAR_ORIGIN_X, y, font_size=22, buff=0.35)
            value = Text(_amount(amount), font_size=21, color=color).next_to(bar, RIGHT, buff=0.25)
            rows.add(VGroup(label, bar, value))

        axis = vertical_axis(BAR_ORIGIN_X, 0.45, -len(ITEMS) * ROW_STEP + 0.3)
        chart = VGroup(axis, rows).next_to(head, DOWN, buff=0.9)

        self.play(FadeIn(axis), run_time=0.5)
        reveal_staggered(self, rows, shift=RIGHT * 0.3, lag_ratio=0.25, run_time=1.8)
        self.next_slide()
        total = Text(
            f"Total estimado: {_amount(TOTAL)}",
            font_size=34,
            color=ACCENT,
            weight="BOLD",
        ).next_to(chart, DOWN, buff=0.55)
        self.play(FadeIn(total, shift=UP * 0.25))
