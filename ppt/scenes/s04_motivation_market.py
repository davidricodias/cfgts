"""Slide 5/16: motivación (microestructura de mercados)."""

from __future__ import annotations

import numpy as np
from common import GREEN, INK, WARM, ThemedSlide, body
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    LaggedStart,
    Rectangle,
    Text,
    VGroup,
    Write,
)

ASKS = [(100.1, 0.6), (100.2, 0.9), (100.3, 1.5)]
BIDS = [(99.9, 1.2), (99.8, 1.9), (99.7, 0.8)]

ROW_HEIGHT = 0.34
ROW_STEP = 0.44
LABEL_GAP = 0.85


def _rows(levels, color, sign):
    """sign=+1 stacks upward with bars to the right, -1 downward to the left."""
    bars, labels = VGroup(), VGroup()
    for index, (price, volume) in enumerate(levels):
        y = sign * (0.5 + index * ROW_STEP)
        bar = Rectangle(
            width=volume * 1.7,
            height=ROW_HEIGHT,
            color=color,
            fill_opacity=0.75,
            stroke_width=0,
        )
        bar.move_to(np.array([sign * (LABEL_GAP + bar.width / 2), y, 0.0]))
        bars.add(bar)
        labels.add(Text(f"{price:.1f}", font_size=20, color=INK).move_to(np.array([0.0, y, 0.0])))
    return bars, labels


class MotivationMarketSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Motivaci\u00f3n \u00b7 Microestructura de mercados")

        ask_bars, ask_labels = _rows(ASKS, WARM, +1)
        bid_bars, bid_labels = _rows(BIDS, GREEN, -1)
        mid = DashedLine(LEFT * 5.0, RIGHT * 5.0, color=INK, stroke_width=2)

        ask_tag = Text("ventas", font_size=22, color=WARM).next_to(ask_bars, UP, buff=0.3)
        bid_tag = Text("compras", font_size=22, color=GREEN).next_to(bid_bars, DOWN, buff=0.3)

        market = VGroup(ask_bars, ask_labels, bid_bars, bid_labels, mid, ask_tag, bid_tag)
        market.next_to(head, DOWN, buff=0.55)

        self.play(Create(mid), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(bar, shift=RIGHT * 0.3) for bar in ask_bars], lag_ratio=0.2),
            LaggedStart(*[FadeIn(bar, shift=LEFT * 0.3) for bar in bid_bars], lag_ratio=0.2),
            FadeIn(ask_labels),
            FadeIn(bid_labels),
            run_time=1.4,
        )
        self.play(FadeIn(ask_tag), FadeIn(bid_tag))

        self.next_slide()
        caption = body(
            "El libro de \u00f3rdenes: precios, vol\u00famenes y agentes en competencia.",
            font_size=28,
            width=54,
        ).to_edge(DOWN, buff=0.85)
        self.play(Write(caption))

        self.next_slide()
        # A large buy order eats the two best asks and drags the mid price up.
        self.play(
            FadeOut(ask_bars[0], shift=RIGHT * 0.6),
            FadeOut(ask_labels[0], shift=RIGHT * 0.6),
            FadeOut(ask_bars[1], shift=RIGHT * 0.6),
            FadeOut(ask_labels[1], shift=RIGHT * 0.6),
            run_time=0.9,
        )
        self.play(mid.animate.shift(UP * 2 * ROW_STEP), run_time=0.8)

        self.next_slide()
        question = body(
            "\u00bfEn qu\u00e9 estado tendr\u00eda que haber estado el libro "
            "para que el precio no cambiase?",
            font_size=28,
            width=54,
        ).move_to(caption)
        self.play(FadeOut(caption), Write(question))
