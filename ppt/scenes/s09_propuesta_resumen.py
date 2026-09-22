"""Slide 10/20: propuesta · las tres fases de un vistazo."""

from __future__ import annotations

from common import ACCENT, GREEN, INK, MUTED, WARM, ThemedSlide, body, card, eq, reveal_card
from manim import (
    DOWN,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    Text,
    VGroup,
    Write,
)

PHASES = [
    (
        "Fase 1 · Candidatos",
        r"\min\ \big(J_1(\mathbf{x}'),\, J_2(\mathbf{x}')\big)",
        "TPE bi-objetivo sobre el hipercubo factible: el frente de Pareto es C0.",
        ACCENT,
    ),
    (
        "Fase 2 · Cobertura",
        r"\min\ \operatorname{MeanCov}(\mathcal{S})",
        "Discrepancia estelar mínima en el intervalo de cada salida: da el conjunto S.",
        WARM,
    ),
    (
        "Fase 3 · Evaluación",
        r"s_k = \tfrac{1}{D}\sum_d s_{k,d}",
        "DAG + puerta trasera sobre los candidatos y la cobertura: puntúa la consistencia causal.",
        GREEN,
    ),
]


class PropuestaResumenSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("CFGTS: las tres fases")

        inputs = eq(
            r"\langle \hat{f},\; \mathbf{x}_0,\; \mathbf{y}^{*},\; W,\;"
            r"r_{\min},\; r_{\max} \rangle",
            font_size=30,
        ).next_to(head, DOWN, buff=0.45)
        self.play(Write(inputs))

        self.next_slide()
        cards = VGroup(
            *[
                card(
                    title,
                    VGroup(
                        eq(tex, font_size=26, color=color),
                        body(text, font_size=20, width=30, color=INK),
                    ).arrange(DOWN, buff=0.3),
                    title_font_size=23,
                    title_color=color,
                    title_width=26,
                    frame_color=color,
                    gap=0.28,
                )
                for title, tex, text, color in PHASES
            ]
        ).arrange(RIGHT, buff=0.55, aligned_edge=UP)
        cards.scale_to_fit_width(12.6).next_to(inputs, DOWN, buff=0.75)

        arrows = VGroup(
            *[
                Arrow(
                    cards[i].get_right(),
                    cards[i + 1].get_left(),
                    buff=0.08,
                    color=MUTED,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.35,
                )
                for i in range(len(PHASES) - 1)
            ]
        )

        for index, phase_card in enumerate(cards):
            reveal_card(self, phase_card, frame_run_time=0.6, body_run_time=0.5)
            if index < len(arrows):
                self.play(Create(arrows[index]), run_time=0.4)
            self.next_slide()

        self.next_slide()
        output = eq(
            r"\mathcal{C} = \left\{\left(\mathbf{x}'_k,\; \hat{\mathbf{y}}'_k,\; s_k\right)"
            r"\right\}_{k=1}^{K}",
            font_size=32,
            color=ACCENT,
        ).next_to(cards, DOWN, buff=0.4)
        output_note = Text(
            "contrafactuales del frente de Pareto, con su predicción y su score causal",
            font_size=21,
            color=INK,
        ).next_to(output, DOWN, buff=0.22)
        self.play(Write(output))
        self.play(FadeIn(output_note, shift=UP * 0.15))
