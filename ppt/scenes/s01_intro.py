"""Slide 2/16: introducción."""

from __future__ import annotations

from common import ACCENT, INK, MUTED, WARM, ThemedSlide, body, eq
from manim import (
    DOWN,
    RIGHT,
    Arrow,
    Circumscribe,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Rectangle,
    ReplacementTransform,
    VGroup,
    Write,
)


class IntroSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Introducción")

        x0 = eq(r"\mathbf{x}_0", font_size=46)
        box = Rectangle(width=2.0, height=1.3, color=ACCENT, stroke_width=3)
        y0 = eq(r"\hat{\mathbf{y}}_0", font_size=46)
        row = VGroup(x0, box, y0).arrange(RIGHT, buff=1.6)

        fhat = eq(r"\hat{f}", font_size=46, color=ACCENT).move_to(box)
        a1 = Arrow(x0.get_right(), box.get_left(), buff=0.3, color=INK, stroke_width=4)
        a2 = Arrow(box.get_right(), y0.get_left(), buff=0.3, color=INK, stroke_width=4)
        diagram = VGroup(row, fhat, a1, a2).next_to(head, DOWN, buff=1.1)

        self.play(FadeIn(x0, shift=RIGHT * 0.4))
        self.play(Create(box), Write(fhat))
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(y0, shift=RIGHT * 0.4))

        self.next_slide()
        signature = eq(
            r"\hat{f}:\ \mathbb{R}^{n_{\mathrm{In}}} \to \mathbb{R}^{D} | n_{\mathrm{In}} = D \times T",
            font_size=32,
            color=MUTED,
        ).next_to(diagram, DOWN, buff=0.75)
        caption = body(
            "Los modelos predicen",
            font_size=28,
            width=52,
        ).next_to(signature, DOWN, buff=0.5)
        self.play(FadeIn(signature), Write(caption))

        self.next_slide()
        ystar = eq(r"\mathbf{y}^{*}", font_size=46, color=WARM).move_to(y0)
        question = body(
            "Pero nos preguntamos cómo obtener una salida distinta...",
            font_size=28,
            width=52,
        ).move_to(caption)
        self.play(FadeOut(signature), ReplacementTransform(y0, ystar))
        self.play(ReplacementTransform(caption, question))

        self.next_slide()
        xprime = eq(r"\mathbf{x}'", font_size=46, color=WARM).move_to(x0)
        ask = body(
            "...y qué entrada habría llevado al modelo hasta el nuevo objetivo",
            font_size=28,
            width=52,
        ).move_to(question)
        self.play(ReplacementTransform(x0, xprime))
        self.play(Circumscribe(xprime, color=WARM), ReplacementTransform(question, ask))

        self.next_slide()
        goal = eq(
            r"\hat{f}",
            r"(",
            r"\mathbf{x}'",
            r")",
            r"\approx",
            r"\mathbf{y}^{*}",
            r"\qquad",
            r"\|",
            r"\mathbf{x}'",
            r"- \mathbf{x}_0\|_2 \ \text{min}",
            font_size=38,
        ).move_to(ask)
        goal[0].set_color(ACCENT)  # \hat{f}
        goal[2].set_color(WARM)  # x'
        goal[4].set_color(ACCENT)  # \approx
        goal[5].set_color(WARM)  # y*
        goal[7].set_color(ACCENT)  # \|...\|_2 min
        goal[8].set_color(WARM)  # x'
        goal[9].set_color(ACCENT)  # - x_0\|_2 min
        self.play(FadeOut(ask), Write(goal))
