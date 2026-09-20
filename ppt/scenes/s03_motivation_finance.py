"""Slide 4/16: motivación (finanzas)."""

from __future__ import annotations

from common import ACCENT, GREEN, MUTED, WARM, ThemedSlide, body
from manim import (
    DOWN,
    UP,
    Arrow,
    Axes,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Flash,
    GrowArrow,
    Text,
    Write,
)

RETURNS = [0.4, -0.8, 1.2, 0.3, -1.5, 0.9, 1.8, -0.4, 1.1, -2.1]


class MotivationFinanceSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Motivaci\u00f3n \u00b7 Finanzas")

        axes = Axes(
            x_range=[0, 11, 1],
            y_range=[-3, 3, 1],
            x_length=9.5,
            y_length=3.2,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": False},
        ).next_to(head, DOWN, buff=0.6)

        zero = DashedLine(axes.c2p(0, 0), axes.c2p(11, 0), color=MUTED, stroke_width=2)
        graph = axes.plot_line_graph(
            x_values=list(range(1, len(RETURNS) + 1)),
            y_values=RETURNS,
            line_color=ACCENT,
            vertex_dot_radius=0.05,
            vertex_dot_style={"color": ACCENT},
            stroke_width=4,
        )
        caption = body(
            "Movimiento diario de un portfolio de deuda.", font_size=28, width=52
        ).next_to(axes, DOWN, buff=0.5)

        self.play(Create(axes), Create(zero), run_time=0.9)
        self.play(Create(graph), run_time=2.0)
        self.play(Write(caption))

        self.next_slide()
        last_x = len(RETURNS)
        today = Dot(axes.c2p(last_x, RETURNS[-1]), color=WARM, radius=0.10)
        today_label = Text("ayer", font_size=24, color=WARM).next_to(today, DOWN, buff=0.2)
        self.play(FadeIn(today, scale=0.5), Flash(today, color=WARM, line_length=0.25))
        self.play(Write(today_label))

        self.next_slide()
        target = Dot(axes.c2p(last_x, 0), color=GREEN, radius=0.10)
        lift = Arrow(
            axes.c2p(last_x, RETURNS[-1]),
            axes.c2p(last_x, 0),
            buff=0.1,
            color=GREEN,
            stroke_width=4,
        )
        question = body(
            "\u00bfQu\u00e9 portfolio habr\u00eda producido un movimiento cero?",
            font_size=28,
            width=52,
        ).move_to(caption)
        self.play(FadeOut(caption), GrowArrow(lift), FadeIn(target, scale=0.5))
        self.play(Write(question))

        self.next_slide()
        note = body(
            "Los instrumentos de deuda presentan autocorrelaci\u00f3n y correlaci\u00f3n cruzada: "
            "no se puede mover una pata sin mover las dem\u00e1s.",
            font_size=26,
            width=60,
            color=MUTED,
        ).next_to(question, DOWN, buff=0.35)
        self.play(FadeIn(note, shift=UP * 0.2))
