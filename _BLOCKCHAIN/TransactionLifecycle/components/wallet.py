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


class WalletBox(VGroup):
    def __init__(self, owner: str, color=BLUE_C, width=2.8, height=1.6, **kwargs):
        super().__init__(**kwargs)
        self.box = RoundedRectangle(
            width=width, height=height, corner_radius=0.12,
            color=color, fill_opacity=0.1, stroke_width=2.5,
        )
        self.label = Text(f"{owner}'s Wallet", font_size=22, color=color)
        self.label.next_to(self.box, UP, buff=0.12)
        self.add(self.box, self.label)


class KeyPair(VGroup):
    """Visual for a private/public key pair inside a wallet."""

    def __init__(self, priv_text="7a3f...e91b", pub_text="04c6...8d2a", **kwargs):
        super().__init__(**kwargs)

        priv_icon = VGroup(
            RoundedRectangle(width=1.8, height=0.5, corner_radius=0.06, color=RED_D,
                             fill_opacity=0.18, stroke_width=2),
            Text(f"Priv  {priv_text}", font_size=14, color=RED_D),
        )
        priv_icon[1].move_to(priv_icon[0])

        pub_icon = VGroup(
            RoundedRectangle(width=1.8, height=0.5, corner_radius=0.06, color=GREEN_D,
                             fill_opacity=0.18, stroke_width=2),
            Text(f"Pub  {pub_text}", font_size=14, color=GREEN_D),
        )
        pub_icon[1].move_to(pub_icon[0])

        self.priv = priv_icon
        self.pub = pub_icon
        VGroup(priv_icon, pub_icon).arrange(DOWN, buff=0.15)
        self.add(priv_icon, pub_icon)


class AddressLabel(VGroup):
    """A Bitcoin address derived from the public key."""

    def __init__(self, address="1A1zP1...QGefi2", color=TEAL_C, **kwargs):
        super().__init__(**kwargs)
        self.rect = RoundedRectangle(
            width=2.6, height=0.5, corner_radius=0.06,
            color=color, fill_opacity=0.15, stroke_width=2,
        )
        self.text = Text(f"Addr  {address}", font_size=14, color=color)
        self.text.move_to(self.rect)
        self.add(self.rect, self.text)
