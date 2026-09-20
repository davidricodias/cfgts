"""Slide 9/16: resultados."""

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

# (etiqueta, puntuación media CFGTS, puntuación del control aleatorio)
ROWS = [
    ("AR(2) \u00b7 Lineal", 0.975, 0.891),
    ("AR(2) \u00b7 Random Forest", 0.599, 0.516),
    ("VAR(4) \u00b7 Lineal", 0.940, 0.869),
    ("VAR(4) \u00b7 Random Forest", 0.537, 0.413),
    ("Sunspots \u00b7 Lineal", 0.948, 0.917),
    ("Sunspots \u00b7 Random Forest", 0.500, 0.421),
]

BAR_SCALE = 5.2
BAR_HEIGHT = 0.15
BAR_GAP = 0.05
ROW_STEP = 0.56
BAR_ORIGIN_X = -2.2


def _bar(value: float, y: float, color: str) -> Rectangle:
    bar = Rectangle(
        width=value * BAR_SCALE, height=BAR_HEIGHT, color=color, fill_opacity=0.9, stroke_width=0
    )
    bar.move_to(np.array([BAR_ORIGIN_X + bar.width / 2, y, 0.0]))
    return bar


class ResultadosSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Resultados")

        rows = VGroup()
        for index, (label, score, control) in enumerate(ROWS):
            y = -index * ROW_STEP
            name = Text(label, font_size=21, color=INK)
            name.next_to(np.array([BAR_ORIGIN_X, y, 0.0]), LEFT, buff=0.3)
            top = _bar(score, y + (BAR_HEIGHT + BAR_GAP) / 2, ACCENT)
            bottom = _bar(control, y - (BAR_HEIGHT + BAR_GAP) / 2, MUTED)
            value = Text(f"{score:.3f}", font_size=20, color=ACCENT).next_to(top, RIGHT, buff=0.2)
            rows.add(VGroup(name, top, bottom, value))

        axis = Line(
            np.array([BAR_ORIGIN_X, 0.45, 0.0]),
            np.array([BAR_ORIGIN_X, -len(ROWS) * ROW_STEP + 0.1, 0.0]),
            color=MUTED,
            stroke_width=2,
        )
        chart = VGroup(axis, rows).next_to(head, DOWN, buff=0.6)

        legend = VGroup(
            VGroup(
                Rectangle(width=0.4, height=0.15, color=ACCENT, fill_opacity=0.9, stroke_width=0),
                Text("CFGTS", font_size=20, color=INK),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Rectangle(width=0.4, height=0.15, color=MUTED, fill_opacity=0.9, stroke_width=0),
                Text("control aleatorio", font_size=20, color=INK),
            ).arrange(RIGHT, buff=0.2),
        ).arrange(RIGHT, buff=0.9)
        legend.next_to(chart, DOWN, buff=0.45)

        self.play(FadeIn(axis), FadeIn(legend), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(row, shift=RIGHT * 0.3) for row in rows], lag_ratio=0.15),
            run_time=2.0,
        )

        self.next_slide()
        first = body(
            "La naturaleza del modelo domina la puntuaci\u00f3n: "
            "lineal cerca de 1, Random Forest en torno a 0,5.",
            font_size=26,
            width=62,
        ).next_to(legend, DOWN, buff=0.4)
        self.play(Write(first))

        self.next_slide()
        second = body(
            "CFGTS supera al control aleatorio en las seis configuraciones.",
            font_size=28,
            width=62,
            color=WARM,
        ).move_to(first)
        self.play(FadeIn(second, shift=UP * 0.2), first.animate.shift(UP * 0.45))
