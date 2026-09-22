"""Slide 11/20: implementación, CI/CD y publicación en PyPI."""

from __future__ import annotations

from common import ACCENT, BG, GREEN, INK, MUTED, WARM, ThemedSlide, body, card, fit_below, reveal_card
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    RoundedRectangle,
    Text,
    VGroup,
    Write,
)

MODULES = [
    ("cfgts/cfgts.py", "clase CFGTS, objetivos anidados y distancias con Numba"),
    ("cfgts/logger.py", "ContextLogger con timeit() para medir cada fase"),
    ("cfgts/py.typed", "marcador PEP 561: el paquete se distribuye tipado"),
]

DEPENDENCIES = [
    ("scikit-learn", "RegressorMixin + check_is_fitted"),
    ("Optuna", "NSGA y TPE de las fases 1 y 2"),
    ("DoWhy + NetworkX", "DAG y efectos causales"),
    ("Polars + NumPy + Numba", "datos y cálculo vectorizado"),
]

# Cadena de CI: cada push/PR dispara linting y la matriz de tests.
CI_STEPS = [
    ("push / PR", MUTED),
    ("ruff + mypy", ACCENT),
    ("pytest\n3 Python x 3 SO", ACCENT),
]
# Cadena de CD: al publicar la release, se construye y se publica.
CD_STEPS = [
    ("merge a main\nRelease Drafter", MUTED),
    ("release\npublicada", WARM),
    ("uv build\nuv publish", GREEN),
]

BOX_W = 2.75
BOX_H = 1.05


def _step(label: str, color: str) -> VGroup:
    box = RoundedRectangle(
        width=BOX_W, height=BOX_H, corner_radius=0.12, color=color, stroke_width=2.5
    )
    box.set_fill(color, opacity=0.08)
    text = Text(label, font_size=19, color=INK, line_spacing=0.9).move_to(box)
    return VGroup(box, text)


def _column(title: str, entries: list[tuple[str, str]], color: str) -> VGroup:
    """Columna 'título + pares (nombre, descripción)' de la vista de arquitectura."""
    rows = VGroup(
        *[
            VGroup(
                Text(name, font_size=19, color=color, weight="BOLD"),
                body(text, font_size=18, width=32, color=MUTED),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            for name, text in entries
        ]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    header = Text(title, font_size=22, color=INK, weight="BOLD")
    return VGroup(header, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3)


def _chain(steps: list[tuple[str, str]]) -> tuple[VGroup, VGroup]:
    boxes = VGroup(*[_step(label, color) for label, color in steps]).arrange(RIGHT, buff=0.75)
    arrows = VGroup(
        *[
            Arrow(
                boxes[i].get_right(),
                boxes[i + 1].get_left(),
                buff=0.1,
                color=MUTED,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.4,
            )
            for i in range(len(boxes) - 1)
        ]
    )
    return boxes, arrows


class ImplementacionSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Implementación")

        api = card(
            "API de clase única",
            VGroup(
                Text("CFGTS(model, instance, counterfactual_value, ...)", font_size=20, color=INK),
                Text(".run()  →  .counterfactuals  ·  .study", font_size=20, color=ACCENT),
            ).arrange(DOWN, buff=0.22),
            title_font_size=24,
        ).next_to(head, DOWN, buff=0.5)
        reveal_card(self, api)

        self.next_slide()
        modules = _column("Módulos", MODULES, ACCENT)
        deps = _column("Dependencias", DEPENDENCIES, WARM)
        columns = VGroup(modules, deps).arrange(RIGHT, buff=1.0, aligned_edge=UP)
        fit_below(columns, api, buff=0.5, bottom=-3.6)
        self.play(FadeIn(columns, shift=UP * 0.2), run_time=1.2)

        self.next_slide()
        self.play(FadeOut(api), FadeOut(columns), run_time=0.6)

        # --- Pipeline de CI/CD ---
        ci_title = Text("Integración continua", font_size=24, color=ACCENT, weight="BOLD")
        ci_boxes, ci_arrows = _chain(CI_STEPS)
        ci = VGroup(ci_title, VGroup(ci_boxes, ci_arrows)).arrange(DOWN, buff=0.3)
        ci.next_to(head, DOWN, buff=0.5)

        self.play(Write(ci_title))
        self.play(FadeIn(ci_boxes[0]), run_time=0.4)
        for index in range(len(ci_arrows)):
            self.play(Create(ci_arrows[index]), FadeIn(ci_boxes[index + 1]), run_time=0.6)
        self.next_slide()

        cd_title = Text("Entrega continua", font_size=24, color=GREEN, weight="BOLD")
        cd_boxes, cd_arrows = _chain(CD_STEPS)
        cd = VGroup(cd_title, VGroup(cd_boxes, cd_arrows)).arrange(DOWN, buff=0.3)
        cd.next_to(ci, DOWN, buff=0.5)

        self.play(Write(cd_title))
        self.play(FadeIn(cd_boxes[0]), run_time=0.4)
        for index in range(len(cd_arrows)):
            self.play(Create(cd_arrows[index]), FadeIn(cd_boxes[index + 1]), run_time=0.6)

        self.next_slide()
        pypi = _step("PyPI", GREEN)
        docs = _step("GitHub Pages\n(mkdocs)", MUTED)
        targets = VGroup(docs, pypi).arrange(RIGHT, buff=0.75)
        targets.next_to(cd_boxes, DOWN, buff=0.8)
        to_pypi = Arrow(
            cd_boxes[2].get_bottom(), pypi.get_top(), buff=0.12, color=GREEN, stroke_width=3
        )
        to_docs = Arrow(
            cd_boxes[1].get_bottom(), docs.get_top(), buff=0.12, color=MUTED, stroke_width=3
        )
        self.play(Create(to_pypi), FadeIn(pypi), Create(to_docs), FadeIn(docs), run_time=1.0)

        oidc = Text(
            "OIDC: publicación de confianza, sin credenciales en el repositorio",
            font_size=20,
            color=GREEN,
        ).next_to(targets, DOWN, buff=0.35)
        self.play(FadeIn(oidc, shift=UP * 0.15))

        self.next_slide()
        install_box = RoundedRectangle(
            width=4.4, height=0.9, corner_radius=0.12, color=ACCENT, stroke_width=3
        ).set_fill(BG, opacity=1.0)
        install_text = Text("pip install cfgts", font_size=28, color=ACCENT).move_to(install_box)
        install = VGroup(install_box, install_text).move_to(targets)
        self.play(
            FadeOut(targets),
            FadeOut(to_pypi),
            FadeOut(to_docs),
            FadeOut(oidc),
            run_time=0.5,
        )
        self.play(Create(install_box), Write(install_text))

        self.next_slide()
        version = Text("cfgts 1.0.0  ·  Python 3.11+  ·  CC BY-NC-ND", font_size=22, color=INK)
        version.next_to(install, DOWN, buff=0.35)
        self.play(FadeIn(version, shift=UP * 0.15))
