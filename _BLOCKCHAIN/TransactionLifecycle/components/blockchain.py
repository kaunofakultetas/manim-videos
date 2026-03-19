from manim import *
import numpy as np

DX = 0.22
DY = 0.18


class Block3D(VGroup):
    def __init__(self, number, txids=None, color=BLUE, width=1.3, height=0.8,
                 font_size=16, tx_font_size=10, tx_radius=0.10, **kwargs):
        super().__init__(**kwargs)
        has_tx = txids and len(txids) > 0
        h = height * 1.35 if has_tx else height

        front = Rectangle(
            width=width, height=h,
            color=color, fill_opacity=0.3, stroke_width=2,
        )
        ul = front.get_corner(UL)
        ur = front.get_corner(UR)
        dr = front.get_corner(DR)
        offset = np.array([DX, DY, 0])
        top_face = Polygon(
            ul, ur, ur + offset, ul + offset,
            color=color, fill_opacity=0.18, stroke_width=1.5,
        )
        side_face = Polygon(
            ur, dr, dr + offset, ur + offset,
            color=color, fill_opacity=0.12, stroke_width=1.5,
        )

        num_label = Text(f"#{number}", font_size=font_size, weight=BOLD, color=color)
        content = VGroup(num_label)

        if txids:
            tx_grp = VGroup()
            for txid in txids:
                bubble = Circle(
                    radius=tx_radius, color="#26de81",
                    fill_opacity=0.65, stroke_width=1.5,
                )
                txt = Text(txid, font_size=tx_font_size, weight=BOLD)
                if txt.width > bubble.width * 0.85:
                    txt.scale_to_fit_width(bubble.width * 0.85)
                txt.move_to(bubble)
                tx_grp.add(VGroup(bubble, txt))
            tx_grp.arrange(RIGHT, buff=0.05)
            content.add(tx_grp)

        content.arrange(DOWN, buff=0.07)
        content.move_to(front)

        self.front = front
        self.top_face = top_face
        self.side_face = side_face
        self.rect = front
        self.number_label = num_label
        self.add(side_face, top_face, front, content)


class BlockChain(VGroup):
    def __init__(self, start_pos=LEFT * 5.5, gap=0.15,
                 block_width=1.3, block_height=0.8,
                 font_size=16, tx_font_size=10, tx_radius=0.10, **kwargs):
        super().__init__(**kwargs)
        self.blocks = []
        self.connectors = VGroup()
        self.start_pos = start_pos
        self.gap = gap
        self.block_width = block_width
        self.block_height = block_height
        self.font_size = font_size
        self.tx_font_size = tx_font_size
        self.tx_radius = tx_radius

    def add_block(self, scene, number, txids=None, color=BLUE, animate=True):
        block = Block3D(
            number, txids=txids, color=color,
            width=self.block_width, height=self.block_height,
            font_size=self.font_size, tx_font_size=self.tx_font_size,
            tx_radius=self.tx_radius,
        )
        if self.blocks:
            block.next_to(self.blocks[-1], RIGHT, buff=self.gap)
        else:
            block.move_to(self.start_pos)
        self.blocks.append(block)
        self.add(block)

        if animate:
            scene.play(
                FadeIn(block, shift=UP * 0.25, scale=0.85),
                run_time=0.45,
            )

        if len(self.blocks) > 1:
            prev = self.blocks[-2]
            connector = Arrow(
                prev.get_right() + RIGHT * 0.02,
                block.get_left() + LEFT * 0.02,
                buff=0, color=YELLOW_D, stroke_width=2.5,
                max_tip_length_to_length_ratio=0.4,
            )
            self.connectors.add(connector)
            self.add(connector)
            if animate:
                scene.play(GrowArrow(connector), run_time=0.2)

        return block
