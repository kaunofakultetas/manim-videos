from manim import *


class ChainBlock(VGroup):
    """A single block in the blockchain visualization."""

    def __init__(self, number: str, txids=None, color=BLUE, width=1.4, height=0.9,
                 font_size=20, tx_font_size=12, tx_radius=0.14, **kwargs):
        super().__init__(**kwargs)
        has_tx = txids is not None and len(txids) > 0
        actual_h = height * 1.4 if has_tx else height

        self.rect = Rectangle(
            width=width, height=actual_h,
            color=color, fill_opacity=0.4, stroke_width=2.5,
        )
        self.number_label = Text(f"#{number}", font_size=font_size, weight=BOLD, color=color)
        content = VGroup(self.number_label)

        if txids:
            self.tx_group = VGroup()
            for txid in txids:
                bubble = Circle(radius=tx_radius, color=GREEN_D, fill_opacity=0.8)
                tx_text = Text(txid, font_size=tx_font_size)
                if tx_text.width > bubble.width * 0.85:
                    tx_text.scale_to_fit_width(bubble.width * 0.85)
                tx_text.move_to(bubble)
                self.tx_group.add(VGroup(bubble, tx_text))
            self.tx_group.arrange(RIGHT, buff=0.06)
            content.add(self.tx_group)

        content.arrange(DOWN, buff=0.08)
        content.move_to(self.rect)
        self.add(self.rect, content)


class SimpleChain(VGroup):
    """A horizontal blockchain of blocks with connecting lines."""

    def __init__(self, block_width=1.4, block_height=0.9, block_gap=0.2,
                 font_size=20, tx_font_size=12, tx_radius=0.14,
                 start_pos=ORIGIN, **kwargs):
        super().__init__(**kwargs)
        self.blocks = []
        self.connectors = VGroup()
        self.block_width = block_width
        self.block_height = block_height
        self.block_gap = block_gap
        self.font_size = font_size
        self.tx_font_size = tx_font_size
        self.tx_radius = tx_radius
        self.start_pos = start_pos

    def add_block(self, scene: Scene, number: str, txids=None,
                  color=BLUE, animate=True):
        block = ChainBlock(number, txids=txids, color=color,
                           width=self.block_width, height=self.block_height,
                           font_size=self.font_size, tx_font_size=self.tx_font_size,
                           tx_radius=self.tx_radius)
        if self.blocks:
            prev = self.blocks[-1]
            block.next_to(prev, RIGHT, buff=self.block_gap)
        else:
            block.move_to(self.start_pos)
        self.blocks.append(block)
        self.add(block)

        if animate:
            scene.play(GrowFromCenter(block), run_time=0.5)

        if len(self.blocks) > 1:
            prev = self.blocks[-2]
            line = Line(
                prev.get_right(), block.get_left(),
                color=YELLOW_D, stroke_width=3,
            )
            self.connectors.add(line)
            self.add(line)
            if animate:
                scene.play(Create(line), run_time=0.25)

        return block
