"""Slide 8/20: propuesta · fase 2 (conjunto de cobertura)."""

from __future__ import annotations

import numpy as np
from common import ACCENT, GREEN, INK, MUTED, WARM, ThemedSlide, body, card, eq, reveal_card
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Brace,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Text,
    VGroup,
    Write,
)

# Recta de la componente d: a_d, y_0, y*, b_d equiespaciados por Delta y_d,
# de modo que el diametro del intervalo es 3 * Delta y_d (Teorema thm:cov_diameter).
LINE_Y = -0.2
A_X, Y0_X, YSTAR_X, B_X = -4.8, -2.4, 0.0, 2.4

# Dos muestras de 8 puntos en [0, 1]: agrupada (discrepancia alta) y
# casi uniforme (discrepancia baja), como las que compara la Fase 2.
CLUMPED = [0.04, 0.09, 0.13, 0.17, 0.22, 0.26, 0.78, 0.86]
UNIFORM = [0.06, 0.19, 0.31, 0.44, 0.56, 0.69, 0.81, 0.94]

STRIP_LEFT, STRIP_RIGHT = -3.4, 3.4
STRIP_Y = -1.2


def _strip_x(u: float) -> float:
    return STRIP_LEFT + u * (STRIP_RIGHT - STRIP_LEFT)


def _tick(x: float, label: str, *, color: str = INK, below: bool = True) -> VGroup:
    mark = Line(
        np.array([x, LINE_Y - 0.16, 0.0]),
        np.array([x, LINE_Y + 0.16, 0.0]),
        color=color,
        stroke_width=3,
    )
    text = eq(label, font_size=28, color=color)
    text.next_to(mark, DOWN if below else UP, buff=0.18)
    return VGroup(mark, text)


