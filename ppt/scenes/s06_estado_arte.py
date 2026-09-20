"""Slide 7/16: estado del arte."""

from __future__ import annotations

from common import ACCENT, INK, MUTED, WARM, ThemedSlide, body
from manim import (
    DOWN,
    UP,
    Circumscribe,
    FadeIn,
    FadeOut,
    LaggedStart,
    Text,
    VGroup,
    Write,
)

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
            "Propiedades deseables de una explicaci\u00f3n contrafactual:",
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
            "Ning\u00fan m\u00e9todo domina todas a la vez, y c\u00f3mo incorporar "
            "causalidad sigue siendo una pregunta abierta.",
            font_size=26,
            width=60,
            color=MUTED,
        ).next_to(items, DOWN, buff=0.55)
        self.play(FadeIn(note, shift=UP * 0.2))

        self.next_slide()
        gap_text = body(
            "Adem\u00e1s, la literatura se concentra en clasificaci\u00f3n. "
            "En regresi\u00f3n sobre series temporales apenas hay m\u00e9todos: "
            "CounTS y ForecastCF.",
            font_size=30,
            width=48,
        ).shift(UP * 0.4)
        self.play(FadeOut(intro), FadeOut(items), FadeOut(note))
        self.play(Write(gap_text))

        self.next_slide()
        here = Text(
            "Ah\u00ed se sit\u00faa CFGTS", font_size=34, color=ACCENT, weight="BOLD"
        ).next_to(gap_text, DOWN, buff=0.8)
        self.play(FadeIn(here, shift=UP * 0.3))
