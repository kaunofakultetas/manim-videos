from manim import *


class UTXOCoin(VGroup):
    def __init__(self, amount, label="", color=GOLD_D, radius=0.28, **kwargs):
        super().__init__(**kwargs)
        outer = Circle(radius=radius, color=color, fill_opacity=0.2, stroke_width=2.5)
        amt = Text(amount, font_size=14, color=color, weight=BOLD)
        amt.move_to(outer)
        self.coin = VGroup(outer, amt)
        self.add(self.coin)
        if label:
            lbl = Text(label, font_size=12, color=GREY_B)
            lbl.next_to(outer, DOWN, buff=0.08)
            self.add(lbl)


class TransactionCard(VGroup):
    def __init__(self, txid="a4f2...c7e1", inputs=None, outputs=None,
                 fee="0.0001 BTC", width=5.6, **kwargs):
        super().__init__(**kwargs)
        height = 2.8
        shadow = RoundedRectangle(
            width=width, height=height, corner_radius=0.12,
            color=BLACK, fill_opacity=0.2, stroke_width=0,
        )
        shadow.shift(DR * 0.06)
        self.outer = RoundedRectangle(
            width=width, height=height, corner_radius=0.12,
            color="#4a6cf7", fill_opacity=0.04, stroke_width=2,
        )
        header = Rectangle(
            width=width - 0.08, height=0.35,
            color="#4a6cf7", fill_opacity=0.1, stroke_width=0,
        )
        header.next_to(self.outer.get_top(), DOWN, buff=0.04)
        txid_label = Text(f"TX  {txid}", font_size=15, color="#4a6cf7", weight=BOLD)
        txid_label.move_to(header)

        in_title = Text("Inputs", font_size=15, color="#f7b731", weight=BOLD)
        self.inputs_group = VGroup(in_title)
        if inputs:
            for inp in inputs:
                coin = UTXOCoin(
                    inp["amount"], label=inp.get("label", ""),
                    color="#f7b731", radius=0.26,
                )
                self.inputs_group.add(coin)
        self.inputs_group.arrange(DOWN, buff=0.1, aligned_edge=LEFT)

        out_title = Text("Outputs", font_size=15, color="#26de81", weight=BOLD)
        self.outputs_group = VGroup(out_title)
        if outputs:
            for out in outputs:
                coin = UTXOCoin(
                    out["amount"], label=out.get("label", ""),
                    color="#26de81", radius=0.26,
                )
                self.outputs_group.add(coin)
        self.outputs_group.arrange(DOWN, buff=0.1, aligned_edge=LEFT)

        arrow = Arrow(
            LEFT * 0.3, RIGHT * 0.3, color=GREY_B,
            stroke_width=2.5, buff=0,
            max_tip_length_to_length_ratio=0.35,
        )

        body = VGroup(self.inputs_group, arrow, self.outputs_group)
        body.arrange(RIGHT, buff=0.35)
        body.move_to(self.outer.get_center() + DOWN * 0.1)

        self.fee_label = Text(f"Fee: {fee}", font_size=13, color=ORANGE)
        self.fee_label.next_to(self.outer, DOWN, buff=0.1)

        self.shadow = shadow
        self.header = header
        self.txid_label = txid_label
        self.body = body
        self.add(shadow, self.outer, header, txid_label, body, self.fee_label)


class TxPacket(VGroup):
    def __init__(self, txid="tx", color=BLUE_D, radius=0.2, **kwargs):
        super().__init__(**kwargs)
        glow = VGroup()
        for i in range(4):
            t = (i + 1) / 4
            c = Circle(
                radius=radius * (1 + t * 0.8), color=color,
                fill_opacity=0.04 * (1 - t), stroke_width=0,
            )
            glow.add(c)
        self.circle = Circle(
            radius=radius, color=color, fill_opacity=0.85, stroke_width=2,
        )
        self.label = Text(txid, font_size=14, weight=BOLD)
        if self.label.width > self.circle.width * 0.8:
            self.label.scale_to_fit_width(self.circle.width * 0.8)
        self.label.move_to(self.circle)
        self.add(glow, self.circle, self.label)
