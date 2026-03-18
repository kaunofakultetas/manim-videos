from manim import *


def create_person(label: str, color=WHITE, font_size=24):
    body = Line(UP * 0.5, DOWN * 0.5)
    head = Circle(radius=0.25).next_to(body.get_start(), UP, buff=0)
    leg1 = Line(body.get_end(), body.get_end() + DOWN * 0.5 + LEFT * 0.3)
    leg2 = Line(body.get_end(), body.get_end() + DOWN * 0.5 + RIGHT * 0.3)
    arm1 = Line(body.get_center() + UP * 0.1, body.get_center() + LEFT * 0.4 + DOWN * 0.1)
    arm2 = Line(body.get_center() + UP * 0.1, body.get_center() + RIGHT * 0.4 + DOWN * 0.1)
    person_drawing = VGroup(body, head, leg1, leg2, arm1, arm2).set_color(color)
    person_label = Text(label, font_size=font_size).next_to(person_drawing, DOWN, buff=0.2)
    return VGroup(person_drawing, person_label)


class KeyIcon(VGroup):
    """A visual key icon built from basic shapes."""

    def __init__(self, color=RED_D, label="Private Key", scale_f=1.0, **kwargs):
        super().__init__(**kwargs)
        head = Circle(radius=0.18, color=color, fill_opacity=0.3, stroke_width=2.5)
        hole = Circle(radius=0.06, color=color, fill_opacity=0, stroke_width=2)
        hole.move_to(head)
        shaft = Line(head.get_right(), head.get_right() + RIGHT * 0.4,
                      color=color, stroke_width=3)
        tooth1 = Line(shaft.get_end(), shaft.get_end() + DOWN * 0.12,
                       color=color, stroke_width=3)
        tooth2 = Line(shaft.point_from_proportion(0.6),
                       shaft.point_from_proportion(0.6) + DOWN * 0.1,
                       color=color, stroke_width=3)
        icon = VGroup(head, hole, shaft, tooth1, tooth2)
        self.icon = icon
        self.lbl = Text(label, font_size=16, color=color)
        self.lbl.next_to(icon, DOWN, buff=0.12)
        self.add(icon, self.lbl)
        self.scale(scale_f)


class CoinIcon(VGroup):
    """A Bitcoin coin shape."""

    def __init__(self, amount="1.0 BTC", color=GOLD_D, radius=0.35, **kwargs):
        super().__init__(**kwargs)
        outer = Circle(radius=radius, color=color, fill_opacity=0.25, stroke_width=2.5)
        inner = Circle(radius=radius * 0.7, color=color, fill_opacity=0.0, stroke_width=1.5)
        btc = Text("₿", font_size=int(radius * 60), color=color, weight=BOLD)
        btc.move_to(outer)
        self.coin_shape = VGroup(outer, inner, btc)
        self.amount_label = Text(amount, font_size=16, color=color, weight=BOLD)
        self.amount_label.next_to(outer, DOWN, buff=0.1)
        self.add(self.coin_shape, self.amount_label)


class WalletShape(VGroup):
    """A wallet that looks like a wallet (folder-like shape with flap)."""

    def __init__(self, owner="Alice", color=BLUE_C, width=3.0, height=2.0, **kwargs):
        super().__init__(**kwargs)
        body = RoundedRectangle(width=width, height=height, corner_radius=0.15,
                                 color=color, fill_opacity=0.08, stroke_width=2.5)
        flap = RoundedRectangle(width=width * 0.4, height=height * 0.25, corner_radius=0.08,
                                 color=color, fill_opacity=0.15, stroke_width=2)
        flap.move_to(body.get_top() + DOWN * flap.height / 2, aligned_edge=UP)
        flap.align_to(body, RIGHT).shift(LEFT * 0.1)
        clasp = Circle(radius=0.06, color=color, fill_opacity=0.5)
        clasp.move_to(flap.get_bottom() + DOWN * 0.02)
        self.body = body
        self.flap = flap
        label = Text(f"{owner}'s Wallet", font_size=20, color=color)
        label.next_to(body, UP, buff=0.12)
        self.label = label
        self.add(body, flap, clasp, label)


class AddressLabel(VGroup):
    """A Bitcoin address with a mailbox-like icon."""

    def __init__(self, address="1A1zP1...QGefi2", color=TEAL_C, **kwargs):
        super().__init__(**kwargs)
        box = RoundedRectangle(width=2.6, height=0.55, corner_radius=0.06,
                                color=color, fill_opacity=0.12, stroke_width=2)
        flag = Rectangle(width=0.08, height=0.25, color=color, fill_opacity=0.7)
        flag.next_to(box, LEFT, buff=0.0).shift(UP * 0.08)
        txt = Text(address, font_size=14, color=color)
        txt.move_to(box)
        self.add(box, flag, txt)
        self.box = box
