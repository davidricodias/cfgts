"""Slide 3/20: motivación (finanzas)."""

from __future__ import annotations

from common import ACCENT, GREEN, MUTED, WARM, ThemedSlide, body
from manim import (
    DOWN,
    RIGHT,
    UP,
    AnimationGroup,
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
    Transform,
    Write,
)

# "Portfolio" return per day: the mean across instruments. Each instrument
# deviates from it by BASE_OFFSETS[i] * SCALES[t] (offsets sum to zero, so
# the portfolio mean is exactly RETURNS regardless of the per-day scale).
RETURNS = [0.4, -0.8, 1.2, 0.3, -1.5, 0.9, 1.8, -0.4, 1.1, -2.1]
BASE_OFFSETS = [1.0, -1.0, 0.6, -0.6]
SCALES = [0.6, 0.9, 0.4, 1.1, 0.7, 1.3, 0.5, 0.8, 1.0, 0.6]
INSTRUMENT_COLORS = [ACCENT, "#7A3FA0", "#0E8F8F", "#B0862E"]

# Counterfactual: history (days 1-5) is unchanged, but from day 6 onward the
# portfolio follows a different path (own offsets too, still summing to
# zero) that lands on a zero move on the last day, so the whole tail of the
# lines looks like a distinct series rather than a single shifted point.
DIVERGE_AT = 5
RETURNS_CF = RETURNS[:DIVERGE_AT] + [-0.6, 1.5, -0.9, 0.7, 0.0]
OFFSETS_CF = [0.9, 0.4, -0.6, -0.7]


def instrument_series(
    base_returns: list[float],
    diverge_at: int = len(RETURNS),
    offsets_after: list[float] = BASE_OFFSETS,
) -> list[list[float]]:
    return [
        [
            r + (offset if t < diverge_at else offsets_after[i]) * scale
            for t, (r, scale) in enumerate(zip(base_returns, SCALES))
        ]
        for i, offset in enumerate(BASE_OFFSETS)
    ]


INSTRUMENTS = instrument_series(RETURNS)
INSTRUMENTS_CF = instrument_series(RETURNS_CF, DIVERGE_AT, OFFSETS_CF)


class MotivationFinanceSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Motivación")

        axes = Axes(
            x_range=[0, 11, 1],
            y_range=[-3, 3, 1],
            x_length=9.5,
            y_length=2.9,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": False},
        ).next_to(head, DOWN, buff=0.45)

        zero = DashedLine(axes.c2p(0, 0), axes.c2p(11, 0), color=MUTED, stroke_width=2)
        x_values = list(range(1, len(RETURNS) + 1))
        graphs = [
            axes.plot_line_graph(
                x_values=x_values,
                y_values=values,
                line_color=color,
                vertex_dot_radius=0.045,
                vertex_dot_style={"color": color},
                stroke_width=3,
            )
            for values, color in zip(INSTRUMENTS, INSTRUMENT_COLORS)
        ]
        caption = body(
            "Movimiento diario de los instrumentos de un portfolio de deuda.",
            font_size=28,
            width=52,
        ).next_to(axes, DOWN, buff=0.4)

        self.play(Create(axes), Create(zero), run_time=0.5)
        self.play(
            AnimationGroup(*(Create(g) for g in graphs), lag_ratio=0.15),
            run_time=3.0,
        )
        self.play(Write(caption))

        self.next_slide()
        last_x = len(RETURNS)
        today = Dot(axes.c2p(last_x, RETURNS[-1]), color=WARM, radius=0.10)
        today_label = Text("ayer", font_size=24, color=WARM).next_to(today, RIGHT, buff=0.2)
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
            "¿Qué movimientos anteriores habrían producido un movimiento cero?",
            font_size=28,
            width=52,
        ).move_to(caption)
        cf_graphs = [
            axes.plot_line_graph(
                x_values=x_values,
                y_values=values,
                line_color=color,
                vertex_dot_radius=0.045,
                vertex_dot_style={"color": color},
                stroke_width=3,
            )
            for values, color in zip(INSTRUMENTS_CF, INSTRUMENT_COLORS)
        ]
        self.play(
            FadeOut(caption),
            GrowArrow(lift),
            FadeIn(target, scale=0.5),
            *(Transform(g, cf_g) for g, cf_g in zip(graphs, cf_graphs)),
        )
        self.play(Write(question))

        self.next_slide()
        note = body(
            "Los instrumentos de deuda presentan autocorrelación y correlación cruzada: "
            "no se puede modificar el riesgo de un portfolio cambiando un único instrumento.",
            font_size=24,
            width=78,
            color=MUTED,
        ).next_to(question, DOWN, buff=0.3)
        self.play(FadeIn(note, shift=UP * 0.2))
