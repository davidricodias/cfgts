"""Slide 3/16: las tres fases del algoritmo."""

from __future__ import annotations

from common import ACCENT, BG, INK, MUTED, ThemedSlide, eq, wrap
from manim import (
    DOWN,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    FadeIn,
    GrowArrow,
    SurroundingRectangle,
    Text,
    VGroup,
    Write,
)


def _card(number: str, title: str, tex: str) -> VGroup:
    disc = Circle(radius=0.30, color=ACCENT, fill_opacity=1.0, stroke_width=0)
    badge = Text(number, font_size=26, color=BG, weight="BOLD").move_to(disc)
    label = Text(wrap(title, 17), font_size=24, color=INK, weight="BOLD", line_spacing=1.1)
    formula = eq(tex, font_size=30)
    content = VGroup(VGroup(disc, badge), label, formula).arrange(DOWN, buff=0.35)
    frame = SurroundingRectangle(
        content, corner_radius=0.15, buff=0.35, color=MUTED, stroke_width=2
    )
    return VGroup(frame, content)


class PhasesSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Un algoritmo de tres fases")

        cards = VGroup(
            _card("1", "Generación de candidatos", r"\min_{\mathbf{x}'}\, (J_1,\, J_2)"),
            _card(
                "2", "Conjunto de cobertura", r"\min_{\mathcal{S}}\, \mathrm{MeanCov}(\mathcal{S})"
            ),
            _card("3", "Consistencia causal", r"s_k \in (0,\, 1]"),
        ).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        cards.next_to(head, DOWN, buff=0.7)

        arrows = VGroup(
            *[
                Arrow(
                    cards[i].get_right(),
                    cards[i + 1].get_left(),
                    buff=0.12,
                    color=MUTED,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.35,
                )
                for i in range(len(cards) - 1)
            ]
        )

        for index, card in enumerate(cards):
            frame, content = card
            badge, label, formula = content
            self.play(Create(frame), FadeIn(badge, scale=0.6), Write(label), run_time=1.0)
            self.play(Write(formula), run_time=0.8)
            if index < len(arrows):
                self.play(GrowArrow(arrows[index]), run_time=0.5)
            self.next_slide()

        objectives = VGroup(
            eq(r"J_1(\mathbf{x}') = \sum_{k=0}^{D-1} \frac{|y^*_k - f_k(\mathbf{x}')|}{|y^*_k|}"),
            eq(r"J_2(\mathbf{x}') = \|\mathbf{x}_0 - \mathbf{x}'\|_2"),
        ).arrange(RIGHT, buff=1.4)
        objectives.next_to(cards, DOWN, buff=0.7)
        self.play(FadeIn(objectives[0], shift=UP * 0.2))

        self.next_slide()
        self.play(FadeIn(objectives[1], shift=UP * 0.2))
