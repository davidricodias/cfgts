"""Slide 12/20: ejemplo de uso y validación con tests."""

from __future__ import annotations

from common import ACCENT, GREEN, INK, MUTED, WARM, ThemedSlide, body, eq, marker_item
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Code,
    Create,
    FadeIn,
    FadeOut,
    Text,
    VGroup,
    Write,
)

USAGE = """model = MultiOutputRegressor(LinearRegression())
model.fit(X, y)   # lags -> X_t, Y_t

instance = DataFrame({
    "X_t-1": [2], "X_t-2": [1],
    "Y_t-1": [4], "Y_t-2": [3],
})
target = DataFrame({"X_t": [5], "Y_t": [7]})

cfgts = CFGTS(
    model=model,
    instance=instance,
    counterfactual_value=target,
    whitelist=["X_t-1", "Y_t-1"],
    timeout=30,
)
cfgts.run()
print(cfgts.counterfactuals)
"""

RESULT_SCHEMA = [
    ("X_t-1, X_t-2, Y_t-1, Y_t-2", "el contrafactual: una fila por punto del frente", INK),
    ("X_t, Y_t", "la predicción del modelo para ese contrafactual", INK),
    ("score", "consistencia causal media, entre 0 y 1", GREEN),
]


def _check_item(text: str) -> VGroup:
    return marker_item(
        Text("\u2713", font_size=24, color=GREEN), text, font_size=21, width=52, buff=0.25
    )


def _schema_row(name: str, meaning: str, color: str) -> VGroup:
    return VGroup(
        Text(name, font_size=18, color=color, weight="BOLD"),
        body(meaning, font_size=18, width=34, color=MUTED),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)


class EjemploUsoSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Ejemplo de uso")

        snippet = Code(
            code_string=USAGE,
            language="python",
            add_line_numbers=False,
            background="rectangle",
            formatter_style="friendly",
            paragraph_config={"font": "monospace", "font_size": 15, "line_spacing": 0.55},
        )
        snippet.scale_to_fit_width(6.8)
        if snippet.height > 5.4:
            snippet.scale_to_fit_height(5.4)
        snippet.to_edge(LEFT, buff=0.6).shift(DOWN * 0.5)
        self.play(FadeIn(snippet, shift=UP * 0.2), run_time=1.0)

        self.next_slide()
        problem = VGroup(
            Text("instancia y objetivo", font_size=21, color=MUTED),
            eq(
                r"\mathbf{x}_0 = (2, 1, 4, 3) \;\Rightarrow\;"
                r"\hat{\mathbf{y}}_0 = (3, 5)",
                font_size=24,
            ),
            eq(
                r"\mathbf{y}^{*} = (5, 7), \quad W = \{X_{t-1}, Y_{t-1}\}", font_size=24, color=WARM
            ),
        ).arrange(DOWN, buff=0.22)
        problem.next_to(head, DOWN, buff=0.45).set_x(4.0)
        self.play(Write(problem))

        self.next_slide()
        arrow = Arrow(
            problem.get_bottom(),
            problem.get_bottom() + DOWN * 0.7,
            buff=0.05,
            color=MUTED,
            stroke_width=3,
        )
        table = VGroup(*[_schema_row(*row) for row in RESULT_SCHEMA]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25
        )
        caption = Text("cfgts.counterfactuals: DataFrame de Polars", font_size=20, color=ACCENT)
        result = VGroup(caption, table).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        result.next_to(arrow, DOWN, buff=0.3)
        self.play(Create(arrow))
        self.play(FadeIn(result, shift=UP * 0.2), run_time=1.0)

        self.next_slide()
        highlight = body(
            "Solo cambian los retardos de la whitelist; el frente de Pareto "
            "ofrece el compromiso entre alcanzar el objetivo y no alejarse.",
            font_size=21,
            width=44,
            color=INK,
        ).next_to(result, DOWN, buff=0.4)

        self.next_slide()
        self.play(
            FadeOut(snippet),
            FadeOut(problem),
            FadeOut(arrow),
            FadeOut(result),
            run_time=0.6,
        )
