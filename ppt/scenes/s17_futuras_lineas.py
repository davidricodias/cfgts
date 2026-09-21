"""Slide 18/20: futuras líneas de investigación."""

from __future__ import annotations

from common import ACCENT, INK, ThemedSlide, card, reveal_card, wrap
from manim import (
    DOWN,
    RIGHT,
    UP,
    FadeIn,
    Text,
    VGroup,
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
    detail = Text(wrap(text, 30), font_size=19, color=INK, line_spacing=1.15)
    return card(
        title,
        detail,
        title_font_size=24,
        title_width=22,
        title_line_spacing=1.1,
        buff=0.32,
        gap=0.3,
    )


class FuturasLineasSlide(ThemedSlide):
    def construct(self) -> None:
        head = self.show_heading("Futuras líneas de investigación")

        cards = VGroup(*[_line(title, text) for title, text in LINES])
        cards.arrange(RIGHT, buff=0.55, aligned_edge=UP).next_to(head, DOWN, buff=0.9)

        for card_group in cards:
            reveal_card(self, card_group, frame_run_time=0.7, body_run_time=0.7)
            self.next_slide()

        closing = Text(
            "La implementación es fácilmente extendible",
            font_size=26,
            color=ACCENT,
            weight="BOLD",
        ).next_to(cards, DOWN, buff=0.6)
        self.play(FadeIn(closing, shift=UP * 0.2))
