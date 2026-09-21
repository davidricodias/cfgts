"""Shared palette/helpers for the ppt/ slide scripts.

Prose uses Pango `Text` (native accent support); only equations use
`MathTex`, so no Spanish text ever goes through the LaTeX toolchain.
"""

from __future__ import annotations

import textwrap

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circle,
    Create,
    FadeIn,
    LaggedStart,
    Line,
    ManimColor,
    MathTex,
    Mobject,
    Rectangle,
    RoundedRectangle,
    SurroundingRectangle,
    Text,
    VGroup,
    Write,
)
from manim_slides import Slide

Text.set_default(font="CMU Serif")

BG = "#F2F4FF"
INK = "#12163A"
MUTED = "#525C82"
ACCENT = "#1F52C4"
WARM = "#C4451F"
GREEN = "#1F7A4C"


def wrap(text: str, width: int = 46) -> str:
    """Textwrap because `Text` does not wrap on its own."""
    return "\n".join(textwrap.wrap(text, width=width))


def body(text: str, *, font_size: int = 28, width: int = 46, color: str = INK) -> Text:
    return Text(wrap(text, width), font_size=font_size, color=color, line_spacing=1.15)


def bullets(items: list[str], *, font_size: int = 28, width: int = 46) -> VGroup:
    return VGroup(
        *[
            Text(f"\u2022 {wrap(item, width)}", font_size=font_size, color=INK, line_spacing=1.15)
            for item in items
        ]
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)


def eq(*tex: str, font_size: int = 38, color: str = INK) -> MathTex:
    """`MathTex` renders white by default, invisible on this light background."""
    return MathTex(*tex, font_size=font_size, color=color)


def fit_below(group: Mobject, reference: Mobject, *, buff: float = 0.6, bottom: float = -3.9):
    """Place `group` under `reference`, shrinking it if it would overflow `bottom`."""
    available = reference.get_bottom()[1] - buff - bottom
    if group.height > available:
        group.scale(available / group.height)
    group.next_to(reference, DOWN, buff=buff)
    return group


def frame_around(
    content: Mobject,
    *,
    width: float | None = None,
    height: float | None = None,
    color: str = MUTED,
    corner_radius: float = 0.12,
    buff: float = 0.32,
) -> Mobject:
    """A rounded frame around `content`.

    Auto-fits to `content` (`SurroundingRectangle`) unless `width`/`height` are
    given, in which case a fixed-size `RoundedRectangle` is centered on it
    instead -- used when several cards must share one uniform size.
    """
    if width is not None and height is not None:
        return RoundedRectangle(
            width=width, height=height, corner_radius=corner_radius, color=color, stroke_width=2
        ).move_to(content)
    return SurroundingRectangle(content, corner_radius=corner_radius, buff=buff, color=color)


def card(
    title: str,
    content: Mobject,
    *,
    title_font_size: int = 26,
    title_color: str = ACCENT,
    title_width: int | None = None,
    title_line_spacing: float = 1.0,
    frame_color: str = MUTED,
    corner_radius: float = 0.12,
    buff: float = 0.32,
    gap: float = 0.3,
    width: float | None = None,
    height: float | None = None,
) -> VGroup:
    """A titled card: rounded frame around a `Write`-able title and a body.

    `title_width` wraps the title (like `wrap()`) when it may span multiple
    lines. Returns `VGroup(frame, VGroup(title_text, content))` so
    `reveal_card` can animate the title/frame first and the body second.
    Covers the "title + wrapped body in a frame, arranged in a grid/row"
    pattern shared by the pillar/quadrant/block/line slides.
    """
    title_text = wrap(title, title_width) if title_width is not None else title
    label = Text(
        title_text,
        font_size=title_font_size,
        color=title_color,
        weight="BOLD",
        line_spacing=title_line_spacing,
    )
    inner = VGroup(label, content).arrange(DOWN, buff=gap)
    frame = frame_around(
        inner, width=width, height=height, color=frame_color, corner_radius=corner_radius, buff=buff
    )
    return VGroup(frame, inner)


