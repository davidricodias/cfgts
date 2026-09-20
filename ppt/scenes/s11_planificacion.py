"""Slide 12/16: planificación."""

from __future__ import annotations

import numpy as np
from common import ACCENT, INK, MUTED, ThemedSlide, body
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DashedLine,
    FadeIn,
    LaggedStart,
    Line,
    Rectangle,
    Text,
    VGroup,
)

# (fase, mes inicio, mes fin) con 0 = enero 2025 y 20 = septiembre 2026.
PHASES = [
    ("Investigaci\u00f3n y fundamentos", 0, 8),
    ("Formalizaci\u00f3n matem\u00e1tica", 4, 10),
    ("Implementaci\u00f3n del paquete", 6, 15),
    ("Experimentaci\u00f3n y resultados", 14, 19),
    ("Redacci\u00f3n de la memoria", 12, 20),
]

TOTAL_MONTHS = 20
TRACK_LEFT = -1.9
TRACK_WIDTH = 7.4
ROW_STEP = 0.62


def _month_x(month: int) -> float:
    return TRACK_LEFT + (month / TOTAL_MONTHS) * TRACK_WIDTH


class PlanificacionSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Planificaci\u00f3n")

        rows = VGroup()
        for index, (name, start, end) in enumerate(PHASES):
            y = -index * ROW_STEP
            left, right = _month_x(start), _month_x(end)
            bar = Rectangle(
                width=right - left,
                height=0.26,
                color=ACCENT,
                fill_opacity=0.85,
                stroke_width=0,
            ).move_to(np.array([(left + right) / 2, y, 0.0]))
            label = Text(name, font_size=21, color=INK)
            label.next_to(np.array([TRACK_LEFT, y, 0.0]), LEFT, buff=0.35)
            rows.add(VGroup(label, bar))

        baseline = Line(
            np.array([TRACK_LEFT, 0.45, 0.0]),
            np.array([TRACK_LEFT, -len(PHASES) * ROW_STEP + 0.15, 0.0]),
            color=MUTED,
            stroke_width=2,
        )
        ticks = VGroup()
        for month, name in ((0, "01/2025"), (TOTAL_MONTHS, "09/2026")):
            x = _month_x(month)
            ticks.add(
                DashedLine(
                    np.array([x, 0.45, 0.0]),
                    np.array([x, -len(PHASES) * ROW_STEP + 0.15, 0.0]),
                    color=MUTED,
                    stroke_width=1.5,
                ),
                Text(name, font_size=19, color=MUTED).move_to(np.array([x, 0.75, 0.0])),
            )

        gantt = VGroup(baseline, ticks, rows).next_to(head, DOWN, buff=0.75)

        self.play(Create(baseline), FadeIn(ticks), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(row, shift=RIGHT * 0.3) for row in rows], lag_ratio=0.2),
            run_time=2.0,
        )

        self.next_slide()
        note = body(
            "Veinte meses en bloques diarios cortos pero fases largas: hubo margen para "
            "reformular la puntuaci\u00f3n causal sin comprometer la entrega.",
            font_size=25,
            width=64,
            color=MUTED,
        ).next_to(gantt, DOWN, buff=0.5)
        self.play(FadeIn(note, shift=UP * 0.2))
