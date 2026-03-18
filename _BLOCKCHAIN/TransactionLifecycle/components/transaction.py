from manim import *


class UTXOCoin(VGroup):
    """A coin-shaped UTXO with amount."""

    def __init__(self, amount: str, label: str = "", color=GOLD_D, radius=0.32, **kwargs):
        super().__init__(**kwargs)
        outer = Circle(radius=radius, color=color, fill_opacity=0.25, stroke_width=2.5)
        inner = Circle(radius=radius * 0.72, color=color, fill_opacity=0.0, stroke_width=1.5)
        amt = Text(amount, font_size=14, color=color, weight=BOLD)
        amt.move_to(outer)
        self.coin = VGroup(outer, inner, amt)
        self.add(self.coin)
        if label:
            lbl = Text(label, font_size=12, color=GREY_B)
            lbl.next_to(outer, DOWN, buff=0.08)
            self.add(lbl)


class TransactionEnvelope(VGroup):
    """Transaction visualised as an envelope being constructed."""

    def __init__(self, txid="a4f2...c7e1", width=5.6, height=2.8, **kwargs):
        super().__init__(**kwargs)
        self.env_body = RoundedRectangle(
            width=width, height=height, corner_radius=0.12,
            color=BLUE_D, fill_opacity=0.06, stroke_width=2.5,
        )
        flap_pts = [
            self.env_body.get_corner(UL),
            self.env_body.get_top() + DOWN * height * 0.3,
            self.env_body.get_corner(UR),
        ]
        self.flap = Polygon(*flap_pts, color=BLUE_D, fill_opacity=0.04, stroke_width=1.5)
        self.txid_label = Text(f"TX  {txid}", font_size=16, color=BLUE_C)
        self.txid_label.next_to(self.env_body, UP, buff=0.08)
        self.add(self.env_body, self.flap, self.txid_label)


class TransactionBox(VGroup):
    """Full visual of a Bitcoin transaction with inputs and outputs."""

    def __init__(self, txid="a4f2...c7e1", inputs=None, outputs=None,
                 fee="0.0001 BTC", width=5.4, **kwargs):
        super().__init__(**kwargs)

        self.outer = RoundedRectangle(
            width=width, height=2.6, corner_radius=0.1,
            color=BLUE_D, fill_opacity=0.06, stroke_width=2.5,
        )
        self.txid_label = Text(f"TX  {txid}", font_size=16, color=BLUE_C)
        self.txid_label.next_to(self.outer, UP, buff=0.1)

        in_title = Text("Inputs", font_size=16, color=GOLD_D, weight=BOLD)
        out_title = Text("Outputs", font_size=16, color=GREEN_D, weight=BOLD)

        self.inputs_group = VGroup(in_title)
        if inputs:
            for inp in inputs:
                coin = UTXOCoin(inp["amount"], label=inp.get("label", ""),
                                 color=GOLD_D, radius=0.28)
                self.inputs_group.add(coin)
        self.inputs_group.arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        self.outputs_group = VGroup(out_title)
        if outputs:
            for out in outputs:
                coin = UTXOCoin(out["amount"], label=out.get("label", ""),
                                 color=GREEN_D, radius=0.28)
                self.outputs_group.add(coin)
        self.outputs_group.arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        self.arrow_mob = Arrow(LEFT * 0.3, RIGHT * 0.3, color=GREY_B,
                                stroke_width=2.5, buff=0)
        body = VGroup(self.inputs_group, self.arrow_mob, self.outputs_group)
        body.arrange(RIGHT, buff=0.4)
        body.move_to(self.outer)

        self.fee_label = Text(f"Fee: {fee}", font_size=14, color=ORANGE)
        self.fee_label.next_to(self.outer, DOWN, buff=0.1)

        self.add(self.outer, self.txid_label, body, self.fee_label)
        self.body = body


class TxPacket(VGroup):
    """Small transaction packet for network propagation."""

    def __init__(self, txid="tx", color=BLUE_D, radius=0.22, **kwargs):
        super().__init__(**kwargs)
        self.circle = Circle(radius=radius, color=color, fill_opacity=0.85)
        self.label = Text(txid, font_size=16, weight=BOLD)
        if self.label.width > self.circle.width * 0.8:
            self.label.scale_to_fit_width(self.circle.width * 0.8)
        self.label.move_to(self.circle)
        self.add(self.circle, self.label)
