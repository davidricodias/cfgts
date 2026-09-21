"""Slide 18/20: conclusiones."""

from __future__ import annotations

from common import ACCENT, ThemedSlide, body, fit_below, marker_item
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    Text,
    VGroup,
)

CONCLUSIONS = [
    "Algoritmo de tres fases formalizado: optimización bi-objetivo, conjunto de "
    "cobertura y consistencia causal.",
    "La formalización precisa la validez de los candidatos, la región factible y "
    "el significado de la puntuación.",
    "Implementación en Python agnóstica al regresor de scikit-learn, publicada en PyPI.",
    "La evaluación confirma que la puntuación depende de la naturaleza del modelo.",
]


class ConclusionesSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Conclusiones")

        items = VGroup(
            *[
                marker_item(
                    Text("\u2713", font_size=30, color=ACCENT, weight="BOLD"),
                    text,
                    font_size=25,
                    width=52,
                    aligned_edge=UP,
                )
                for text in CONCLUSIONS
            ]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        fit_below(items, head, buff=0.7, bottom=-2.9)

        for item in items:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.7)
            self.next_slide()

        closing = body(
            "Una base técnica y conceptual para seguir construyendo",
            font_size=26,
            width=80,
            color=ACCENT,
        ).next_to(items, DOWN, buff=0.55)
        self.play(FadeIn(closing, shift=UP * 0.2))
