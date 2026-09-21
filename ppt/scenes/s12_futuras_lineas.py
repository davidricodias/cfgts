"""Slide 15/16: futuras líneas de investigación."""

from __future__ import annotations

from common import ACCENT, INK, MUTED, ThemedSlide, wrap
from manim import (
    DOWN,
    RIGHT,
    UP,
    Create,
    FadeIn,
    SurroundingRectangle,
    Text,
    VGroup,
    Write,
)

LINES = [
    (
        "Métodos alternativos de generación",
        "Descenso de gradiente, algoritmos evolutivos o instancias "
        "prototípicas en la Fase 1, sin tocar las Fases 2 y 3.",
    ),
    (
        "Causalidad en modelos no lineales",
        "Efectos locales dependientes de la instancia y grafos causales "
        "aportados por expertos de dominio.",
    ),
    (
        "Evaluación y transferencia",
        "Más dominios reales y extensión de la interfaz a PyTorch o TensorFlow.",
    ),
]


def _line(title: str, text: str) -> VGroup:
    label = Text(wrap(title, 22), font_size=24, color=ACCENT, weight="BOLD", line_spacing=1.1)
    detail = Text(wrap(text, 30), font_size=19, color=INK, line_spacing=1.15)
    content = VGroup(label, detail).arrange(DOWN, buff=0.3)
    frame = SurroundingRectangle(
        content, corner_radius=0.12, buff=0.32, color=MUTED, stroke_width=2
    )
    return VGroup(frame, content)


class FuturasLineasSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Futuras líneas de investigación")

        cards = VGroup(*[_line(title, text) for title, text in LINES])
        cards.arrange(RIGHT, buff=0.55, aligned_edge=UP).next_to(head, DOWN, buff=0.9)

        for card in cards:
            frame, content = card
            self.play(Create(frame), Write(content[0]), run_time=0.7)
            self.play(FadeIn(content[1], shift=UP * 0.2), run_time=0.7)
            self.next_slide()

        closing = Text(
            "La implementación queda como base para extenderlo",
            font_size=26,
            color=ACCENT,
            weight="BOLD",
        ).next_to(cards, DOWN, buff=0.6)
        self.play(FadeIn(closing, shift=UP * 0.2))
