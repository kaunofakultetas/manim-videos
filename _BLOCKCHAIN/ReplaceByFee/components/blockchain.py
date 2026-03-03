from manim import *

class Blockchain:
    def __init__(self, scene: Scene, anchor=LEFT*5.5 + DOWN*2.2, block_w=1.4, block_h=0.8):
        self.scene = scene
        self.block_w = block_w
        self.block_h = block_h
        self.group = VGroup()
        self.blocks = []
        self.lines = VGroup()
        self.title = Text("Blockchain", font_size=36)
        self.title.move_to(LEFT*5.5 + UP*2.8)
        scene.play(Write(self.title))
        # genesis
        genesis = self._make_block("0", color=WHITE).move_to(anchor)
        scene.play(Create(genesis))
        self.blocks.append(genesis)
        self.group.add(genesis)

    def _make_block(self, label: str, color=WHITE, txids=None):
        # Determine block height based on content
        has_tx = txids is not None and len(txids) > 0
        block_h = self.block_h * 1.5 if has_tx else self.block_h

        rect = Rectangle(width=self.block_w, height=block_h, color=color, fill_opacity=0.15)

        # Block number at the top
        block_label = Text(label, font_size=24, weight=BOLD)
        content = VGroup(block_label)

        if txids:
            tx_bubbles = VGroup()
            for txid in txids:
                bubble_radius = 0.18

                # RBF tx should be orange
                bubble_color = ORANGE if txid == "tx2" else BLUE_D
                
                bubble = Circle(radius=bubble_radius, color=bubble_color, fill_opacity=1.0)
                txid_text = Text(txid, font_size=18, weight=BOLD)
                if txid_text.width > bubble.width * 0.8:
                    txid_text.scale_to_fit_width(bubble.width * 0.8)
                tx_bubble = VGroup(bubble, txid_text)
                tx_bubbles.add(tx_bubble)
            
            tx_bubbles.arrange(DOWN, buff=0.1)
            content.add(tx_bubbles)

        content.arrange(DOWN, buff=0.15)
        content.move_to(rect.get_center())

        block = VGroup(rect, content)
        return block

    def add_block(self, label: str, txids: list[str] | None = None, color=YELLOW):
        prev = self.blocks[-1]
        
        # Calculate new block's height for positioning
        has_tx = txids is not None and len(txids) > 0
        new_block_h = self.block_h * 1.5 if has_tx else self.block_h
        
        # Position based on previous block's height and new block's height
        vertical_shift = (prev.height / 2) + (new_block_h / 2) + 0.18
        target_pos = prev.get_center() + UP * vertical_shift
        
        new_block = self._make_block(label, color=color, txids=txids).move_to(target_pos)
        self.scene.play(GrowFromCenter(new_block), run_time=0.7)
        line = Line(prev.get_top(), new_block.get_bottom(), color=YELLOW, stroke_width=4)
        self.scene.play(Create(line))
        self.blocks.append(new_block)
        self.group.add(new_block)
        self.lines.add(line)
        self.scene.wait(0.2)
        return new_block
