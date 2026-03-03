from manim import *

class Block(VGroup):
    def __init__(self, label, color=BLUE, **kwargs):
        super().__init__(**kwargs)
        rect = Rectangle(width=1.5, height=1, color=color, fill_opacity=0.5)
        text = Text(str(label), font_size=24).move_to(rect.get_center())
        self.add(rect, text)
        self.rect = rect
        self.label = text




class BlockchainForkResolution:
    @staticmethod
    def construct(scene: Scene, group: VGroup = VGroup()):
        """
        Main method to construct the blockchain fork animation within a scene.
        This method orchestrates the creation of the chain, the fork,
        and its resolution, adding all final mobjects to the provided group.
        """
        all_mobjects = VGroup()

        # 1. Create initial chain (blocks 1-3)
        initial_blocks = BlockchainForkResolution._create_initial_chain(scene)
        all_mobjects.add(*initial_blocks)
        
        # 2. Create, grow, and resolve the fork
        chain_tip = BlockchainForkResolution._create_and_resolve_fork(scene, initial_blocks[-1], all_mobjects)
        
        # 3. Continue the main chain with blocks 6 and 7
        block6 = BlockchainForkResolution._add_block_to_chain(scene, chain_tip, "6")
        block7 = BlockchainForkResolution._add_block_to_chain(scene, block6, "7")
        all_mobjects.add(block6, block7)
        
        scene.wait(1)
        
        # Add all persistent mobjects to the parent group for later animations
        group.add(all_mobjects)

    @staticmethod
    def _create_initial_chain(scene: Scene):
        """Creates and animates the first 3 blocks of the chain."""
        blocks = []
        prev_block = None
        for i in range(1, 4):
            block = Block(i)
            if prev_block:
                block.next_to(prev_block, RIGHT, buff=0.1)
            else:
                block.move_to(LEFT * 5)
            scene.play(FadeIn(block), run_time=0.5)
            blocks.append(block)
            prev_block = block
        return blocks

    @staticmethod
    def _create_and_resolve_fork(scene: Scene, last_block, all_mobjects_group):
        """
        Creates a fork, grows one branch, resolves the fork by choosing
        the longer chain, and returns the new tip of the blockchain.
        """
        # Mine 4th block (normal) which will be replaced by the fork
        block4 = Block(4)
        block4.next_to(last_block, RIGHT, buff=0.1)
        scene.play(FadeIn(block4), run_time=0.5)
        scene.wait(0.5)
        
        # Create two competing "4" blocks for the fork
        fork4_up = Block("4", color=RED)
        fork4_down = Block("4", color=RED)
        
        fork4_up.move_to(block4.get_center() + UP * 0.6)
        fork4_down.move_to(block4.get_center() + DOWN * 0.6)
        
        scene.play(
            ReplacementTransform(block4, fork4_up),
            FadeIn(fork4_down),
            run_time=1
        )
        all_mobjects_group.add(fork4_up)
        
        # Add a 5th block to the upper fork, making it the longer chain
        block5 = Block("5", color=RED)
        block5.next_to(fork4_up, RIGHT, buff=0.1)
        scene.play(FadeIn(block5), run_time=0.5)
        all_mobjects_group.add(block5)
        scene.wait(0.5)
        
        # Resolve fork: the shorter (lower) chain is discarded
        scene.play(FadeOut(fork4_down), run_time=0.5)
        
        # Move the winning fork blocks into the main chain's position
        target_pos_4 = last_block.get_center() + RIGHT * 1.6
        target_pos_5 = target_pos_4 + RIGHT * 1.6
        
        scene.play(
            fork4_up.animate.move_to(target_pos_4),
            block5.animate.move_to(target_pos_5),
            run_time=1
        )
        
        # Recolor the resolved fork blocks to match the main chain
        scene.play(
            fork4_up.rect.animate.set_color(BLUE).set_fill(BLUE, opacity=0.5),
            block5.rect.animate.set_color(BLUE).set_fill(BLUE, opacity=0.5),
            run_time=0.5
        )
        
        return block5  # The new tip of the chain

    @staticmethod
    def _add_block_to_chain(scene: Scene, prev_block, label, color=BLUE):
        """Adds a single new block next to the previous one."""
        block = Block(label, color=color)
        block.next_to(prev_block, RIGHT, buff=0.1)
        scene.play(FadeIn(block), run_time=0.5)
        scene.wait(0.5)
        return block
        