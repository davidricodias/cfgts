"""Slide 1/20: título."""

from __future__ import annotations

import numpy as np
from common import ACCENT, INK, MUTED, WARM, ThemedSlide, wrap
from manim import (
    DOWN,
    UP,
    Axes,
    Create,
    DashedVMobject,
    Dot,
    FadeIn,
    Text,
    Write,
)


def _observed(x: float) -> float:
    return float(np.sin(2.0 * x) + 0.40 * np.sin(5.0 * x + 1.0))


class TitleSlide(ThemedSlide):
    def construct(self) -> None:
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[-2.4, 2.4, 1],
            x_length=12.0,
            y_length=2.6,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": False},
        ).to_edge(DOWN, buff=0.7)

        observed = axes.plot(_observed, x_range=[0, 6.5], color=INK, stroke_width=4)
        branch = axes.plot(
            lambda x: _observed(x) - 0.55 * (x - 6.5),
            x_range=[6.5, 10],
            color=WARM,
            stroke_width=4,
        )
        split = Dot(axes.c2p(6.5, _observed(6.5)), color=WARM, radius=0.08)

        self.play(Create(axes), run_time=0.8)
        self.play(Create(observed), run_time=1)
        self.play(FadeIn(split, scale=0.5))
        self.play(Create(DashedVMobject(branch, num_dashes=26)), run_time=1)

        title = Text("CFGTS", font_size=84, color=ACCENT, weight="BOLD").shift(UP * 2.4)
        self.play(Write(title))

        subtitle = Text(
            wrap(
                "CounterFactual Generation for Time Series",
                70,
            ),
            font_size=28,
            color=INK,
        ).next_to(title, DOWN, buff=0.45)
        author = Text("José David Rico Dias", font_size=22, color=MUTED).next_to(
            subtitle, DOWN, buff=0.45
        )
        university = Text(
            "Grado en Ingeniería Informática — Universidad Carlos III de Madrid",
            font_size=16,
            color=MUTED,
        ).next_to(author, DOWN, buff=0.45)
        self.play(
            FadeIn(subtitle, shift=UP * 0.25),
            FadeIn(author, shift=UP * 0.25),
            FadeIn(university, shift=UP * 0.25),
        )
