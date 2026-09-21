"""Slide 14/20: marco regulador."""

from __future__ import annotations

from common import ACCENT, INK, MUTED, ThemedSlide, body, card, reveal_card, wrap
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    FadeIn,
    Text,
    VGroup,
    Write,
)

BLOCKS = [
    (
        "Legislación",
        [
            "RGPD art. 22: derecho a una explicación significativa.",
            "AI Act (UE 2024/1689): transparencia en sistemas de alto riesgo.",
        ],
    ),
    (
        "Estándares",
        [
            "PEP 8 verificado con ruff.",
            "PEP 484 y PEP 561, validados con mypy.",
            "PEP 517/518/621 con hatchling.",
        ],
    ),
    (
        "Licencia",
        [
            "cfgts bajo CC BY-NC-ND 4.0.",
            "Dependencias con licencias permisivas: MIT, BSD, Apache 2.0.",
        ],
    ),
]


def _block(title: str, lines: list[str]) -> VGroup:
    items = VGroup(
        *[Text(wrap(line, 26), font_size=20, color=INK, line_spacing=1.1) for line in lines]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    return card(title, items, buff=0.32, gap=0.35)


class MarcoReguladorSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Marco regulador")

        note = body(
            "CFGTS no recopila ni procesa datos personales: recibe un modelo ajustado, "
            "una instancia y un objetivo.",
            font_size=26,
            width=64,
            color=MUTED,
        ).next_to(head, DOWN, buff=0.45)
        self.play(Write(note))

        self.next_slide()
        blocks = VGroup(*[_block(title, lines) for title, lines in BLOCKS])
        blocks.arrange(RIGHT, buff=0.55, aligned_edge=UP).next_to(note, DOWN, buff=0.6)

        for block in blocks:
            reveal_card(self, block, frame_run_time=0.7, body_run_time=0.7)
            self.next_slide()

        closing = Text(
            "Una explicación contrafactual es el mecanismo natural del art. 22",
            font_size=26,
            color=ACCENT,
            weight="BOLD",
        ).next_to(blocks, DOWN, buff=0.5)
        self.play(FadeIn(closing, shift=UP * 0.2))
