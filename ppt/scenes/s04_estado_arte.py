"""Slide 7/16: estado del arte."""

from __future__ import annotations

import numpy as np

from common import ACCENT, GREEN, INK, MUTED, WARM, ThemedSlide, body, eq
from manim import (
    DOWN,
    RIGHT,
    UP,
    Arrow,
    Axes,
    Circumscribe,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    LaggedStart,
    Rectangle,
    Text,
    VGroup,
    Write,
)


def _forecast_curve(x: float) -> float:
    """Synthetic differentiable forecaster f(x), only used to draw the diagram."""
    return 0.25 * (x - 5) + 1.5 + 0.6 * np.sin(1.3 * x)


ALPHA, BETA = 2.0, 2.6
ORIGINAL_X, COUNTERFACTUAL_X = 2.0, 7.0

PROPERTIES = [
    "Validez",
    "Minimalidad",
    "Similaridad",
    "Plausibilidad",
    "Poder discriminante",
    "Accionabilidad",
    "Causalidad",
    "Diversidad",
]
CAUSALITY_INDEX = 6


class EstadoArteSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Estado del arte")

        intro = body(
            "Propiedades deseables de una explicación contrafactual:",
            font_size=28,
            width=58,
        ).next_to(head, DOWN, buff=0.55)

        items = VGroup(
            *[Text(f"\u2022 {name}", font_size=27, color=INK) for name in PROPERTIES]
        ).arrange_in_grid(rows=4, cols=2, buff=(1.6, 0.38), col_alignments="ll")
        items.next_to(intro, DOWN, buff=0.55)

        self.play(Write(intro))
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.2) for item in items], lag_ratio=0.15))

        self.next_slide()
        gap = items[CAUSALITY_INDEX]
        self.play(gap.animate.set_color(WARM), Circumscribe(gap, color=WARM))
        note = body(
            "Ningún método domina todas a la vez, y cómo incorporar "
            "causalidad sigue siendo una pregunta abierta.",
            font_size=26,
            width=60,
            color=MUTED,
        ).next_to(items, DOWN, buff=0.55)
        self.play(FadeIn(note, shift=UP * 0.2))

        self.next_slide()
        gap_text = body(
            "Además, la literatura se concentra en clasificación. "
            "En regresión sobre series temporales apenas hay métodos: "
            "CounTS y ForecastCF.",
            font_size=30,
            width=48,
        ).shift(UP * 0.4)
        self.play(FadeOut(intro), FadeOut(items), FadeOut(note))
        self.play(Write(gap_text))

        self.next_slide()
        here = Text("Ahí se sitúa CFGTS", font_size=34, color=ACCENT, weight="BOLD").move_to(
            gap_text
        )
        self.play(FadeOut(gap_text), FadeIn(here, shift=UP * 0.3))
