from manim import *

from components.mempool import Mempool, MempoolCloud
from components.blockchain import Blockchain
from components.actors import create_person, create_network

class Main(Scene):
    def construct(self):
        # Title
        title = Paragraph("Double spend attack using \nReplace-By-Fee transactions", font_size=58, alignment="center")
        self.play(Write(title))
        self.wait(0.6)
        self.play(title.animate.scale(0.5).to_edge(UP))

        # Views
        chain = Blockchain(self)
        mempool_cloud = MempoolCloud(self, near_block=chain.blocks[-1], block_w=chain.block_w, block_h=chain.block_h)
        mempool = Mempool(self)

        # Indicate these two are the same mempool
        link1 = Arrow(mempool_cloud.cloud.get_right(), mempool.container.get_left(), buff=0.2, color=BLUE_C)
        link2 = Arrow(mempool.container.get_left(), mempool_cloud.cloud.get_right(), buff=0.2, color=BLUE_C)
        same_lbl = Text("same mempool", font_size=22, color=BLUE_C).next_to(link1, UP, buff=0.1)
        self.play(Create(link1), Create(link2), FadeIn(same_lbl))
        self.wait(0.6)
        self.play(FadeOut(link1), FadeOut(link2), FadeOut(same_lbl))

        # tie them together for syncing
        mempool.cloud = mempool_cloud

        # ---- Story Scene ----
        # 1. Fade out main UI to focus on the story
        main_ui = VGroup(chain.group, chain.title, mempool.container, mempool.title, mempool.items_group, mempool_cloud.group)
        self.play(FadeOut(main_ui))

        # 2. Create actors and network
        attacker = create_person("Attacker", color=RED_E).move_to(LEFT * 4.5)
        merchant = create_person("Merchant", color=GREEN_C).move_to(RIGHT * 4.5)
        network = create_network().scale(0.9)
        caption = Text("", font_size=30).to_edge(DOWN)

        # Create and position "Goods" package from the start
        goods_square = Square(side_length=0.5, color=ORANGE, fill_opacity=0.8)
        goods_label = Text("Goods", font_size=16).next_to(goods_square, DOWN, buff=0.1)
        package = VGroup(goods_square, goods_label)
        package.next_to(merchant, DOWN, buff=0.2) # Position relative to the whole person group

        self.play(
            FadeIn(attacker, shift=LEFT),
            FadeIn(merchant, shift=RIGHT),
            Create(network),
            FadeIn(package)
        )
        self.wait(0.5)

        # 3. Attacker sends low-fee tx
        self.play(Transform(caption, Text("1. Attacker sends a low-fee transaction to the Merchant", font_size=30).to_edge(DOWN)))
        tx1_packet = VGroup(
            Circle(radius=0.2, color=BLUE_E, fill_opacity=1.0), 
            Text("tx1", font_size=20)
        ).move_to(attacker.get_center())
        
        self.play(tx1_packet.animate.move_to(network.get_center()))
        self.play(Circumscribe(network, color=BLUE_E))

        # Propagate copy to merchant
        tx1_copy = tx1_packet.copy()
        self.play(tx1_copy.animate.move_to(merchant.get_center()))
        self.play(FadeOut(tx1_copy))
        self.wait(0.5)

        # 4. Merchant sees it (zero-conf) and gives goods
        self.play(Transform(caption, Text("2. Merchant sees the unconfirmed transaction and hands over the goods", font_size=30).to_edge(DOWN)))
        
        # Animate package to a position below the attacker, where it will stay
        self.play(package.animate.next_to(attacker, DOWN, buff=0.2)) # Position relative to the whole person group
        self.wait(0.5)
        
        # 5. Attacker sends RBF tx
        self.play(Transform(caption, Text("3. Attacker immediately sends a conflicting, higher-fee transaction", font_size=30).to_edge(DOWN)))
        tx2_packet = VGroup(
            Circle(radius=0.2, color=ORANGE, fill_opacity=1.0),
            Text("tx2", font_size=20)
        ).move_to(attacker.get_center())
        self.play(tx2_packet.animate.move_to(network.get_center()))
        self.play(FadeOut(tx1_packet), run_time=0.3) # tx2 replaces tx1 in the network
        self.play(Circumscribe(network, color=ORANGE))

        # Propagate copy to merchant
        tx2_copy = tx2_packet.copy()
        self.play(tx2_copy.animate.move_to(merchant.get_center()))
        self.play(FadeOut(tx2_copy))
        self.wait(0.5)

        # 6. Transition back to main UI
        story_scene = VGroup(attacker, merchant, network, tx2_packet, caption, package)
        self.play(FadeOut(story_scene))
        self.play(FadeIn(main_ui))
        self.wait(0.5)
        # ---- End Story Scene ----

        # Step 1: Low-fee RBF transaction enters mempool
        caption = Text("1) Broadcast low-fee tx signaling RBF", font_size=30).to_edge(DOWN)
        self.play(FadeIn(caption, shift=UP*0.2))
        tx1 = mempool.add_tx(
            "tx1",
            "Alice -> Bob 0.010 BTC",
            "fee 1 sat/vB",
            color=BLUE_E,
            rbf=True
        )
        self.play(Circumscribe(tx1, color=BLUE), run_time=0.9)
        self.wait(0.5)

        # Step 2: Merchant risk (unconfirmed)
        line1 = Text("Merchant sees unconfirmed", font_size=28, color=GREY_B)
        line2 = Text("payment", font_size=28, color=GREY_B)
        merchant_note = VGroup(line1, line2).arrange(DOWN, buff=0.15)
        merchant_note.next_to(tx1, DOWN, buff=0.25)

        self.play(FadeIn(merchant_note))
        self.wait(0.6)
        self.play(FadeOut(merchant_note))

        # Step 3: Replacement with higher fee (conflicting input)
        self.play(Transform(caption, Text("2) Replacement tx with higher fee is broadcast", font_size=30).to_edge(DOWN)))
        tx2 = mempool.replace_by_fee(
            "tx1",
            "tx2",
            "Alice -> Alice 0.010 BTC",
            "fee 20 sat/vB",
            color=ORANGE,
            rbf=True
        )
        self.wait(0.4)

        # Step 4: Miner selects higher-fee tx and mines a block
        self.play(Transform(caption, Text("3) Miner selects higher-fee tx and mines next block", font_size=30).to_edge(DOWN)))
        
        # Calculate future block position for the arrow target
        last_block = chain.blocks[-1]
        future_block_center = last_block.get_center() + UP * (last_block.height / 2 + (chain.block_h * 1.5) / 2 + 0.18)

        pick_arrow = Arrow(mempool.container.get_left(), last_block.get_center() + UP, buff=0.25, color=YELLOW)
        self.play(Create(pick_arrow))
        self.play(Indicate(tx2, color=YELLOW))
        self.wait(0.2)

        # Remove tx2 from mempool (mined) and add block with tx2
        mined_item = mempool.pop_tx("tx2")
        if mined_item is not None:
            self.play(mined_item.animate.move_to(chain.blocks[-1].get_right()+RIGHT*1.2).set_opacity(0.0), FadeOut(pick_arrow), run_time=0.6)
        
        # Make space for the new block by moving the cloud first
        last_block = chain.blocks[-1]

        # Correctly calculate future block position and create a dummy with the right height
        new_block_h = chain.block_h * 1.5 # We know tx block is larger
        vertical_shift = (last_block.height / 2) + (new_block_h / 2) + 0.18
        future_block_center = last_block.get_center() + UP * vertical_shift
        
        dummy_block = Rectangle(height=new_block_h, width=chain.block_w).move_to(future_block_center)
        mempool_cloud.update_position(dummy_block)

        block1 = chain.add_block("1", txids=["tx2"], color=GREEN)
        self.play(Circumscribe(block1, color=GREEN))
        self.wait(0.3)

        # Step 5: Outcome – double spend succeeds against zero-conf
        self.play(Transform(caption, Text("Outcome: Bob's unconfirmed tx did not confirm (double spend succeeded)", font_size=30).to_edge(DOWN)))
        self.wait(1.5)

        # --- Final Scene ---
        # Fade out everything except the title and caption
        final_ui_elements = VGroup(chain.group, chain.lines, chain.title, mempool.container, mempool.title, mempool.items_group, mempool_cloud.group)
        self.play(FadeOut(final_ui_elements), run_time=0.8)

        # Display final messages in the center
        danger = Text("Risk: zero-conf payments are unsafe with RBF", font_size=32, color=RED_E).move_to(UP * 0.5)
        self.play(FadeIn(danger, shift=UP*0.2))
        self.wait(2)

        best = Text("Best practice: wait for confirmations", font_size=34, color=YELLOW_E).next_to(danger, DOWN, buff=0.5)
        self.play(FadeIn(best))
        self.wait(2)

        # Outro
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.2)




