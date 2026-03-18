from manim import *
import numpy as np

from components.wallet import (create_person, KeyIcon, CoinIcon,
                                WalletShape, AddressLabel)
from components.transaction import UTXOCoin, TransactionBox, TxPacket
from components.network import P2PNetwork, MempoolPool
from components.blockchain import SimpleChain, ChainBlock


BG_COLOR = "#0e0e0e"
ACCENT = "#ffd866"


class Main(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        self.step = 0

        self._build_bg_grid()
        self.scene_title()
        self.scene_wallet_and_keys()
        self.scene_construct_transaction()
        self.scene_digital_signing()
        self.scene_broadcast()
        self.scene_mempool_validation()
        self.scene_mining()
        self.scene_confirmations()
        self.scene_outro()

    # ============================================================ bg grid
    def _build_bg_grid(self):
        dots = VGroup()
        for x in np.arange(-7, 7.5, 1.0):
            for y in np.arange(-4, 4.5, 1.0):
                d = Dot(point=[x, y, 0], radius=0.015, color=GREY_E)
                d.set_opacity(0.25)
                dots.add(d)
        self.bg_grid = dots
        self.add(dots)

    # ============================================================ progress
    def _show_progress(self, step: int, total: int = 7):
        bar_w = 4.0
        bar_h = 0.06
        bar_bg = RoundedRectangle(width=bar_w, height=bar_h, corner_radius=0.03,
                                   color=GREY_E, fill_opacity=0.3, stroke_width=0)
        fill_w = max(0.08, bar_w * step / total)
        bar_fill = RoundedRectangle(width=fill_w, height=bar_h, corner_radius=0.03,
                                     color=YELLOW_D, fill_opacity=0.8, stroke_width=0)
        bar_fill.align_to(bar_bg, LEFT)
        label = Text(f"{step}/{total}", font_size=12, color=GREY_B)
        label.next_to(bar_bg, RIGHT, buff=0.15)
        progress = VGroup(bar_bg, bar_fill, label)
        progress.to_corner(DR, buff=0.3)

        if hasattr(self, '_progress_bar'):
            self.play(ReplacementTransform(self._progress_bar, progress), run_time=0.3)
        else:
            self.play(FadeIn(progress, shift=UP * 0.1), run_time=0.3)
        self._progress_bar = progress

    # ============================================================ caption
    def _caption(self, text: str, color=WHITE):
        return Text(text, font_size=26, color=color).to_edge(DOWN, buff=0.35)

    def _update_caption(self, old_caption, new_text, color=WHITE):
        new_cap = self._caption(new_text, color)
        self.play(ReplacementTransform(old_caption, new_cap), run_time=0.5)
        return new_cap

    # ============================================================ zoom
    def _zoom_to(self, center, scale=1.0, run_time=0.8):
        frame = self.camera.frame
        self.play(
            frame.animate.set(width=14.2 / scale).move_to(center),
            run_time=run_time,
        )

    def _zoom_reset(self, run_time=0.6):
        frame = self.camera.frame
        self.play(frame.animate.set(width=14.2).move_to(ORIGIN), run_time=run_time)

    # ============================================================ title
    def scene_title(self):
        title_top = Text("The Lifecycle of a", font_size=38, color=GREY_B)
        title_bot = Text("Bitcoin Transaction", font_size=56, weight=BOLD)
        title = VGroup(title_top, title_bot).arrange(DOWN, buff=0.2)

        underline = Line(LEFT * 3.8, RIGHT * 3.8, color=YELLOW_D, stroke_width=2.5)
        underline.next_to(title, DOWN, buff=0.25)

        self.play(FadeIn(title_top, shift=DOWN * 0.3), run_time=0.6)
        self.play(Write(title_bot), run_time=1.0)
        self.play(Create(underline), run_time=0.4)
        self.wait(0.8)

        target_title = title_bot.copy().scale(0.35)
        target_title.to_edge(UP, buff=0.18)
        self.play(
            FadeOut(title_top), FadeOut(underline),
            ReplacementTransform(title_bot, target_title),
            run_time=0.8,
        )
        self.top_title = target_title

    # ============================================ 1. wallet & keys
    def scene_wallet_and_keys(self):
        self._show_progress(1)
        cap = self._caption("Step 1 — Alice creates a wallet")

        alice = create_person("Alice", color=BLUE_C).scale(0.75)
        alice.move_to(LEFT * 5 + UP * 0.3)
        self.play(alice.shift(LEFT * 2).animate.shift(RIGHT * 2), run_time=0.7)

        wallet = WalletShape("Alice", color=BLUE_C, width=3.4, height=2.0)
        wallet.move_to(RIGHT * 0.5 + UP * 0.5)
        self.play(
            DrawBorderThenFill(wallet.body, run_time=0.7),
            FadeIn(wallet.flap, shift=DOWN * 0.1),
            Write(wallet.label),
        )
        self.wait(0.3)

        cap = self._update_caption(cap, "A wallet is really just a pair of cryptographic keys")

        priv_key = KeyIcon(color=RED_D, label="Private Key", scale_f=1.2)
        priv_key.move_to(wallet.body.get_center() + UP * 0.35)
        pub_key = KeyIcon(color=GREEN_D, label="Public Key", scale_f=1.2)
        pub_key.move_to(wallet.body.get_center() + DOWN * 0.35)

        self.play(FadeIn(priv_key, shift=RIGHT * 0.4), run_time=0.5)
        priv_note = Text("Keep secret!", font_size=15, color=RED_D)
        priv_note.next_to(priv_key, RIGHT, buff=0.3)
        self.play(FadeIn(priv_note, shift=LEFT * 0.1), run_time=0.3)

        self.play(FadeIn(pub_key, shift=RIGHT * 0.4), run_time=0.5)
        pub_note = Text("Share with anyone", font_size=15, color=GREEN_D)
        pub_note.next_to(pub_key, RIGHT, buff=0.3)
        self.play(FadeIn(pub_note, shift=LEFT * 0.1), run_time=0.3)
        self.wait(0.4)

        cap = self._update_caption(cap, "The public key is hashed into a Bitcoin address")

        addr = AddressLabel("1A1zP1...QGefi2", color=TEAL_C)
        addr.move_to(DOWN * 1.4 + RIGHT * 0.5)
        arrow = CurvedArrow(pub_key.get_bottom() + DOWN * 0.05,
                             addr.get_top() + UP * 0.05,
                             color=TEAL_C, stroke_width=2.5, angle=-0.3)
        hash_lbl = Text("Hash", font_size=14, color=TEAL_C)
        hash_lbl.next_to(arrow, RIGHT, buff=0.08)

        self.play(Create(arrow), FadeIn(hash_lbl), run_time=0.5)
        self.play(GrowFromCenter(addr), run_time=0.5)
        self.play(Circumscribe(addr, color=TEAL_C, buff=0.05), run_time=0.5)
        self.wait(0.6)

        scene_group = VGroup(alice, wallet, priv_key, pub_key, priv_note,
                              pub_note, addr, arrow, hash_lbl)
        self.play(FadeOut(scene_group, shift=LEFT * 0.5), FadeOut(cap), run_time=0.5)

    # ========================================= 2. construct transaction
    def scene_construct_transaction(self):
        self._show_progress(2)
        cap = self._caption("Step 2 — Alice builds a transaction to pay Bob")

        alice = create_person("Alice", color=BLUE_C).scale(0.65)
        alice.move_to(LEFT * 5.5 + UP * 1.5)
        bob = create_person("Bob", color=GREEN_C).scale(0.65)
        bob.move_to(RIGHT * 5.5 + UP * 1.5)
        self.play(
            alice.shift(LEFT * 1).animate.shift(RIGHT * 1),
            bob.shift(RIGHT * 1).animate.shift(LEFT * 1),
            run_time=0.6,
        )

        thought = Text("\"I want to send Bob 0.5 BTC\"", font_size=20, color=GREY_B,
                         slant=ITALIC)
        thought.next_to(alice, RIGHT, buff=0.3).shift(UP * 0.3)
        self.play(FadeIn(thought, shift=UP * 0.15), run_time=0.4)
        self.wait(0.5)
        self.play(FadeOut(thought), run_time=0.3)

        cap = self._update_caption(cap, "She has an unspent coin (UTXO) worth 1.0 BTC")

        coin = CoinIcon("1.0 BTC", color=GOLD_D, radius=0.4)
        coin.move_to(LEFT * 3.5 + DOWN * 0.3)
        coin_label = Text("Alice's unspent coin", font_size=16, color=GOLD_D)
        coin_label.next_to(coin, DOWN, buff=0.25)
        self.play(GrowFromCenter(coin), FadeIn(coin_label, shift=UP * 0.1), run_time=0.6)
        self.wait(0.5)

        cap = self._update_caption(cap, "She spends the coin, creating new outputs for Bob and herself")

        tx = TransactionBox(
            txid="a4f2...c7e1",
            inputs=[{"amount": "1.0 BTC", "label": "Alice's coin"}],
            outputs=[
                {"amount": "0.5 BTC", "label": "→ Bob"},
                {"amount": "0.4999", "label": "→ Alice (change)"},
            ],
            fee="0.0001 BTC",
            width=5.4,
        )
        tx.move_to(DOWN * 0.3)

        self.play(
            coin.animate.move_to(tx.inputs_group.get_center()).scale(0.01).set_opacity(0),
            FadeOut(coin_label),
            run_time=0.6,
        )
        self.remove(coin)
        self.play(FadeIn(tx, shift=UP * 0.2), run_time=0.7)
        self.wait(0.3)

        self.play(Indicate(tx.inputs_group, color=GOLD_D, scale_factor=1.05), run_time=0.5)
        self.play(Indicate(tx.outputs_group, color=GREEN_D, scale_factor=1.05), run_time=0.5)
        self.play(Indicate(tx.fee_label, color=ORANGE, scale_factor=1.1), run_time=0.4)
        self.wait(0.6)

        self.tx_box = tx
        self.play(FadeOut(alice, shift=LEFT * 0.5), FadeOut(bob, shift=RIGHT * 0.5),
                  FadeOut(cap), run_time=0.5)

    # ============================================= 3. digital signing
    def scene_digital_signing(self):
        self._show_progress(3)
        cap = self._caption("Step 3 — Alice signs the transaction with her private key")

        tx = self.tx_box
        self.play(tx.animate.move_to(RIGHT * 1.5 + DOWN * 0.1).scale(0.9), run_time=0.5)

        priv_key = KeyIcon(color=RED_D, label="Alice's Private Key", scale_f=1.4)
        priv_key.move_to(LEFT * 4.5 + UP * 0.5)
        self.play(priv_key.shift(LEFT * 1.5).animate.shift(RIGHT * 1.5), run_time=0.6)
        self.wait(0.2)

        cap = self._update_caption(cap, "The private key creates a unique digital signature")

        sign_arrow = CurvedArrow(priv_key.get_right() + RIGHT * 0.1,
                                  tx.get_left() + LEFT * 0.1 + UP * 0.2,
                                  color=YELLOW_D, stroke_width=2.5, angle=-0.4)
        sign_label = Text("Signs", font_size=16, color=YELLOW_D)
        sign_label.next_to(sign_arrow, UP, buff=0.05)
        self.play(Create(sign_arrow), FadeIn(sign_label), run_time=0.6)
        self.wait(0.2)

        lock = VGroup(
            RoundedRectangle(width=0.5, height=0.4, corner_radius=0.04,
                             color=YELLOW_D, fill_opacity=0.3, stroke_width=2.5),
            Arc(radius=0.15, start_angle=0, angle=PI, color=YELLOW_D, stroke_width=3)
            .shift(UP * 0.2),
        )
        sig_group = VGroup(lock,
                           Text("Signed ✓", font_size=16, color=YELLOW_D, weight=BOLD))
        sig_group.arrange(RIGHT, buff=0.15)
        sig_group.next_to(tx.outer, DOWN, buff=0.5)

        self.play(GrowFromCenter(sig_group), run_time=0.5)
        self.play(
            Flash(sig_group, color=YELLOW, flash_radius=0.7,
                  line_length=0.15, num_lines=14, run_time=0.5),
        )
        self.wait(0.3)

        verify = Text("Anyone with Alice's public key can verify this signature",
                        font_size=17, color=GREEN_D)
        verify.next_to(sig_group, DOWN, buff=0.25)
        self.play(FadeIn(verify, shift=UP * 0.1), run_time=0.5)
        self.wait(0.6)

        scene_g = VGroup(tx, priv_key, sign_arrow, sign_label, sig_group, verify)
        self.play(FadeOut(scene_g, shift=LEFT * 0.3), FadeOut(cap), run_time=0.5)

    # ============================================ 4. broadcast
    def scene_broadcast(self):
        self._show_progress(4)
        cap = self._caption("Step 4 — Alice sends the transaction to the Bitcoin network")

        net_label = Text("Bitcoin P2P Network", font_size=18, color=GREY_B)
        net_label.move_to(RIGHT * 1.0 + UP * 2.2)
        network = P2PNetwork(scale_factor=0.7, node_radius=0.2)
        network.move_to(RIGHT * 1.0 + DOWN * 0.1)

        alice_node = VGroup(
            Circle(radius=0.3, color=BLUE_C, fill_opacity=0.6, stroke_width=2.5),
            Text("Alice", font_size=12, color=BLUE_C),
        )
        alice_node[1].move_to(alice_node[0])
        alice_node.move_to(LEFT * 4.8)
        conn = DashedLine(alice_node.get_right(), network.nodes[0].get_left(),
                           color=GREY_B, stroke_width=1.5, dash_length=0.1)

        self.play(
            FadeIn(alice_node, shift=RIGHT * 0.3),
            Create(network, run_time=1.0),
            FadeIn(net_label, shift=DOWN * 0.1),
        )
        self.play(Create(conn), run_time=0.4)
        self.wait(0.2)

        packet = TxPacket("tx", color=BLUE_D, radius=0.18)
        packet.move_to(alice_node.get_center())
        self.play(FadeIn(packet, scale=0.3), run_time=0.25)

        path_line = Line(alice_node.get_center(), network.nodes[0].get_center(),
                          color=BLUE_D, stroke_width=2)
        self.play(
            MoveAlongPath(packet, path_line),
            Create(path_line),
            run_time=0.6,
        )
        self.play(FadeOut(packet), FadeOut(path_line), run_time=0.15)
        self.play(
            network.nodes[0].animate.set_color(GREEN_D).set_fill(GREEN_D, 0.4),
            Flash(network.nodes[0], color=GREEN_D, flash_radius=0.35,
                  line_length=0.12, num_lines=8, run_time=0.3),
            run_time=0.3,
        )

        cap = self._update_caption(cap, "Each node validates and relays to its neighbours")

        waves = network.get_propagation_order(0)
        for wave in waves:
            anims = []
            for idx in wave:
                anims.append(
                    network.nodes[idx].animate.set_color(GREEN_D).set_fill(GREEN_D, 0.4))
                anims.append(
                    Flash(network.nodes[idx], color=GREEN_D, flash_radius=0.3,
                          line_length=0.1, num_lines=8, run_time=0.35))
            self.play(*anims, run_time=0.45)

        all_lit = Text("All nodes received the transaction", font_size=18,
                        color=GREEN_D, weight=BOLD)
        all_lit.next_to(network, DOWN, buff=0.4)
        self.play(FadeIn(all_lit, shift=UP * 0.1), run_time=0.4)
        self.wait(0.5)

        scene_g = VGroup(alice_node, network, conn, net_label, all_lit)
        self.play(FadeOut(scene_g, shift=RIGHT * 0.3), FadeOut(cap), run_time=0.5)

    # =========================================== 5. mempool & validation
    def scene_mempool_validation(self):
        self._show_progress(5)
        cap = self._caption("Step 5 — Each node validates the transaction")

        checks = [
            ("Is the digital signature valid?", GREEN_D),
            ("Do the input UTXOs exist and are unspent?", GREEN_D),
            ("Is there no double-spend attempt?", GREEN_D),
            ("Is the transaction format correct?", GREEN_D),
        ]
        checks_title = Text("Node Validation", font_size=30, color=BLUE_C, weight=BOLD)
        checks_title.move_to(UP * 2.3)
        self.play(FadeIn(checks_title, shift=DOWN * 0.2), run_time=0.4)

        check_group = VGroup()
        for txt, col in checks:
            line = VGroup(
                Text("✓", font_size=22, color=col, weight=BOLD),
                Text(txt, font_size=19, color=col),
            ).arrange(RIGHT, buff=0.15)
            check_group.add(line)
        check_group.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        check_group.move_to(UP * 0.4 + LEFT * 0.3)

        for line in check_group:
            line[0].set_opacity(0)
            self.play(FadeIn(line[1], shift=RIGHT * 0.2), run_time=0.3)
            self.play(line[0].animate.set_opacity(1), run_time=0.2)
            self.wait(0.08)

        passed = Text("All checks passed — transaction accepted!", font_size=20,
                       color=GREEN_D, weight=BOLD)
        passed.next_to(check_group, DOWN, buff=0.4)
        self.play(
            FadeIn(passed, scale=1.15),
            Flash(passed, color=GREEN, flash_radius=1.0, line_length=0.15,
                  num_lines=12, run_time=0.5),
            run_time=0.5,
        )
        self.wait(0.4)

        self.play(FadeOut(checks_title), FadeOut(check_group), FadeOut(passed), run_time=0.4)

        cap = self._update_caption(cap, "The transaction enters the mempool — a waiting room")

        mempool = MempoolPool(width=5.0, height=3.4)
        mempool.move_to(UP * 0.1)
        self.play(DrawBorderThenFill(mempool.container, run_time=0.6),
                  Write(mempool.title), FadeIn(mempool.subtitle), run_time=0.7)

        tx_data = [
            ("tx₁", "0.5 BTC → Bob", BLUE_D, True),
            ("tx₂", "0.3 BTC → Carol", TEAL_D, False),
            ("tx₃", "1.2 BTC → Dave", PURPLE_B, False),
            ("tx₄", "0.08 BTC → Eve", MAROON_D, False),
            ("tx₅", "2.0 BTC → Frank", ORANGE, False),
        ]
        tx_items = []
        for i, (txid, desc, color, is_ours) in enumerate(tx_data):
            tx_rect = RoundedRectangle(width=4.2, height=0.45, corner_radius=0.06,
                                        color=color, fill_opacity=0.12, stroke_width=2)
            bubble = Circle(radius=0.15, color=color, fill_opacity=0.8)
            tx_text = Text(txid, font_size=12, weight=BOLD)
            tx_text.move_to(bubble)
            desc_text = Text(desc, font_size=14, color=GREY_B)
            txid_group = VGroup(bubble, tx_text)
            txid_group.move_to(tx_rect.get_left() + RIGHT * 0.45)
            desc_text.next_to(txid_group, RIGHT, buff=0.2)
            item = VGroup(tx_rect, txid_group, desc_text)
            pos = mempool.get_slot_position(i)
            item.move_to(pos)
            tx_items.append((item, is_ours))

        for item, is_ours in tx_items:
            appear = mempool.container.get_right() + RIGHT * 1.5
            target = item.get_center().copy()
            item.move_to(appear)
            self.play(item.animate.move_to(target), run_time=0.35)

        our_item = tx_items[0][0]
        pointer = Arrow(our_item.get_left() + LEFT * 0.15,
                          our_item.get_left() + LEFT * 1.2,
                          buff=0, color=BLUE_C, stroke_width=2.5)
        pointer_lbl = Text("Alice's tx", font_size=15, color=BLUE_C, weight=BOLD)
        pointer_lbl.next_to(pointer, LEFT, buff=0.1)
        self.play(Create(pointer), FadeIn(pointer_lbl), run_time=0.4)
        self.play(Circumscribe(our_item, color=BLUE, buff=0.04), run_time=0.6)
        self.wait(0.6)

        all_items = VGroup(*[it for it, _ in tx_items])
        scene_g = VGroup(mempool, all_items, pointer, pointer_lbl)
        self.play(FadeOut(scene_g, shift=DOWN * 0.3), FadeOut(cap), run_time=0.5)

    # ============================================= 6. mining
    def scene_mining(self):
        self._show_progress(6)
        cap = self._caption("Step 6 — A miner picks transactions and builds a block")

        miner = create_person("Miner", color=YELLOW_D).scale(0.65)
        miner.move_to(LEFT * 5.2 + UP * 1.0)
        self.play(miner.shift(LEFT * 1).animate.shift(RIGHT * 1), run_time=0.5)

        mp = RoundedRectangle(width=2.2, height=2.0, corner_radius=0.12,
                               color=BLUE_C, fill_opacity=0.06, stroke_width=2)
        mp.move_to(LEFT * 1.8 + UP * 1.0)
        mp_lbl = Text("Mempool", font_size=16, color=BLUE_C)
        mp_lbl.next_to(mp, UP, buff=0.08)
        self.play(DrawBorderThenFill(mp), FadeIn(mp_lbl, shift=DOWN * 0.1), run_time=0.5)

        tx_circles = VGroup()
        tx_colors = [BLUE_D, TEAL_D, PURPLE_B, ORANGE]
        tx_names = ["tx₁", "tx₂", "tx₃", "tx₄"]
        for i, (col, nm) in enumerate(zip(tx_colors, tx_names)):
            c = Circle(radius=0.16, color=col, fill_opacity=0.75)
            t = Text(nm, font_size=11)
            t.move_to(c)
            tx_circles.add(VGroup(c, t))
        tx_circles.arrange_in_grid(2, 2, buff=0.15)
        tx_circles.move_to(mp.get_center())
        self.play(FadeIn(tx_circles, scale=0.7), run_time=0.4)
        self.wait(0.2)

        block_r = Rectangle(width=3.0, height=2.4, color=GREEN_D,
                              fill_opacity=0.1, stroke_width=2.5)
        block_r.move_to(RIGHT * 2.5 + UP * 1.0)
        block_hdr = Text("Block #7", font_size=20, weight=BOLD, color=GREEN_D)
        block_hdr.next_to(block_r, UP, buff=0.1)
        self.play(DrawBorderThenFill(block_r), Write(block_hdr), run_time=0.6)

        pick_arrow = Arrow(mp.get_right(), block_r.get_left(), buff=0.15,
                            color=YELLOW_D, stroke_width=2.5)
        pick_lbl = Text("Highest-fee txs", font_size=13, color=YELLOW_D)
        pick_lbl.next_to(pick_arrow, UP, buff=0.05)
        self.play(GrowArrow(pick_arrow), FadeIn(pick_lbl), run_time=0.5)

        tx_in_block = tx_circles.copy()
        tx_in_block.generate_target()
        tx_in_block.target.arrange_in_grid(2, 2, buff=0.12)
        tx_in_block.target.move_to(block_r.get_center())
        self.play(MoveToTarget(tx_in_block), run_time=0.6)
        self.wait(0.2)

        cap = self._update_caption(cap,
            "The miner tries trillions of nonces to find a valid hash (Proof of Work)")

        nonce_d = Text("Nonce: 0", font_size=18, color=ORANGE)
        nonce_d.next_to(block_r, DOWN, buff=0.2)
        hash_d = Text("Hash: ????????...????", font_size=14, color=GREY_B)
        hash_d.next_to(nonce_d, DOWN, buff=0.12)
        target_txt = Text("Target: hash must start with 000000...", font_size=13, color=GREY)
        target_txt.next_to(hash_d, DOWN, buff=0.12)
        self.play(FadeIn(nonce_d), FadeIn(hash_d), FadeIn(target_txt), run_time=0.4)

        nonce_vals = [
            ("14,203", "8f3a1b...91cb"),
            ("51,887", "d20ef4...f4a2"),
            ("107,442", "b791cc...55e3"),
            ("248,991", "4c0821...aa17"),
            ("301,556", "e2f1ab...3b09"),
            ("377,840", "1d9c07...c8e4"),
            ("389,012", "a33f19...ee71"),
        ]
        for nonce, hash_v in nonce_vals:
            nn = Text(f"Nonce: {nonce}", font_size=18, color=ORANGE).move_to(nonce_d)
            hh = Text(f"Hash: {hash_v}", font_size=14, color=RED_C).move_to(hash_d)
            self.play(Transform(nonce_d, nn), Transform(hash_d, hh), run_time=0.18)

        final_n = Text("Nonce: 392,117", font_size=18, color=GREEN_D, weight=BOLD)
        final_n.move_to(nonce_d)
        final_h = Text("Hash: 000000...7f2a ✓", font_size=14, color=GREEN_D, weight=BOLD)
        final_h.move_to(hash_d)
        self.play(Transform(nonce_d, final_n), Transform(hash_d, final_h), run_time=0.3)

        self.play(
            Flash(block_r.get_center(), color=GREEN, flash_radius=1.6,
                  line_length=0.25, num_lines=20, run_time=0.6),
            Circumscribe(VGroup(block_r, block_hdr), color=GREEN, buff=0.08),
            run_time=0.7,
        )

        mined_txt = Text("Block mined!", font_size=28, color=GREEN_D, weight=BOLD)
        mined_txt.move_to(DOWN * 2.6)
        self.play(FadeIn(mined_txt, scale=1.3), run_time=0.4)
        self.wait(0.5)

        scene_g = VGroup(miner, mp, mp_lbl, tx_circles, block_r, block_hdr,
                          pick_arrow, pick_lbl, tx_in_block,
                          nonce_d, hash_d, target_txt, mined_txt)
        self.play(FadeOut(scene_g, shift=UP * 0.3), FadeOut(cap), run_time=0.5)

    # ========================================= 7. confirmations
    def scene_confirmations(self):
        self._show_progress(7)
        cap = self._caption("Step 7 — The block is added to the blockchain")

        chain = SimpleChain(block_width=1.05, block_height=0.65, block_gap=0.12,
                            font_size=16, tx_font_size=10, tx_radius=0.10,
                            start_pos=LEFT * 5.8 + DOWN * 0.3)

        for i in range(5, 7):
            chain.add_block(self, str(i), color=BLUE_D)

        cap = self._update_caption(cap, "Block 7 contains Alice's transaction — that's 1 confirmation")

        b7 = chain.add_block(self, "7", txids=["tx"], color=GREEN_D)
        self.play(
            Circumscribe(b7, color=GREEN, buff=0.06),
            Flash(b7.get_center(), color=GREEN, flash_radius=0.6,
                  line_length=0.12, num_lines=10, run_time=0.5),
            run_time=0.7,
        )

        conf_lbl = Text("1 confirmation", font_size=20, color=GREEN_D)
        conf_arrow = Arrow(ORIGIN, ORIGIN, buff=0)
        conf_lbl.next_to(b7, UP, buff=0.4)
        conf_arrow = Arrow(conf_lbl.get_bottom(), b7.get_top(),
                            buff=0.05, color=GREEN_D, stroke_width=2,
                            max_tip_length_to_length_ratio=0.25)
        self.play(FadeIn(conf_lbl, shift=DOWN * 0.1), Create(conf_arrow), run_time=0.4)
        self.wait(0.3)

        cap = self._update_caption(cap, "Every new block on top adds another confirmation")

        for i, num in enumerate([8, 9, 10, 11, 12]):
            chain.add_block(self, str(num), color=BLUE_D)
            new_c = Text(f"{i + 2} confirmations", font_size=20, color=GREEN_D)
            new_c.move_to(conf_lbl)
            self.play(Transform(conf_lbl, new_c), run_time=0.22)

        self.play(FadeOut(conf_arrow), run_time=0.2)

        final_lbl = Text("6 confirmations — practically irreversible",
                          font_size=22, color=YELLOW_D, weight=BOLD)
        final_lbl.next_to(chain, UP, buff=0.55)
        self.play(
            ReplacementTransform(conf_lbl, final_lbl),
            run_time=0.5,
        )
        self.play(Circumscribe(final_lbl, color=YELLOW, buff=0.06), run_time=0.6)
        self.wait(0.5)

        safe = Text("Bob can now trust the payment is final", font_size=20,
                      color=GREEN_D)
        safe.next_to(final_lbl, DOWN, buff=0.15)
        self.play(FadeIn(safe, shift=UP * 0.1), run_time=0.4)
        self.wait(0.7)

        scene_g = VGroup(chain, final_lbl, safe)
        self.play(FadeOut(scene_g, shift=DOWN * 0.3), FadeOut(cap), run_time=0.5)

    # ============================================= outro
    def scene_outro(self):
        if hasattr(self, '_progress_bar'):
            self.play(FadeOut(self._progress_bar), run_time=0.3)
        self.play(FadeOut(self.top_title), FadeOut(self.bg_grid), run_time=0.4)

        recap = Text("The Transaction Lifecycle", font_size=36, weight=BOLD)
        recap.move_to(UP * 3.0)
        line = Line(LEFT * 3, RIGHT * 3, color=YELLOW_D, stroke_width=2.5)
        line.next_to(recap, DOWN, buff=0.12)
        self.play(FadeIn(recap, shift=DOWN * 0.2), Create(line), run_time=0.5)

        steps_data = [
            ("1", "Create wallet & keys", BLUE_C,  "🔑"),
            ("2", "Build the transaction", GOLD_D,  "📝"),
            ("3", "Sign with private key", YELLOW_D, "🔒"),
            ("4", "Broadcast to network", GREEN_D,  "📡"),
            ("5", "Validate & enter mempool", BLUE_D, "✓"),
            ("6", "Mine into a block", TEAL_D,      "⛏"),
            ("7", "Confirm on the blockchain", YELLOW_D, "⛓"),
        ]

        rows = VGroup()
        for num, desc, color, icon_str in steps_data:
            bullet = Circle(radius=0.14, color=color, fill_opacity=0.6, stroke_width=2)
            n_txt = Text(num, font_size=14, color=WHITE, weight=BOLD)
            n_txt.move_to(bullet)
            icon = Text(icon_str, font_size=18)
            desc_txt = Text(desc, font_size=20, color=GREY_B)
            row = VGroup(VGroup(bullet, n_txt), icon, desc_txt).arrange(RIGHT, buff=0.2)
            rows.add(row)
        rows.arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        rows.next_to(line, DOWN, buff=0.35)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.4), run_time=0.25)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
