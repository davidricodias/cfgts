"""Slide 6/16: fundamentos teóricos."""

from __future__ import annotations

from common import ACCENT, GREEN, INK, MUTED, WARM, ThemedSlide, body, card, eq, fit_below, reveal_card
from manim import (
    DOWN,
    UP,
    Arrow,
    Circle,
    Create,
    CurvedArrow,
    DashedVMobject,
    FadeIn,
    FadeOut,
    MathTex,
    Text,
    VGroup,
    Write,
)

PILLARS = [
    ("Estadística", r"y_t = \beta_0 + \beta_1 x_t + \varepsilon_t"),
    ("Series temporales", r"X_t = \phi_1 X_{t-1} + \phi_2 X_{t-2} + \varepsilon_t"),
    ("Causalidad pearliana", r"\mathbb{P}\left(C \mid do(P = p)\right)"),
    ("Explicabilidad en IA", r"g \approx \hat{f} \quad \text{(LIME)}"),
]

NODE_RADIUS = 0.55  # fixed so every DAG node in the deck matches in size


def _node(label: str, *, x: float, y: float, color: str = INK, exogenous: bool = False):
    """A circular DAG node, mirroring the tikz `draw, circle` style used in report.tex."""
    text = MathTex(label, font_size=30, color=color)
    circle = Circle(radius=NODE_RADIUS, color=color, stroke_width=3)
    if exogenous:
        circle = DashedVMobject(circle, num_dashes=14)
    node = VGroup(circle, text).move_to([x, y, 0])
    return node


class FundamentosSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Fundamentos teóricos")

        PAD = 0.6  # uniform frame padding so every pillar card matches in size

        def _pillar_card(width: float | None = None, height: float | None = None) -> list:
            return [
                card(title, eq(tex, font_size=28), title_font_size=25, gap=0.28, width=width, height=height)
                for title, tex in PILLARS
            ]

        box_width = max(c[1].width for c in _pillar_card()) + PAD
        box_height = max(c[1].height for c in _pillar_card()) + PAD
        grid = VGroup(*_pillar_card(box_width, box_height))
        grid.arrange_in_grid(rows=2, cols=2, buff=(0.7, 0.6))
        grid.next_to(head, DOWN, buff=0.8)

        for pillar_card in grid:
            reveal_card(self, pillar_card, frame_run_time=0.7, body_run_time=0.6, body_shift=UP * 0.15)
            self.next_slide()

        self.play(FadeOut(grid), run_time=0.6)

        # --- Grafo causal (fig:dag_conversion_publicidad de report.tex) ---
        self.next_slide()
        dag_intro = body(
            "Un DAG hace explícito un factor de confusión: la edad (A) afecta "
            "tanto a la publicidad (P) como a la conversión (C).",
            font_size=27,
            width=58,
        ).next_to(head, DOWN, buff=0.55)

        node_a = _node("A", x=-3.4, y=-0.6)
        node_p = _node("P", x=0, y=-0.6)
        node_c = _node("C", x=3.4, y=-0.6)

        edge_ap = Arrow(
            node_a.get_right(), node_p.get_left(), buff=0.1, color=INK, stroke_width=3
        )
        edge_pc = Arrow(
            node_p.get_right(), node_c.get_left(), buff=0.1, color=INK, stroke_width=3
        )
        edge_ac = CurvedArrow(
            node_a.get_top(), node_c.get_top(), angle=-1.1, color=WARM, stroke_width=3
        )
        confounder_label = Text(
            "factor de confusión: P \u2190 A \u2192 C", font_size=24, color=WARM
        )

        dag = VGroup(node_a, node_p, node_c, edge_ap, edge_pc, edge_ac)
        dag_block = VGroup(dag, confounder_label).arrange(DOWN, buff=0.5)
        fit_below(dag_block, dag_intro, buff=0.7, bottom=-3.5)

        self.play(Write(dag_intro))
        self.play(FadeIn(node_a), FadeIn(node_p), FadeIn(node_c))
        self.play(Create(edge_ap), Create(edge_pc))
        self.next_slide()
        self.play(Create(edge_ac), Write(confounder_label))

        self.next_slide()
        self.play(FadeOut(dag_intro), FadeOut(dag), FadeOut(confounder_label))

        # --- Grafo de series temporales (fig:ts_graph_var de report.tex) ---
        bridge = body(
            "Series temporales y causalidad se encuentran en el grafo desplegado "
            "en el tiempo: el efecto de un retardo es la suma de todos los caminos "
            "dirigidos que lo conectan con el presente.",
            font_size=27,
            width=58,
        ).next_to(head, DOWN, buff=0.55)
        self.play(Write(bridge))

        x2 = _node("X_{t-2}", x=-4.2, y=1.2, color=INK)
        x1 = _node("X_{t-1}", x=-1.0, y=1.2, color=INK)
        xt = _node("X_t", x=2.2, y=1.2, color=ACCENT)
        y2 = _node("Y_{t-2}", x=-4.2, y=-0.7, color=INK)
        y1 = _node("Y_{t-1}", x=-1.0, y=-0.7, color=INK)
        yt = _node("Y_t", x=2.2, y=-0.7, color=GREEN)

        auto_x1 = Arrow(x2.get_right(), x1.get_left(), buff=0.1, color=INK, stroke_width=3)
        auto_x2 = Arrow(x1.get_right(), xt.get_left(), buff=0.1, color=ACCENT, stroke_width=3)
        auto_y1 = Arrow(y2.get_right(), y1.get_left(), buff=0.1, color=INK, stroke_width=3)
        auto_y2 = Arrow(y1.get_right(), yt.get_left(), buff=0.1, color=GREEN, stroke_width=3)
        cross_1 = Arrow(x1.get_bottom(), yt.get_top(), buff=0.15, color=MUTED, stroke_width=2.5)
        cross_2 = Arrow(y1.get_top(), xt.get_bottom(), buff=0.15, color=MUTED, stroke_width=2.5)
        # retardo 2 (autorregresion propia, arqueadas como en fig:ts_graph_var)
        lag2_x = CurvedArrow(x2.get_top(), xt.get_top(), angle=-1.0, color=ACCENT, stroke_width=2.5)
        lag2_y = CurvedArrow(y2.get_bottom(), yt.get_bottom(), angle=1.0, color=GREEN, stroke_width=2.5)

        ts_graph = VGroup(
            x2, x1, xt, y2, y1, yt,
            auto_x1, auto_x2, auto_y1, auto_y2, cross_1, cross_2, lag2_x, lag2_y,
        )

        effect = eq(
            r"\frac{\partial\, \mathbb{E}\!\left[Z^u_t \mid do(Z^v_{t-\tau})\right]}"
            r"{\partial\, Z^v_{t-\tau}} \;=\; "
            r"\sum_{\pi\,:\,Z^v_{t-\tau} \rightsquigarrow Z^u_t}\ \prod_{e \in \pi} [A_{\tau(e)}]_e",
            font_size=32,
        )

        block = VGroup(ts_graph, effect).arrange(DOWN, buff=0.45)
        fit_below(block, bridge, buff=0.6, bottom=-3.5)

        self.next_slide()
        self.play(FadeIn(x2), FadeIn(x1), FadeIn(xt), FadeIn(y2), FadeIn(y1), FadeIn(yt))
        self.play(
            Create(auto_x1),
            Create(auto_x2),
            Create(auto_y1),
            Create(auto_y2),
        )
        self.play(Create(cross_1), Create(cross_2))
        self.play(Create(lag2_x), Create(lag2_y))

        self.next_slide()
        self.play(Write(effect), run_time=2.0)

