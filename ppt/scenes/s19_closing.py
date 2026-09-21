"""Slide 20/20: cierre."""

from __future__ import annotations

from common import ACCENT, INK, ThemedSlide, wrap
from manim import DOWN, UP, FadeIn, RoundedRectangle, Text, VGroup, Write


class ClosingSlide(ThemedSlide):
    def construct(self) -> None:
        statement = Text(
            wrap(
                "Buenas explicaciones contrafactuales son plausibles, aumentan la "
                "confianza en el modelo y amplían nuestro conocimiento del "
                "fenómeno modelado.",
                44,
            ),
            font_size=32,
            color=INK,
            line_spacing=1.25,
            t2c={"plausibles": ACCENT, "confianza": ACCENT, "conocimiento": ACCENT},
        ).shift(UP * 1.0)

        self.play(Write(statement), run_time=3.0)

        self.next_slide()
        thanks = Text("Gracias", font_size=44, color=ACCENT, weight="BOLD").next_to(
            statement, DOWN, buff=0.8
        )
        self.play(FadeIn(thanks, shift=UP * 0.3))

        snippet_text = Text(
            "$ pip install cfgts",
            font="Monospace",
            font_size=18,
            color="#F2F4FF",
        )
        snippet_box = RoundedRectangle(
            corner_radius=0.12,
            width=snippet_text.width + 0.8,
            height=snippet_text.height + 0.6,
            fill_color=INK,
            fill_opacity=1.0,
            stroke_color=ACCENT,
            stroke_width=2,
        )
        snippet = VGroup(snippet_box, snippet_text).next_to(thanks, DOWN, buff=0.7)
        self.play(FadeIn(snippet, shift=UP * 0.3))
