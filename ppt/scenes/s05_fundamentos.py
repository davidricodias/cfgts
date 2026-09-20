"""Slide 6/16: fundamentos teóricos."""

from __future__ import annotations

from common import ACCENT, MUTED, ThemedSlide, body, eq
from manim import (
    DOWN,
    UP,
    Create,
    FadeIn,
    FadeOut,
    SurroundingRectangle,
    Text,
    VGroup,
    Write,
)

PILLARS = [
    ("Estad\u00edstica", r"y_t = \beta_0 + \beta_1 x_t + \varepsilon_t"),
    ("Series temporales", r"X_t = \phi_1 X_{t-1} + \phi_2 X_{t-2} + \varepsilon_t"),
    ("Causalidad pearliana", r"\mathbb{P}\left(C \mid do(P = p)\right)"),
    ("Explicabilidad en IA", r"g \approx \hat{f} \quad \text{(LIME)}"),
]


def _pillar(title: str, tex: str) -> VGroup:
    label = Text(title, font_size=25, color=ACCENT, weight="BOLD")
    formula = eq(tex, font_size=28)
    content = VGroup(label, formula).arrange(DOWN, buff=0.28)
    frame = SurroundingRectangle(content, corner_radius=0.12, buff=0.3, color=MUTED, stroke_width=2)
    return VGroup(frame, content)


class FundamentosSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Fundamentos te\u00f3ricos")

        grid = VGroup(*[_pillar(title, tex) for title, tex in PILLARS])
        grid.arrange_in_grid(rows=2, cols=2, buff=(0.7, 0.6))
        grid.next_to(head, DOWN, buff=0.8)

        for card in grid:
            frame, content = card
            self.play(Create(frame), Write(content[0]), run_time=0.7)
            self.play(FadeIn(content[1], shift=UP * 0.15), run_time=0.6)
            self.next_slide()

        bridge = body(
            "Series temporales y causalidad se encuentran en el grafo desplegado "
            "en el tiempo: el efecto de un retardo es la suma de todos los caminos "
            "dirigidos que lo conectan con el presente.",
            font_size=28,
            width=58,
        ).shift(UP * 1.3)
        effect = eq(
            r"\frac{\partial\, \mathbb{E}\!\left[Z^u_t \mid do(Z^v_{t-\tau})\right]}"
            r"{\partial\, Z^v_{t-\tau}} \;=\; "
            r"\sum_{\pi\,:\,Z^v_{t-\tau} \rightsquigarrow Z^u_t}\ \prod_{e \in \pi} [A_{\tau(e)}]_e",
            font_size=36,
        ).next_to(bridge, DOWN, buff=0.9)

        self.play(FadeOut(grid), run_time=0.6)
        self.play(Write(bridge))

        self.next_slide()
        self.play(Write(effect), run_time=2.0)
