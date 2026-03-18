from manim import *


class UTXOBox(VGroup):
    """Visual representation of an Unspent Transaction Output."""

    def __init__(self, amount: str, label: str = "", color=GOLD_D, width=2.0, height=0.55, **kwargs):
        super().__init__(**kwargs)
        self.rect = RoundedRectangle(
            width=width, height=height, corner_radius=0.06,
            color=color, fill_opacity=0.2, stroke_width=2,
        )
        self.amount_text = Text(amount, font_size=18, color=color, weight=BOLD)
        self.amount_text.move_to(self.rect)
        self.add(self.rect, self.amount_text)
        if label:
            self.lbl = Text(label, font_size=14, color=GREY_B)
            self.lbl.next_to(self.rect, DOWN, buff=0.08)
            self.add(self.lbl)


class TransactionBox(VGroup):
    """Full visual of a Bitcoin transaction with inputs and outputs."""

    def __init__(self, txid="a4f2...c7e1", inputs=None, outputs=None,
                 fee="0.0001 BTC", width=5.0, **kwargs):
        super().__init__(**kwargs)

        self.outer = RoundedRectangle(
            width=width, height=2.6, corner_radius=0.1,
            color=BLUE_D, fill_opacity=0.08, stroke_width=2.5,
        )
        self.txid_label = Text(f"TX  {txid}", font_size=16, color=BLUE_C)
        self.txid_label.next_to(self.outer, UP, buff=0.1)

        in_title = Text("Inputs", font_size=16, color=GOLD_D, weight=BOLD)
        out_title = Text("Outputs", font_size=16, color=GREEN_D, weight=BOLD)

        self.inputs_group = VGroup(in_title)
        if inputs:
            for inp in inputs:
                box = UTXOBox(inp["amount"], label=inp.get("label", ""), color=GOLD_D, width=1.9)
                self.inputs_group.add(box)
        self.inputs_group.arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        self.outputs_group = VGroup(out_title)
        if outputs:
            for out in outputs:
                box = UTXOBox(out["amount"], label=out.get("label", ""), color=GREEN_D, width=1.9)
                self.outputs_group.add(box)
        self.outputs_group.arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        arrow = Text("→", font_size=36, color=GREY_B)
        body = VGroup(self.inputs_group, arrow, self.outputs_group).arrange(RIGHT, buff=0.35)
        body.move_to(self.outer)

        self.fee_label = Text(f"Fee: {fee}", font_size=14, color=ORANGE)
        self.fee_label.next_to(self.outer, DOWN, buff=0.1)

        self.add(self.outer, self.txid_label, body, self.fee_label)

        self.arrow_mob = arrow
        self.body = body


class TxPacket(VGroup):
    """Small transaction packet for network propagation animations."""

    def __init__(self, txid="tx", color=BLUE_D, radius=0.22, **kwargs):
        super().__init__(**kwargs)
        self.circle = Circle(radius=radius, color=color, fill_opacity=0.9)
        self.label = Text(txid, font_size=16, weight=BOLD)
        if self.label.width > self.circle.width * 0.8:
            self.label.scale_to_fit_width(self.circle.width * 0.8)
        self.label.move_to(self.circle)
        self.add(self.circle, self.label)
