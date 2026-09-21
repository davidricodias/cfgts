"""Slide 8/16: análisis del problema."""

from __future__ import annotations

from common import ACCENT, ThemedSlide, disc_marker, eq, marker_item
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    Text,
    VGroup,
    Write,
)

REQUIREMENTS = [
    "No depender del conjunto de entrenamiento original.",
    "Aproximar un objetivo vectorial en las D salidas, no una sola variable.",
    "Respetar la estructura temporal codificada en los retardos.",
    "Puntuar la consistencia causal de cada candidato.",
]


def _requirement(number: int, text: str) -> VGroup:
    return marker_item(disc_marker(number), text, font_size=26, width=52)


class AnalisisProblemaSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Análisis del problema")

        given = eq(
            r"\hat{f}: \mathbb{R}^{n_{\mathrm{In}}} \to \mathbb{R}^{D},",
            r"\quad \mathbf{x}_0,",
            r"\quad \mathbf{y}^{*} \in \mathbb{R}^{D}",
            font_size=36,
        ).next_to(head, DOWN, buff=0.6)
        self.play(Write(given))

        self.next_slide()
        items = VGroup(*[_requirement(i + 1, t) for i, t in enumerate(REQUIREMENTS)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(given, DOWN, buff=0.7)

        for item in items:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.7)
            self.next_slide()

        closing = Text(
            "Más restrictivo que el caso tabular estático",
            font_size=28,
            color=ACCENT,
            weight="BOLD",
        ).next_to(items, DOWN, buff=0.55)
        self.play(FadeIn(closing, shift=UP * 0.2))
