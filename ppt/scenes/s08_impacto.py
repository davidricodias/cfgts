"""Slide 11/16: impacto económico, social, medioambiental y ético."""

from __future__ import annotations

from common import ACCENT, INK, MUTED, ThemedSlide, body, card, fit_below, reveal_card, wrap
from manim import (
    DOWN,
    UP,
    FadeIn,
    Text,
    VGroup,
)

QUADRANTS = [
    (
        "Económico",
        "Auditar un modelo sin su conjunto de entrenamiento y sin código específico "
        "por tipo de modelo abarata la explicabilidad.",
    ),
    (
        "Social",
        "Mejora la confianza que el operador del modelo tiene sobre los outputs"
    ),
    (
        "Medioambiental",
        "Cientos de evaluaciones del modelo por explicación, es intensivo energéticamente"
    ),
    (
        "Ético",
        "Riesgo de explicabilidad de fachada y de abuso de la whitelist para justificar "
        "decisiones sesgadas.",
    ),
]


def _quadrant(title: str, text: str, accent: str) -> VGroup:
    lines = Text(wrap(text, 34), font_size=20, color=INK, line_spacing=1.15)
    return card(title, lines, title_color=accent, buff=0.3, gap=0.3)


class ImpactoSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Impacto económico, social, medioambiental y ético")

        colors = [ACCENT, ACCENT, ACCENT, ACCENT]
        grid = VGroup(
            *[
                _quadrant(title, text, color)
                for (title, text), color in zip(QUADRANTS, colors, strict=False)
            ]
        )
        grid.arrange_in_grid(rows=2, cols=2, buff=(0.6, 0.5))
        fit_below(grid, head, buff=0.5, bottom=-3.0)

        for card_group in grid:
            reveal_card(self, card_group, frame_run_time=0.6, body_run_time=0.6, body_shift=UP * 0.15)
            self.next_slide()

        closing = body(
            "El impacto es indirecto: depende del operador de CFGTS",
            font_size=25,
            width=80,
            color=MUTED,
        ).next_to(grid, DOWN, buff=0.45)
        self.play(FadeIn(closing, shift=UP * 0.2))
