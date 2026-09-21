"""Slide 6/20: análisis del problema."""

from __future__ import annotations

import numpy as np
from common import (
    ACCENT,
    GREEN,
    INK,
    MUTED,
    WARM,
    ThemedSlide,
    body,
    disc_marker,
    eq,
    fit_below,
    marker_item,
    reveal_staggered,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedLine,
    DashedVMobject,
    Dot,
    Ellipse,
    FadeIn,
    FadeOut,
    Line,
    Rectangle,
    Text,
    VGroup,
    Write,
)

# (texto del requisito, formalización asociada)
REQUIREMENTS = [
    (
        "No depender del conjunto de entrenamiento original.",
        r"\mathcal{D}_{\mathrm{train}} = \varnothing \;\Rightarrow\; "
        r"\langle \hat{f},\, \mathbf{x}_0,\, \mathbf{y}^{*} \rangle",
    ),
    (
        "Aproximar un objetivo vectorial en las D salidas, no una sola variable.",
        r"\min_{\mathbf{x}'}\; \bigl\| \hat{f}(\mathbf{x}') - \mathbf{y}^{*} \bigr\|_2",
    ),
    (
        "Respetar la estructura temporal codificada en los retardos.",
        r"x'_j = x_{0,j}\ \forall j \notin W,\quad x'_j \in [r_{\min}, r_{\max}]",
    ),
    (
        "Puntuar la consistencia causal de cada candidato.",
        r"s_k = \tfrac{1}{D} \sum_{d=1}^{D} \mathrm{cons}_d",
    ),
]

# perfil de retardos del ejemplo: x_0 (serie observada) y una perturbación
# coherente con la dinámica frente a otra arbitraria que rompe la continuidad.
LAGS = ["t-4", "t-3", "t-2", "t-1"]
X0_VALUES = [0.35, 0.62, 0.88, 1.05]
COHERENT = [0.35, 0.70, 1.02, 1.28]
ARBITRARY = [0.35, 1.45, 0.20, 1.30]

# consistencia causal por salida: cambio esperado por el modelo causal auxiliar
# frente al cambio realmente inducido por el predictor.
CONSISTENCY = [
    ("X_t", 0.82, 0.78),
    ("Y_t", 0.55, 0.61),
    ("Z_t", 0.40, 0.14),
]


def _requirement(number: int, text: str, tex: str) -> VGroup:
    item = marker_item(disc_marker(number), text, font_size=24, width=44)
    formula = eq(tex, font_size=24, color=MUTED)
    return VGroup(item, formula).arrange(RIGHT, buff=0.45)


class AnalisisProblemaSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Análisis del problema")

        # --- Formalización del problema ---
        given = eq(
            r"\hat{f}: \mathbb{R}^{n_{\mathrm{In}}} \to \mathbb{R}^{D},",
            r"\quad \mathbf{x}_0,",
            r"\quad \mathbf{y}^{*} \in \mathbb{R}^{D}",
            font_size=36,
        ).next_to(head, DOWN, buff=0.6)
        self.play(Write(given))

        self.next_slide()
        detail = VGroup(
            eq(
                r"n_{\mathrm{In}} = D \times T, \qquad "
                r"\mathbf{x}_0 = \bigl(Z^1_{t-1}, \ldots, Z^D_{t-T}\bigr)",
                font_size=30,
            ),
            eq(
                r"\hat{\mathbf{y}}_0 = \hat{f}(\mathbf{x}_0), \qquad "
                r"\Delta \mathbf{y}^{*} = \mathbf{y}^{*} - \hat{\mathbf{y}}_0",
                font_size=30,
            ),
        ).arrange(DOWN, buff=0.3).next_to(given, DOWN, buff=0.5)
        self.play(Write(detail), run_time=1.6)

        self.next_slide()
        self.play(FadeOut(detail))

        # --- Cuatro requisitos, cada uno con su formalización ---
        items = VGroup(*[_requirement(i + 1, t, x) for i, (t, x) in enumerate(REQUIREMENTS)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        # columna de fórmulas alineada a la izquierda (el ancho del texto varía)
        formula_x = max(item[0].get_right()[0] for item in items) + 0.5
        for item in items:
            item[1].move_to(
                np.array([formula_x + item[1].width / 2, item[1].get_center()[1], 0.0])
            )
        fit_below(items, given, buff=0.55, bottom=-3.0)

        for item in items:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.7)
            self.next_slide()

        closing = Text(
            "Más restrictivo que el caso tabular estático",
            font_size=26,
            color=ACCENT,
            weight="BOLD",
        ).next_to(items, DOWN, buff=0.45)
        self.play(FadeIn(closing, shift=UP * 0.2))

        self.next_slide()
        self.play(FadeOut(given), FadeOut(items), FadeOut(closing))

        # --- Figura 1: espacio de salida, frontera y conjunto de cobertura ---
        caption = body(
            "El objetivo suele situarse en la frontera de las salidas alcanzables "
            "mediante perturbaciones locales de la instancia original.",
            font_size=24,
            width=74,
        ).next_to(head, DOWN, buff=0.5)
        self.play(Write(caption))

        reachable = DashedVMobject(
            Ellipse(width=6.4, height=3.0, color=MUTED, stroke_width=3), num_dashes=40
        ).move_to([-0.6, -1.3, 0])
        region_label = Text("salidas alcanzables", font_size=20, color=MUTED)
        region_label.next_to(reachable, DOWN, buff=0.15)

        y0_point = np.array([-2.0, -1.7, 0.0])
        ystar_point = np.array([2.3, -0.67, 0.0])
        y0 = Dot(y0_point, radius=0.09, color=ACCENT)
        ystar = Dot(ystar_point, radius=0.09, color=WARM)
        y0_label = eq(r"\hat{\mathbf{y}}_0", font_size=28, color=ACCENT).next_to(y0, DOWN, buff=0.2)
        ystar_label = eq(r"\mathbf{y}^{*}", font_size=28, color=WARM).next_to(ystar, UP, buff=0.2)
        path = Arrow(y0_point, ystar_point, buff=0.12, color=INK, stroke_width=3)

        self.next_slide()
        self.play(Create(reachable), Write(region_label))
        self.play(FadeIn(y0), Write(y0_label), FadeIn(ystar), Write(ystar_label))
        self.next_slide()
        self.play(Create(path))


        # nube de cobertura alrededor del trayecto
        self.next_slide()
        rng = np.random.default_rng(7)
        cloud = VGroup()
        for lam in np.linspace(0.05, 0.95, 7):
            center = (1 - lam) * y0_point + lam * ystar_point
            for _ in range(3):
                offset = np.array([rng.normal(0, 0.22), rng.normal(0, 0.18), 0.0])
                cloud.add(Dot(center + offset, radius=0.045, color=GREEN))
        cloud_label = Text("conjunto de cobertura", font_size=20, color=GREEN)
        cloud_label.next_to(reachable, UP, buff=0.18).shift(RIGHT * 1.8)
        reveal_staggered(self, cloud, lag_ratio=0.05, run_time=1.4)
        self.play(Write(cloud_label))

        figure1 = VGroup(
            reachable, region_label, y0, ystar, y0_label, ystar_label, path, cloud, cloud_label
        )

        self.next_slide()
        self.play(FadeOut(caption), FadeOut(figure1))

        # --- Figura 2: coherencia temporal de los retardos ---
        caption2 = body(
            "Las entradas son retardos: una perturbación arbitraria rompe la "
            "dependencia entre instantes consecutivos aunque siga dentro del "
            "espacio de búsqueda.",
            font_size=25,
            width=62,
        ).next_to(head, DOWN, buff=0.5)
        self.play(Write(caption2))

        base_y = -2.6
        step_x = 1.9
        origin_x = -3.4
        y_scale = 1.6

        def _series(values, color, *, dashed=False):
            points = [
                np.array([origin_x + i * step_x, base_y + v * y_scale, 0.0])
                for i, v in enumerate(values)
            ]
            group = VGroup()
            for start, end in zip(points, points[1:], strict=False):
                seg = Line(start, end, color=color, stroke_width=4)
                group.add(DashedVMobject(seg, num_dashes=8) if dashed else seg)
            for point in points:
                group.add(Dot(point, radius=0.07, color=color))
            return group

        axis_x = Line(
            np.array([origin_x - 0.5, base_y, 0.0]),
            np.array([origin_x + (len(LAGS) - 1) * step_x + 1.1, base_y, 0.0]),
            color=MUTED,
            stroke_width=2,
        )
        ticks = VGroup(
            *[
                eq(rf"x_{{{lag}}}", font_size=22, color=MUTED).move_to(
                    np.array([origin_x + i * step_x, base_y - 0.3, 0.0])
                )
                for i, lag in enumerate(LAGS)
            ]
        )
        original = _series(X0_VALUES, INK)
        coherent = _series(COHERENT, GREEN, dashed=True)
        arbitrary = _series(ARBITRARY, WARM, dashed=True)

        legend = VGroup(
            VGroup(Line(np.array([0, 0, 0]), np.array([0.4, 0, 0]), color=INK, stroke_width=4),
                   eq(r"\mathbf{x}_0", font_size=24, color=INK)).arrange(RIGHT, buff=0.2),
            VGroup(Line(np.array([0, 0, 0]), np.array([0.4, 0, 0]), color=GREEN, stroke_width=4),
                   Text("coherente", font_size=21, color=GREEN)).arrange(RIGHT, buff=0.2),
            VGroup(Line(np.array([0, 0, 0]), np.array([0.4, 0, 0]), color=WARM, stroke_width=4),
                   Text("arbitraria", font_size=21, color=WARM)).arrange(RIGHT, buff=0.2),
        ).arrange(RIGHT, buff=0.6)
        legend.next_to(axis_x, DOWN, buff=0.55)

        self.next_slide()
        self.play(Create(axis_x), Write(ticks))
        self.play(Create(original))
        self.next_slide()
        self.play(Create(coherent))
        self.next_slide()
        self.play(Create(arbitrary))
        self.play(FadeIn(legend))

        # --- Figura 3: consistencia causal por salida ---
        caption3 = body(
            "La puntuación compara, salida a salida, el cambio esperado por el "
            "modelo causal auxiliar con el cambio real inducido por el predictor.",
            font_size=25,
            width=62,
        ).next_to(head, DOWN, buff=0.5)
        self.play(FadeOut(caption2), Write(caption3))

        bar_scale = 4.0
        bar_height = 0.22
        bar_gap = 0.07
        row_step = 0.95
        origin = -1.6
        rows = VGroup()
        for index, (name, expected, real) in enumerate(CONSISTENCY):
            y = -index * row_step
            label = eq(rf"{name}", font_size=26, color=INK)
            label.move_to(np.array([origin - 0.9, y, 0.0]))
            top = Rectangle(
                width=expected * bar_scale, height=bar_height, color=ACCENT, fill_opacity=0.9, stroke_width=0
            ).move_to(np.array([origin + expected * bar_scale / 2, y + (bar_height + bar_gap) / 2, 0.0]))
            bottom = Rectangle(
                width=real * bar_scale, height=bar_height, color=WARM, fill_opacity=0.9, stroke_width=0
            ).move_to(np.array([origin + real * bar_scale / 2, y - (bar_height + bar_gap) / 2, 0.0]))
            gap_line = DashedLine(
                np.array([origin + min(expected, real) * bar_scale, y, 0.0]),
                np.array([origin + max(expected, real) * bar_scale, y, 0.0]),
                color=MUTED,
                stroke_width=2,
                dash_length=0.08,
            )
            rows.add(VGroup(label, top, bottom, gap_line))

        axis = Line(
            np.array([origin, 0.6, 0.0]),
            np.array([origin, -len(CONSISTENCY) * row_step + 0.35, 0.0]),
            color=MUTED,
            stroke_width=2,
        )
        legend3 = VGroup(
            VGroup(
                Rectangle(width=0.4, height=0.16, color=ACCENT, fill_opacity=0.9, stroke_width=0),
                eq(r"\Delta \tilde{y}_d \ \text{(causal)}", font_size=23, color=INK),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Rectangle(width=0.4, height=0.16, color=WARM, fill_opacity=0.9, stroke_width=0),
                eq(r"\Delta \hat{y}_d \ \text{(modelo)}", font_size=23, color=INK),
            ).arrange(RIGHT, buff=0.2),
        ).arrange(RIGHT, buff=0.8)

        chart = VGroup(axis, rows)
        score = eq(
            r"s_k = \frac{1}{D} \sum_{d=1}^{D} "
            r"\mathrm{cons}\bigl(\Delta \tilde{y}_d,\, \Delta \hat{y}_d\bigr) \in (0, 1]",
            font_size=28,
        )
        block = VGroup(chart, legend3, score).arrange(DOWN, buff=0.35)
        fit_below(block, caption3, buff=0.45, bottom=-3.9)

        self.next_slide()
        self.play(Create(axis))
        reveal_staggered(self, rows, lag_ratio=0.2, run_time=1.6)
        self.play(FadeIn(legend3))
        self.next_slide()
        self.play(Write(score), run_time=1.6)
