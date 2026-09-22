"""Slide 7/20: propuesta · fase 1 (generación de candidatos)."""

from __future__ import annotations

import numpy as np
from common import ACCENT, INK, MUTED, WARM, ThemedSlide, body, card, eq, reveal_card
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Text,
    VGroup,
    Write,
)

# Frente de Pareto del estudio bi-objetivo, en coordenadas normalizadas
# (J1, J2) in [0, 1]^2: menor error relativo cuesta mayor distancia.
FRONT = [(0.05, 0.95), (0.15, 0.62), (0.30, 0.45), (0.50, 0.30), (0.75, 0.18), (0.95, 0.10)]
# Candidatos dominados: para cada uno existe un punto del frente con J1 y J2 menores.
DOMINATED = [
    (0.25, 0.95),
    (0.30, 0.80),
    (0.45, 0.65),
    (0.50, 0.85),
    (0.60, 0.55),
    (0.70, 0.42),
    (0.85, 0.60),
    (0.90, 0.35),
]

PLOT_ORIGIN = np.array([-6.0, -3.2, 0.0])
PLOT_W = 5.0
PLOT_H = 3.4


def _plot_point(j1: float, j2: float) -> np.ndarray:
    return PLOT_ORIGIN + np.array([j1 * PLOT_W, j2 * PLOT_H, 0.0])


class PropuestaFase1Slide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Fase 1: candidatos contrafactuales")

        intro = body(
            "Optimización bi-objetivo (NSGA) sobre el hipercubo factible.",
            font_size=27,
            width=62,
        ).next_to(head, DOWN, buff=0.45)
        feasible = eq(
            r"\mathcal{F}(r_{\min}, r_{\max}) = [r_{\min},\, r_{\max}]^{n_{\mathrm{In}}}",
            font_size=32,
        ).next_to(intro, DOWN, buff=0.4)
        self.play(Write(intro))
        self.play(Write(feasible))

        self.next_slide()
        objectives = VGroup(
            card(
                "Error relativo de predicción",
                eq(
                    r"J_1(\mathbf{x}') = \sum_{k=0}^{D-1}"
                    r"\frac{\left|y^*_k - f_k(\mathbf{x}')\right|}{\left|y^*_k\right|}",
                    font_size=30,
                ),
                title_font_size=24,
                title_width=30,
                gap=0.3,
            ),
            card(
                "Distancia a la instancia original",
                eq(
                    r"J_2(\mathbf{x}') = \|\mathbf{x}_0 - \mathbf{x}'\|_2",
                    font_size=30,
                ),
                title_font_size=24,
                title_width=30,
                gap=0.3,
            ),
        ).arrange(RIGHT, buff=0.9, aligned_edge=UP)
        objectives.next_to(feasible, DOWN, buff=0.7)

        for objective in objectives:
            reveal_card(self, objective)
            self.next_slide()

        self.play(FadeOut(intro), FadeOut(feasible), FadeOut(objectives), run_time=0.6)

        # --- Frente de Pareto ---
        axis_x = Arrow(
            PLOT_ORIGIN + LEFT * 0.2,
            PLOT_ORIGIN + RIGHT * (PLOT_W + 0.5),
            buff=0,
            color=MUTED,
            stroke_width=3,
        )
        axis_y = Arrow(
            PLOT_ORIGIN + DOWN * 0.2,
            PLOT_ORIGIN + UP * (PLOT_H + 0.5),
            buff=0,
            color=MUTED,
            stroke_width=3,
        )
        label_x = eq(r"J_1", font_size=30, color=MUTED).next_to(axis_x.get_end(), DOWN, buff=0.2)
        label_y = eq(r"J_2", font_size=30, color=MUTED).next_to(axis_y.get_end(), RIGHT, buff=0.2)
        axes = VGroup(axis_x, axis_y, label_x, label_y)

        dominated_dots = VGroup(
            *[Dot(_plot_point(*p), radius=0.07, color=MUTED) for p in DOMINATED]
        )
        front_dots = VGroup(*[Dot(_plot_point(*p), radius=0.09, color=MUTED) for p in FRONT])
        front_curve = VGroup(
            *[
                DashedLine(
                    _plot_point(*FRONT[i]),
                    _plot_point(*FRONT[i + 1]),
                    color=ACCENT,
                    stroke_width=3,
                )
                for i in range(len(FRONT) - 1)
            ]
        )

        self.play(Create(axes), run_time=0.8)
        self.play(FadeIn(dominated_dots), FadeIn(front_dots), run_time=1.0)

        self.next_slide()
        dominance = card(
            "Dominancia de Pareto",
            eq(
                r"\mathbf{x}' \succ_P \mathbf{x}'' \iff"
                r"\begin{cases} J_1(\mathbf{x}') \leq J_1(\mathbf{x}'') \\"
                r"J_2(\mathbf{x}') \leq J_2(\mathbf{x}'') \\"
                r"\text{alguna estricta} \end{cases}",
                font_size=26,
            ),
            title_font_size=24,
        )
        dominance.to_edge(RIGHT, buff=0.7).shift(UP * 0.9)
        reveal_card(self, dominance)

        self.next_slide()
        self.play(
            *[dot.animate.set_color(ACCENT).scale(1.25) for dot in front_dots],
            *[dot.animate.set_opacity(0.35) for dot in dominated_dots],
            run_time=0.9,
        )
        self.play(Create(front_curve), run_time=1.0)

        front_label = Text("frente de Pareto", font_size=22, color=ACCENT)
        front_label.move_to(_plot_point(0.32, 0.10))
        self.play(Write(front_label))

        self.next_slide()
        outcome = eq(
            r"\mathcal{C}_0 = \mathcal{P} \subset \mathcal{F}(r_{\min}, r_{\max})",
            font_size=30,
            color=WARM,
        )
        outcome_label = Text(
            "el frente de Pareto es el conjunto de candidatos",
            font_size=21,
            color=WARM,
        )
        note = eq(
            r"\hat{\mathbf{y}}'_k = \hat{f}(\mathbf{x}'_k)"
            r"\quad \text{para cada candidato } \mathbf{x}'_k \in \mathcal{C}_0",
            font_size=26,
            color=INK,
        )
        closing = VGroup(outcome, outcome_label, note).arrange(DOWN, buff=0.28)
        closing.next_to(dominance, DOWN, buff=0.6)
        overflow = closing.get_right()[0] - 6.9
        if overflow > 0:
            closing.shift(LEFT * overflow)
        if closing.get_bottom()[1] < -3.7:
            closing.shift(UP * (-3.7 - closing.get_bottom()[1]))
        self.play(Write(outcome), Write(outcome_label))
        self.play(FadeIn(note, shift=UP * 0.2))
