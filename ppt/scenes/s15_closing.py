"""Slide 16/16: cierre."""

from __future__ import annotations

from common import ACCENT, INK, ThemedSlide, wrap
from manim import DOWN, UP, FadeIn, Text, Write


class ClosingSlide(ThemedSlide):
    def construct(self) -> None:
        statement = Text(
            wrap(
                "Buenas explicaciones contrafactuales son plausibles, aumentan la "
                "confianza en el modelo y ampl\u00edan nuestro conocimiento del "
                "fen\u00f3meno modelado.",
                44,
            ),
            font_size=32,
            color=INK,
            line_spacing=1.25,
            t2c={"plausibles": ACCENT, "confianza": ACCENT, "conocimiento": ACCENT},
        ).shift(UP * 0.6)

        self.play(Write(statement), run_time=3.0)

        self.next_slide()
        thanks = Text("Gracias", font_size=44, color=ACCENT, weight="BOLD").next_to(
            statement, DOWN, buff=1.0
        )
        self.play(FadeIn(thanks, shift=UP * 0.3))
