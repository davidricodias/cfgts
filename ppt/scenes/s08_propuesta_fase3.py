"""Slide 9/20: propuesta · fase 3 (evaluación causal)."""

from __future__ import annotations

import numpy as np
from common import ACCENT, GREEN, INK, MUTED, WARM, ThemedSlide, body, eq, fit_below
from manim import (
    DOWN,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    CurvedArrow,
    DashedLine,
    FadeIn,
    FadeOut,
    MathTex,
    Text,
    VGroup,
    Write,
)

NODE_RADIUS = 0.5  # igual que en el resto del deck (véase s03_fundamentos)

# Grafo desplegado de fig:dag_desplegado: 2 variables x 2 retardos + 2 salidas.
COL_X = {"lag2": -4.6, "lag1": -1.0, "out": 2.8}
ROW_Y = {"X": 0.9, "Y": -1.7}


def _node(label: str, x: float, y: float, *, highlight: bool = False) -> VGroup:
    color = ACCENT if highlight else INK
    circle = Circle(radius=NODE_RADIUS, color=color, stroke_width=4 if highlight else 3)
    if highlight:
        circle.set_fill(ACCENT, opacity=0.12)
    text = MathTex(label, font_size=26, color=INK)
    return VGroup(circle, text).move_to([x, y, 0])


def _edge(src: VGroup, dst: VGroup, *, color: str = ACCENT, dashed: bool = False, width: float = 3):
    """Arista dirigida entre dos nodos, recortada al borde de cada círculo."""
    start, end = src.get_center(), dst.get_center()
    unit = (end - start) / np.linalg.norm(end - start)
    start = start + unit * (NODE_RADIUS + 0.08)
    end = end - unit * (NODE_RADIUS + 0.08)
    if dashed:
        return DashedLine(start, end, color=color, stroke_width=width, dash_length=0.12).add_tip(
            tip_length=0.18
        )
    return Arrow(start, end, buff=0, color=color, stroke_width=width)


def _arc(src: VGroup, dst: VGroup, *, angle: float, color: str = ACCENT, width: float = 3):
    """Arista arqueada: ángulo negativo pasa por arriba, positivo por abajo."""
    if angle < 0:
        start, end = src.get_top(), dst.get_top()
    else:
        start, end = src.get_bottom(), dst.get_bottom()
    return CurvedArrow(start, end, angle=angle, color=color, stroke_width=width)