def reveal_card(
    scene: Slide,
    card_group: VGroup,
    *,
    frame_run_time: float = 0.7,
    body_run_time: float = 0.6,
    body_shift=UP * 0.2,
) -> None:
    """Animate a `card()` group: frame + title, then the body fades in."""
    frame, inner = card_group
    title, content = inner
    scene.play(Create(frame), Write(title), run_time=frame_run_time)
    scene.play(FadeIn(content, shift=body_shift), run_time=body_run_time)


def disc_marker(
    number: int, *, radius: float = 0.22, color: str = ACCENT, text_color: str = BG, font_size: int = 20
) -> VGroup:
    """A filled numbered disc, e.g. for step/requirement lists."""
    disc = Circle(radius=radius, color=color, fill_opacity=1.0, stroke_width=0)
    badge = Text(str(number), font_size=font_size, color=text_color, weight="BOLD").move_to(disc)
    return VGroup(disc, badge)


def marker_item(
    marker: Mobject,
    text: str,
    *,
    font_size: int = 26,
    width: int = 52,
    color: str = INK,
    buff: float = 0.3,
    aligned_edge=None,
) -> VGroup:
    """A `marker` (disc, checkmark, ...) followed by wrapped body text."""
    label = Text(wrap(text, width), font_size=font_size, color=color, line_spacing=1.15)
    group = VGroup(marker, label)
    if aligned_edge is None:
        return group.arrange(RIGHT, buff=buff)
    return group.arrange(RIGHT, buff=buff, aligned_edge=aligned_edge)


def value_bar(
    value: float,
    y: float,
    color: str,
    *,
    origin_x: float = 0.0,
    scale: float = 1.0,
    height: float = 0.15,
    min_width: float = 0.0,
) -> Rectangle:
    """A horizontal bar of length `value * scale`, growing right from `origin_x`."""
    bar_width = max(value * scale, min_width)
    rect = Rectangle(width=bar_width, height=height, color=color, fill_opacity=0.9, stroke_width=0)
    rect.move_to(np.array([origin_x + bar_width / 2, y, 0.0]))
    return rect


def range_bar(left_x: float, right_x: float, y: float, color: str, *, height: float = 0.26) -> Rectangle:
    """A horizontal bar spanning `[left_x, right_x]`, e.g. for Gantt-style timelines."""
    rect = Rectangle(
        width=right_x - left_x, height=height, color=color, fill_opacity=0.85, stroke_width=0
    )
    rect.move_to(np.array([(left_x + right_x) / 2, y, 0.0]))
    return rect


def vertical_axis(x: float, top_y: float, bottom_y: float, *, color: str = MUTED, stroke_width: float = 2) -> Line:
    """A vertical axis/baseline line, e.g. for the left edge of a bar chart."""
    return Line(np.array([x, top_y, 0.0]), np.array([x, bottom_y, 0.0]), color=color, stroke_width=stroke_width)


def row_label(text: str, x: float, y: float, *, font_size: int = 21, color: str = INK, buff: float = 0.3) -> Text:
    """A row label right-aligned to end at `(x, y)`, e.g. left of a bar chart row."""
    label = Text(text, font_size=font_size, color=color)
    label.next_to(np.array([x, y, 0.0]), LEFT, buff=buff)
    return label


def reveal_staggered(
    scene: Slide,
    mobjects,
    *,
    shift=UP * 0.2,
    lag_ratio: float = 0.15,
    run_time: float = 2.0,
) -> None:
    """`FadeIn` each of `mobjects` in a `LaggedStart`, e.g. for chart rows/bullets."""
    scene.play(
        LaggedStart(*(FadeIn(m, shift=shift) for m in mobjects), lag_ratio=lag_ratio),
        run_time=run_time,
    )


class ThemedSlide(Slide):
    """Light-background slide with a consistent animated heading."""

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = ManimColor(BG)

    def show_heading(self, text: str, *, font_size: int = 38) -> VGroup:
        label = Text(text, font_size=font_size, color=ACCENT, weight="BOLD")
        rule = Line(
            label.get_corner(DOWN + LEFT),
            label.get_corner(DOWN + RIGHT),
            color=ACCENT,
            stroke_width=3,
        ).shift(DOWN * 0.2)
        group = VGroup(label, rule).to_edge(UP, buff=0.45)
        self.play(Write(label), Create(rule), run_time=1.0)
        return group