class PropuestaFase2Slide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Fase 2: conjunto de cobertura")

        intro = body(
            "Hace falta diversidad alrededor de la predicción y del objetivo "
            "para poder estimar efectos en la Fase 3.",
            font_size=25,
            width=80,
        ).next_to(head, DOWN, buff=0.4)
        self.play(Write(intro))

        # --- Intervalo de cobertura por componente ---
        self.next_slide()
        axis = Line(
            np.array([-6.2, LINE_Y, 0.0]),
            np.array([4.0, LINE_Y, 0.0]),
            color=MUTED,
            stroke_width=2,
        )
        tick_y0 = _tick(Y0_X, r"\hat{y}_{0,d}", color=ACCENT)
        tick_ystar = _tick(YSTAR_X, r"y^{*}_{d}", color=WARM)
        tick_a = _tick(A_X, "a_d", color=INK)
        tick_b = _tick(B_X, "b_d", color=INK)

        self.play(Create(axis), run_time=0.6)
        self.play(FadeIn(tick_y0), FadeIn(tick_ystar))

        self.next_slide()
        delta = Brace(
            Line(np.array([Y0_X, LINE_Y, 0.0]), np.array([YSTAR_X, LINE_Y, 0.0])),
            direction=UP,
            color=MUTED,
        )
        delta_label = eq(r"\Delta y_d", font_size=26, color=MUTED).next_to(delta, UP, buff=0.1)
        self.play(Create(delta), Write(delta_label))

        self.next_slide()
        span = Line(
            np.array([A_X, LINE_Y, 0.0]),
            np.array([B_X, LINE_Y, 0.0]),
            color=GREEN,
            stroke_width=7,
        )
        self.play(Create(span), FadeIn(tick_a), FadeIn(tick_b))
        diameter = Brace(span, direction=DOWN, color=GREEN)
        diameter_label = eq(r"3\,|\hat{y}_{0,d} - y^{*}_{d}|", font_size=26, color=GREEN)
        diameter_label.next_to(diameter, DOWN, buff=0.1)
        self.play(Create(diameter), Write(diameter_label))

        interval = eq(
            r"\mathcal{I}_d = \left[\min(\hat{y}_{0,d}, y^{*}_d) - \Delta y_d,\;"
            r"\max(\hat{y}_{0,d}, y^{*}_d) + \Delta y_d\right]",
            font_size=28,
        ).next_to(diameter_label, DOWN, buff=0.6)
        self.play(Write(interval))

        number_line = VGroup(
            axis, tick_y0, tick_ystar, tick_a, tick_b, delta, delta_label, span, diameter, diameter_label
        )

        self.next_slide()
        self.play(FadeOut(number_line), FadeOut(interval), FadeOut(intro), run_time=0.6)

        # --- Discrepancia estelar centrada L2 ---
        rescale = card(
            "Normalización a [0, 1]",
            eq(r"\varphi_{a,b}(y) = \frac{y - a}{b - a}", font_size=28),
            title_font_size=23,
            title_width=26,
            gap=0.25,
        )
        discrepancy = card(
            "Discrepancia estelar centrada",
            eq(
                r"D^2(\mathcal{S}) = \frac{13}{12}"
                r"- \frac{2}{m}\sum_{i=1}^{m} k(u_i)"
                r"+ \frac{1}{m^2}\sum_{i=1}^{m}\sum_{j=1}^{m} K(u_i, u_j)",
                font_size=24,
            ),
            title_font_size=23,
            title_width=26,
            gap=0.25,
        )
        formulas = VGroup(rescale, discrepancy).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        formulas.next_to(head, DOWN, buff=0.5)
        for formula in formulas:
            reveal_card(self, formula)
            self.next_slide()

        # --- Muestra agrupada vs muestra de baja discrepancia ---
        strip = Line(
            np.array([STRIP_LEFT, STRIP_Y, 0.0]),
            np.array([STRIP_RIGHT, STRIP_Y, 0.0]),
            color=MUTED,
            stroke_width=2,
        )
        zero = eq("0", font_size=24, color=MUTED).next_to(strip.get_start(), LEFT, buff=0.25)
        one = eq("1", font_size=24, color=MUTED).next_to(strip.get_end(), RIGHT, buff=0.25)
        dots = VGroup(
            *[Dot(np.array([_strip_x(u), STRIP_Y, 0.0]), radius=0.08, color=WARM) for u in CLUMPED]
        )
        caption = Text("discrepancia alta: zonas sin cubrir", font_size=23, color=WARM)
        caption.next_to(strip, DOWN, buff=0.4)

        self.play(Create(strip), FadeIn(zero), FadeIn(one), run_time=0.6)
        self.play(FadeIn(dots, shift=UP * 0.2), Write(caption))

        self.next_slide()
        new_caption = Text("discrepancia baja: cobertura uniforme", font_size=23, color=GREEN)
        new_caption.move_to(caption)
        self.play(
            *[
                dot.animate.move_to(np.array([_strip_x(u), STRIP_Y, 0.0])).set_color(GREEN)
                for dot, u in zip(dots, UNIFORM)
            ],
            FadeOut(caption),
            FadeIn(new_caption),
            run_time=1.4,
        )

        self.next_slide()
        objective = eq(
            r"\operatorname{MeanCov}(\mathcal{S}) = \frac{1}{D}\sum_{d=0}^{D-1}"
            r"\operatorname{Cov}_d(\mathcal{S})"
            r"\;\longrightarrow\; \min_{\mathcal{S} \subseteq [r_{\min}, r_{\max}]^{n_{\mathrm{In}}}}",
            font_size=28,
            color=ACCENT,
        ).next_to(caption, DOWN, buff=0.4)
        note = body(
            "si ninguna predicción cae en el intervalo, esa componente se penaliza",
            font_size=21,
            width=80,
            color=MUTED,
        ).next_to(objective, DOWN, buff=0.25)
        self.play(Write(objective))
        self.play(FadeIn(note, shift=UP * 0.15))
