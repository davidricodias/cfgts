"""Slide 13/20: resultados."""

from __future__ import annotations

from common import ACCENT, INK, MUTED, ThemedSlide, body, reveal_staggered, row_label, value_bar, vertical_axis
from manim import (
    DOWN,
    RIGHT,
    UP,
    FadeIn,
    FadeOut,
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


class ResultadosSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Resultados")

        rows = VGroup()
        for index, (label, score, control) in enumerate(ROWS):
            y = -index * ROW_STEP
            name = row_label(label, BAR_ORIGIN_X, y, font_size=21)
            top = value_bar(
                score, y + (BAR_HEIGHT + BAR_GAP) / 2, ACCENT, origin_x=BAR_ORIGIN_X, scale=BAR_SCALE, height=BAR_HEIGHT
            )
            bottom = value_bar(
                control, y - (BAR_HEIGHT + BAR_GAP) / 2, MUTED, origin_x=BAR_ORIGIN_X, scale=BAR_SCALE, height=BAR_HEIGHT
            )
            value = Text(f"{score:.3f}", font_size=20, color=ACCENT).next_to(top, RIGHT, buff=0.2)
            rows.add(VGroup(name, top, bottom, value))

        axis = vertical_axis(BAR_ORIGIN_X, 0.45, -len(ROWS) * ROW_STEP + 0.1)
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
        reveal_staggered(self, rows, shift=RIGHT * 0.3, lag_ratio=0.15, run_time=2.0)

        self.next_slide()
        first = body(
            "La naturaleza del modelo domina el causal score",
            font_size=26,
            width=62,
        ).next_to(legend, DOWN, buff=0.4)
        self.play(Write(first))

        self.next_slide()
        second = body(
            "CFGTS supera el control aleatorio",
            font_size=28,
            width=62,
            color=INK,
        ).move_to(first)
        self.play(FadeOut(first), FadeIn(second, shift=UP * 0.2))