class PropuestaFase3Slide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Fase 3: evaluación causal")

        intro = body(
            "Sobre los candidatos y el conjunto de cobertura se construye el DAG "
            "y se estiman los efectos con el criterio de puerta trasera.",
            font_size=26,
            width=66,
        ).next_to(head, DOWN, buff=0.4)
        self.play(Write(intro))

        # --- Grafo causal desplegado en el tiempo ---
        x2 = _node("X_{t-2}", COL_X["lag2"], ROW_Y["X"])
        y2 = _node("Y_{t-2}", COL_X["lag2"], ROW_Y["Y"])
        x1 = _node("X_{t-1}", COL_X["lag1"], ROW_Y["X"])
        y1 = _node("Y_{t-1}", COL_X["lag1"], ROW_Y["Y"])
        xt = _node("X_t", COL_X["out"], ROW_Y["X"], highlight=True)
        yt = _node("Y_t", COL_X["out"], ROW_Y["Y"], highlight=True)
        nodes = VGroup(x2, y2, x1, y1, xt, yt)

        # Regla (a): toda entrada apunta a toda salida (8 aristas). Las dos
        # aristas de retardo 2 hacia su propia variable se arquean para no
        # atravesar el nodo de retardo 1 que queda en medio.
        rule_a = VGroup(
            *[_edge(src, dst) for src in (x1, y1) for dst in (xt, yt)],
            _edge(x2, yt),
            _edge(y2, xt),
            _arc(x2, xt, angle=-0.45),
            _arc(y2, yt, angle=0.45),
        )
        # Regla (b): mayor retardo -> menor retardo (4 aristas temporales).
        rule_b = VGroup(
            *[_edge(src, dst, color=MUTED, dashed=True, width=2.5) for src in (x2, y2) for dst in (x1, y1)]
        )

        self.next_slide()
        self.play(FadeOut(intro), FadeIn(nodes), run_time=0.8)

        legend_a = Text("(a) cada entrada → cada salida", font_size=22, color=ACCENT)
        legend_b = Text("(b) retardo mayor → retardo menor", font_size=22, color=MUTED)
        legend = VGroup(legend_a, legend_b).arrange(RIGHT, buff=0.9)
        legend.next_to(VGroup(nodes, rule_a), DOWN, buff=0.35)

        self.play(Create(rule_a), Write(legend_a), run_time=1.4)
        self.next_slide()
        self.play(Create(rule_b), Write(legend_b), run_time=1.2)

        graph = VGroup(nodes, rule_a, rule_b, legend)

        self.next_slide()
        self.play(FadeOut(graph), run_time=0.6)

        # --- Efecto total vs efecto directo (fig:efecto_total_h2 / fig:mco_bloqueo) ---
        z2 = _node(r"\mathbf{Z}_{t-2}", -4.2, 1.1)
        z1 = _node(r"\mathbf{Z}_{t-1}", -0.4, 1.1)
        z0 = _node(r"\mathbf{Z}_{t}", 3.4, 1.1)
        chain = VGroup(z2, z1, z0)

        mediated_1 = _edge(z2, z1, color=MUTED, dashed=True)
        mediated_2 = _edge(z1, z0, color=MUTED, dashed=True)
        direct = CurvedArrow(
            z2.get_bottom() + DOWN * 0.05, z0.get_bottom() + DOWN * 0.05, angle=1.0, color=ACCENT, stroke_width=4
        )
        label_m1 = eq("A_1", font_size=26, color=MUTED).next_to(mediated_1, UP, buff=0.12)
        label_m2 = eq("A_1", font_size=26, color=MUTED).next_to(mediated_2, UP, buff=0.12)
        label_direct = eq("A_2", font_size=26, color=ACCENT).next_to(direct, DOWN, buff=0.1)

        self.play(FadeIn(chain), run_time=0.6)
        self.play(Create(direct), Write(label_direct))
        self.play(Create(mediated_1), Create(mediated_2), Write(label_m1), Write(label_m2))

        decomposition = eq(
            r"\mathbf{T}^{(2)} = \underbrace{A_2}_{\text{directo}}"
            r"+ \underbrace{A_1^2}_{\text{mediado}}",
            font_size=32,
        )
        fit_below(decomposition, direct, buff=0.45, bottom=-1.9)
        self.next_slide()
        self.play(Write(decomposition))

        # MCO condiciona sobre el mediador y bloquea la ruta mediada.
        self.next_slide()
        blocked = Text("MCO condiciona sobre el mediador", font_size=24, color=WARM)
        blocked.next_to(z1, UP, buff=0.55)
        self.play(
            z1[0].animate.set_fill(MUTED, opacity=0.45),
            mediated_1.animate.set_opacity(0.2),
            mediated_2.animate.set_opacity(0.2),
            label_m1.animate.set_opacity(0.2),
            label_m2.animate.set_opacity(0.2),
            Write(blocked),
            run_time=1.0,
        )
        bias = eq(
            r"\mathbf{B}_{\mathrm{MCO}}^{(2)} = \mathbf{D}^{(2)} - \mathbf{T}^{(2)} = -A_1^2",
            font_size=30,
            color=WARM,
        ).next_to(decomposition, DOWN, buff=0.4)
        self.play(Write(bias))

        mediation = VGroup(
            chain, direct, mediated_1, mediated_2, label_direct, label_m1, label_m2, blocked, decomposition, bias
        )

        self.next_slide()
        self.play(FadeOut(mediation), run_time=0.6)

        # --- Puntuación de consistencia causal ---
        deltas = eq(
            r"\Delta y_d^{\mathrm{esp}} = \sum_i \widehat{\beta}_i^{(d)} (x'_i - x_i),",
            r"\qquad \Delta y_d^{\mathrm{real}} = f_d(\mathbf{x}') - f_d(\mathbf{x})",
            font_size=30,
        ).next_to(head, DOWN, buff=0.7)
        score = eq(
            r"s_d(\mathbf{x}') = 1 - \frac{\left|\Delta y_d^{\mathrm{esp}}"
            r"- \Delta y_d^{\mathrm{real}}\right|}{\left|\Delta y_d^{\mathrm{esp}}\right|"
            r"+ \left|\Delta y_d^{\mathrm{real}}\right| + \varepsilon}"
            r"\;\in\; (0, 1]",
            font_size=32,
        ).next_to(deltas, DOWN, buff=0.55)
        mean_score = eq(
            r"s(\mathbf{x}') = \frac{1}{D}\sum_{d=0}^{D-1} s_d(\mathbf{x}')",
            font_size=32,
            color=ACCENT,
        ).next_to(score, DOWN, buff=0.55)

        self.play(Write(deltas))
        self.next_slide()
        self.play(Write(score))
        self.next_slide()
        self.play(Write(mean_score))

        self.next_slide()
        dominance = eq(
            r"s\!\left(\mathbf{x}'; \widehat{\boldsymbol{\beta}}_{\mathrm{mco}}\right)",
            r"\;\leq\;",
            r"s\!\left(\mathbf{x}'; \widehat{\boldsymbol{\beta}}_{\mathrm{causal}}\right)",
            font_size=32,
            color=GREEN,
        ).next_to(mean_score, DOWN, buff=0.6)
        dominance_note = Text(
            "el DAG domina débilmente a la regresión ingenua",
            font_size=23,
            color=GREEN,
        ).next_to(dominance, DOWN, buff=0.25)
        self.play(Write(dominance))
        self.play(FadeIn(dominance_note, shift=UP * 0.15))
