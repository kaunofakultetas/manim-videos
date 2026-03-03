from manim import *

class Mempool:
    def __init__(self, scene: Scene, center=RIGHT*4 + DOWN*0, width=5.2, height=5.0):
        self.scene = scene
        self.width = width
        self.height = height
        self.container = RoundedRectangle(width=width, height=height, corner_radius=0.15, color=BLUE_C)
        self.container.move_to(center)
        self.title = Text("Mempool", font_size=36).next_to(self.container.get_top(), DOWN, buff=0.25)
        self.items_group = VGroup()
        scene.play(Create(self.container), Write(self.title))
        scene.wait(0.25)
        self._reflow()

        # book-keeping
        self.items = {}  # txid -> VGroup
        self.cloud = None  # optional: MempoolCloud reference

    def _reflow(self):
        if len(self.items_group) == 0:
            return
        self.items_group.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        self.items_group.next_to(self.title, DOWN, buff=0.3)
        self.items_group.align_to(self.container, LEFT).shift(RIGHT*0.25)

    def _make_tx_item(self, txid: str, desc: str, fee_label: str, color=BLUE_E, rbf=False):
        rect = RoundedRectangle(
            width=self.width - 0.5,
            height=0.7,
            corner_radius=0.08,
            color=color,
            fill_opacity=0.12
        )

        # Bubble for txid
        bubble_radius = 0.25
        bubble = Circle(radius=bubble_radius, color=color, fill_opacity=1.0)
        txid_text = Text(txid, font_size=24, weight=BOLD)
        if txid_text.width > bubble.width * 0.8:
            txid_text.scale_to_fit_width(bubble.width * 0.8)
        txid_bubble = VGroup(bubble, txid_text)

        # Main description text (RBF flag is no longer displayed)
        main_text = Text(
            f"{desc}\n{fee_label}",
            font_size=22,
            line_spacing=0.9
        )

        # Position bubble and text within the rectangle
        txid_bubble.align_to(rect, LEFT).shift(RIGHT * (bubble_radius + 0.15))
        main_text.next_to(txid_bubble, RIGHT, buff=0.3)

        group = VGroup(rect, txid_bubble, main_text)
        return group

    def add_tx(self, txid: str, desc: str, fee_label: str, color=BLUE_E, rbf=False, appear_from=None):
        if txid in self.items:
            return self.items[txid]
        item = self._make_tx_item(txid, desc, fee_label, color=color, rbf=rbf)
        self.items_group.add(item)
        self.scene.add(item)
        # initial pos
        start_pos = appear_from if appear_from is not None else (self.container.get_right() + RIGHT*0.6)
        item.move_to(start_pos)
        self._reflow()
        self.scene.play(item.animate.move_to(item.get_center()), run_time=0.6)
        self.scene.wait(0.1)
        self.items[txid] = item

        # sync to cloud
        if self.cloud is not None:
            self.cloud.add_tx(txid=txid, color=color)

        return item

    def replace_by_fee(self, old_txid: str, new_txid: str, desc: str, fee_label: str, color=ORANGE, rbf=True):
        if old_txid not in self.items:
            return None
        old_item = self.items[old_txid]
        cross = Cross(old_item[0], color=RED)
        rbf_tag = Text("Replace-By-Fee", font_size=24, color=ORANGE).next_to(old_item, UP, buff=0.1)
        self.scene.play(Create(cross), FadeIn(rbf_tag, shift=UP*0.2))
        self.scene.wait(0.2)
        # remove old, add new
        self.scene.play(FadeOut(old_item), FadeOut(cross), FadeOut(rbf_tag), run_time=0.5)
        self.items_group.remove(old_item)
        del self.items[old_txid]

        # sync cloud removal
        if self.cloud is not None:
            self.cloud.pop_tx(old_txid)

        # add replacement
        new_item = self.add_tx(new_txid, desc, fee_label, color=color, rbf=rbf)
        self._reflow()
        self.scene.play(Indicate(new_item, color=ORANGE))

        # ensure cloud bubble uses new color too
        if self.cloud is not None:
            self.cloud.add_tx(txid=new_txid, color=color)

        return new_item

    def pop_tx(self, txid: str):
        if txid not in self.items:
            return None
        item = self.items[txid]
        self.items_group.remove(item)
        del self.items[txid]
        self._reflow()

        # sync to cloud
        if self.cloud is not None:
            self.cloud.pop_tx(txid)

        return item

class MempoolCloud:
    def __init__(self, scene: Scene, near_block: VGroup, block_w: float = 1.4, block_h: float = 0.8):
        self.scene = scene
        self.bubbles = {}
        self.bubbles_group = VGroup()
        self.block_h = block_h  # Store for updates

        # Cloud shape (small, roughly block-sized)
        c1 = Circle(radius=0.28)
        c2 = Circle(radius=0.22).shift(LEFT*0.28 + DOWN*0.02)
        c3 = Circle(radius=0.24).shift(RIGHT*0.28 + DOWN*0.03)
        c4 = Circle(radius=0.18).shift(UP*0.22 + LEFT*0.12)
        c5 = Circle(radius=0.16).shift(UP*0.18 + RIGHT*0.14)
        self.cloud = Union(c1, c2, c3, c4, c5, color=BLUE_C, fill_opacity=0.15, stroke_width=3)
        self.cloud.scale_to_fit_width(block_w*1.7)

        anchor = near_block.get_top() + UP*(block_h*1.4)
        self.cloud.move_to(anchor)

        self.title = Text("Mempool", font_size=22).next_to(self.cloud, UP, buff=0.12)

        self.group = VGroup(self.cloud, self.title, self.bubbles_group)
        scene.play(Create(self.cloud), Write(self.title))

    def _reflow(self):
        if len(self.bubbles_group) == 0:
            return
        self.bubbles_group.arrange(RIGHT, buff=0.12)
        self.bubbles_group.move_to(self.cloud.get_center())

    def add_tx(self, txid: str, color=BLUE_E):
        if txid in self.bubbles:
            # update color if needed
            bubble = self.bubbles[txid][0]
            bubble.set_color(color)
            bubble.set_fill(color, opacity=0.30)
            return self.bubbles[txid]

        bubble = Circle(radius=0.16, color=color, fill_opacity=0.30)
        label = Text(txid, font_size=16)
        if label.width > bubble.width*0.9:
            label.scale_to_fit_width(bubble.width*0.9)
        label.move_to(bubble.get_center())
        vg = VGroup(bubble, label)

        self.bubbles_group.add(vg)
        self.scene.add(vg)
        vg.move_to(self.cloud.get_center())
        self._reflow()
        self.scene.play(FadeIn(vg, scale=0.85), run_time=0.3)
        self.bubbles[txid] = vg
        return vg

    def pop_tx(self, txid: str):
        if txid not in self.bubbles:
            return None
        vg = self.bubbles[txid]
        self.bubbles_group.remove(vg)
        del self.bubbles[txid]
        self.scene.play(FadeOut(vg), run_time=0.25)
        self._reflow()
        return vg

    def update_position(self, near_block: VGroup, animate: bool = True):
        """Moves the entire cloud assembly based on the position of a target block."""
        target_anchor = near_block.get_top() + UP * (self.block_h * 1.4)
        current_anchor = self.cloud.get_center()
        delta = target_anchor - current_anchor

        if animate:
            self.scene.play(self.group.animate.shift(delta), run_time=0.5)
        else:
            self.group.shift(delta)
