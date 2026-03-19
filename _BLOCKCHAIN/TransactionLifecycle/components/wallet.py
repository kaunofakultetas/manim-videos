from manim import *
import numpy as np


def _soft_glow(pos, color, max_radius=0.5, layers=6, peak_opacity=0.06):
    g = VGroup()
    for i in range(layers):
        t = (i + 1) / layers
        r = max_radius * t
        op = peak_opacity * (1 - t) + 0.003
        c = Circle(radius=r, color=color, fill_opacity=op, stroke_width=0)
        c.move_to(pos)
        g.add(c)
    return g


def create_avatar(name, color=BLUE_C, radius=0.5):
    glow = _soft_glow(ORIGIN, color, max_radius=radius * 1.6, peak_opacity=0.04)
    ring = Circle(
        radius=radius + 0.04, color=color,
        fill_opacity=0, stroke_width=1.5, stroke_opacity=0.35,
    )
    disc = Circle(radius=radius, color=color, fill_opacity=0.18, stroke_width=2.5)
    initial = Text(
        name[0].upper(), font_size=int(radius * 68),
        color=color, weight=BOLD,
    )
    initial.move_to(disc)
    label = Text(name, font_size=22, color=color, weight=BOLD)
    label.next_to(disc, DOWN, buff=0.18)
    g = VGroup(glow, ring, disc, initial, label)
    g.disc = disc
    g.ring = ring
    return g


class KeyIcon(VGroup):
    def __init__(self, color=RED_D, label="Private Key", scale_f=1.0, **kwargs):
        super().__init__(**kwargs)
        head = Circle(radius=0.2, color=color, fill_opacity=0.2, stroke_width=2.5)
        hole = Circle(radius=0.07, color=color, fill_opacity=0, stroke_width=1.5)
        hole.move_to(head)
        shaft = Line(
            head.get_right(), head.get_right() + RIGHT * 0.5,
            color=color, stroke_width=3,
        )
        teeth = VGroup()
        for frac, h in [(0.95, 0.14), (0.65, 0.11), (0.40, 0.08)]:
            pt = shaft.point_from_proportion(frac)
            teeth.add(Line(pt, pt + DOWN * h, color=color, stroke_width=3))
        glow = _soft_glow(head.get_center(), color, max_radius=0.4, peak_opacity=0.05)
        icon = VGroup(head, hole, shaft, teeth)
        self.icon = icon
        self.glow = glow
        self.lbl = Text(label, font_size=16, color=color)
        self.lbl.next_to(icon, DOWN, buff=0.14)
        self.add(glow, icon, self.lbl)
        self.scale(scale_f)


class CoinIcon(VGroup):
    def __init__(self, amount="1.0 BTC", color=GOLD_D, radius=0.38, **kwargs):
        super().__init__(**kwargs)
        glow = _soft_glow(ORIGIN, color, max_radius=radius * 1.7, peak_opacity=0.04)
        outer = Circle(radius=radius, color=color, fill_opacity=0.2, stroke_width=2.5)
        inner = Circle(
            radius=radius * 0.72, color=color,
            stroke_width=1.5, fill_opacity=0,
        )
        btc = Text("₿", font_size=int(radius * 55), color=color, weight=BOLD)
        btc.move_to(outer)
        highlight = Arc(
            radius=radius * 0.85, start_angle=PI * 0.55, angle=PI * 0.5,
            color=WHITE, stroke_width=1.5, stroke_opacity=0.12,
        )
        highlight.move_to(outer)
        self.coin_shape = VGroup(outer, inner, btc, highlight)
        self.amount_label = Text(amount, font_size=16, color=color, weight=BOLD)
        self.amount_label.next_to(outer, DOWN, buff=0.12)
        self.add(glow, self.coin_shape, self.amount_label)


class WalletCard(VGroup):
    def __init__(self, owner="Alice", color=BLUE_C, width=3.2, height=2.2, **kwargs):
        super().__init__(**kwargs)
        shadow = RoundedRectangle(
            width=width, height=height, corner_radius=0.15,
            color=BLACK, fill_opacity=0.25, stroke_width=0,
        )
        shadow.shift(DR * 0.07)
        body = RoundedRectangle(
            width=width, height=height, corner_radius=0.15,
            color=color, fill_opacity=0.06, stroke_width=2,
        )
        header = Rectangle(
            width=width - 0.08, height=0.38,
            color=color, fill_opacity=0.12, stroke_width=0,
        )
        header.next_to(body.get_top(), DOWN, buff=0.04)
        label = Text(f"{owner}'s Wallet", font_size=18, color=color, weight=BOLD)
        label.move_to(header)
        deco = VGroup()
        for i in range(3):
            y_off = -0.15 + i * 0.45
            l = Line(
                body.get_center() + LEFT * (width / 2 - 0.2) + DOWN * y_off,
                body.get_center() + RIGHT * (width / 2 - 0.2) + DOWN * y_off,
                color=color, stroke_width=0.5, stroke_opacity=0.12,
            )
            deco.add(l)
        self.body = body
        self.shadow = shadow
        self.header = header
        self.label = label
        self.flap = header
        self.add(shadow, body, header, label, deco)


class AddressLabel(VGroup):
    def __init__(self, address="1A1zP1...QGefi2", color=TEAL_C, **kwargs):
        super().__init__(**kwargs)
        box = RoundedRectangle(
            width=2.8, height=0.55, corner_radius=0.08,
            color=color, fill_opacity=0.1, stroke_width=2,
        )
        txt = Text(address, font_size=14, color=color)
        txt.move_to(box)
        self.add(box, txt)
        self.box = box
