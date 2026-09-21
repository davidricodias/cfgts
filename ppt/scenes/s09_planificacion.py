"""Slide 12/16: planificación."""

from __future__ import annotations

import numpy as np
from common import ACCENT, MUTED, ThemedSlide, body, range_bar, reveal_staggered, row_label, vertical_axis
from manim import (
    DOWN,
    RIGHT,
    UP,
    Create,
    DashedLine,
    FadeIn,
    Text,
    VGroup,
)

# (fase, mes inicio, mes fin) con 0 = enero 2025 y 20 = septiembre 2026.
PHASES = [
    ("Investigación y fundamentos", 0, 8),
    ("Formalización matemática", 4, 10),
    ("Implementación del paquete", 6, 15),
    ("Experimentación y resultados", 14, 19),
    ("Redacción de la memoria", 12, 20),
]

TOTAL_MONTHS = 20
TRACK_LEFT = -1.9
TRACK_WIDTH = 7.4
ROW_STEP = 0.62


def _month_x(month: int) -> float:
    return TRACK_LEFT + (month / TOTAL_MONTHS) * TRACK_WIDTH


class PlanificacionSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Planificación")

        rows = VGroup()
        for index, (name, start, end) in enumerate(PHASES):
            y = -index * ROW_STEP
            bar = range_bar(_month_x(start), _month_x(end), y, ACCENT, height=0.26)
            label = row_label(name, TRACK_LEFT, y, font_size=21, buff=0.35)
            rows.add(VGroup(label, bar))

        bottom = -len(PHASES) * ROW_STEP + 0.15
        baseline = vertical_axis(TRACK_LEFT, 0.45, bottom)
        ticks = VGroup()
        for month, name in ((0, "01/2025"), (TOTAL_MONTHS, "09/2026")):
            x = _month_x(month)
            ticks.add(
                DashedLine(
                    np.array([x, 0.45, 0.0]),
                    np.array([x, bottom, 0.0]),
                    color=MUTED,
                    stroke_width=1.5,
                ),
                Text(name, font_size=19, color=MUTED).move_to(np.array([x, 0.75, 0.0])),
            )

        gantt = VGroup(baseline, ticks, rows).next_to(head, DOWN, buff=0.75)

        self.play(Create(baseline), FadeIn(ticks), run_time=0.8)
        reveal_staggered(self, rows, shift=RIGHT * 0.3, lag_ratio=0.2, run_time=2.0)

        self.next_slide()
        note = body(
            "Veinte largos meses: no se pudo hacer antes por otras obligaciones",
            font_size=25,
            width=64,
            color=MUTED,
        ).next_to(gantt, DOWN, buff=0.5)
        self.play(FadeIn(note, shift=UP * 0.2))
