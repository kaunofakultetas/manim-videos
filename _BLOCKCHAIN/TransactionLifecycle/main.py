from manim import *
import numpy as np

from components.wallet import create_person, WalletBox, KeyPair, AddressLabel
from components.transaction import UTXOBox, TransactionBox, TxPacket
from components.network import P2PNetwork, MempoolPool
from components.blockchain import SimpleChain, ChainBlock


class Main(Scene):
    def construct(self):
        self.camera.background_color = "#0e0e0e"

        self.scene_title()
        self.scene_wallet_and_keys()
        self._transition("2 / 7")
        self.scene_construct_transaction()
        self._transition("3 / 7")
        self.scene_digital_signing()
        self._transition("4 / 7")
        self.scene_broadcast()
        self._transition("5 / 7")
        self.scene_mempool_validation()
        self._transition("6 / 7")
        self.scene_mining()
        self._transition("7 / 7")
        self.scene_confirmations()
        self.scene_outro()

    # -------------------------------------------------------- transitions
    def _transition(self, step_label: str):
        dot = Circle(radius=0.04, color=GREY_B, fill_opacity=0.6)
        dot.move_to(ORIGIN)
        self.play(FadeIn(dot, scale=0.5), run_time=0.2)
        self.play(FadeOut(dot, scale=2.0), run_time=0.2)

    # ------------------------------------------------------------------ title
    def scene_title(self):
        title = Text("The Lifecycle of a\nBitcoin Transaction", font_size=54,
                      line_spacing=1.3)
        underline = Line(LEFT * 3.5, RIGHT * 3.5, color=YELLOW_D, stroke_width=2)
        underline.next_to(title, DOWN, buff=0.3)

        self.play(Write(title), run_time=1.5)
        self.play(Create(underline), run_time=0.5)
        self.wait(1.0)
        self.play(
            FadeOut(underline),
            title.animate.scale(0.42).to_edge(UP, buff=0.2),
            run_time=0.8,
        )
        self.top_title = title

    # ------------------------------------------------- 1. wallet & key pair
    def scene_wallet_and_keys(self):
        caption = self._caption("1.  Alice creates a wallet — a cryptographic key pair")

        alice = create_person("Alice", color=BLUE_C).scale(0.8)
        alice.move_to(LEFT * 4.5 + UP * 0.5)
        self.play(FadeIn(alice, shift=UP * 0.3))

        wallet = WalletBox("Alice", color=BLUE_C, width=3.2, height=1.8)
        wallet.move_to(RIGHT * 0.3 + UP * 0.6)
        self.play(Create(wallet.box), Write(wallet.label), run_time=0.8)

        keys = KeyPair()
        keys.move_to(wallet.box.get_center())
        self.play(FadeIn(keys.priv, shift=LEFT * 0.3), run_time=0.5)
        self.wait(0.15)
        self.play(FadeIn(keys.pub, shift=LEFT * 0.3), run_time=0.5)
        self.wait(0.4)

        priv_note = Text("Secret — never shared", font_size=16, color=RED_D)
        priv_note.next_to(keys.priv, RIGHT, buff=0.25)
        pub_note = Text("Shared freely", font_size=16, color=GREEN_D)
        pub_note.next_to(keys.pub, RIGHT, buff=0.25)
        self.play(FadeIn(priv_note), FadeIn(pub_note), run_time=0.5)
        self.play(Indicate(keys.priv, color=RED, scale_factor=1.05), run_time=0.5)
        self.wait(0.5)

        self.play(
            Transform(caption,
                      self._caption("The public key is hashed to produce a Bitcoin address")))
        self.wait(0.3)

        addr = AddressLabel("1A1zP1...QGefi2", color=TEAL_C)
        addr.move_to(DOWN * 1.2)
        arrow = Arrow(keys.pub.get_bottom(), addr.get_top(), buff=0.12,
                       color=TEAL_C, stroke_width=2.5, max_tip_length_to_length_ratio=0.12)
        hash_lbl = Text("Hash", font_size=16, color=TEAL_C).next_to(arrow, RIGHT, buff=0.12)
        self.play(Create(arrow), FadeIn(hash_lbl), run_time=0.5)
        self.play(GrowFromCenter(addr), run_time=0.5)
        self.play(Circumscribe(addr, color=TEAL_C), run_time=0.6)
        self.wait(0.7)

        self.wallet_scene = VGroup(alice, wallet, keys, priv_note, pub_note,
                                    addr, arrow, hash_lbl)
        self.play(FadeOut(self.wallet_scene), FadeOut(caption), run_time=0.6)

    # --------------------------------------- 2. construct the transaction
    def scene_construct_transaction(self):
        caption = self._caption("2.  Alice constructs a transaction to send Bitcoin to Bob")

        alice = create_person("Alice", color=BLUE_C).scale(0.7)
        alice.move_to(LEFT * 5.5 + UP * 1.5)
        bob = create_person("Bob", color=GREEN_C).scale(0.7)
        bob.move_to(RIGHT * 5.5 + UP * 1.5)
        self.play(FadeIn(alice, shift=DOWN * 0.2), FadeIn(bob, shift=DOWN * 0.2))

        want_text = Text("Alice wants to send 0.5 BTC to Bob", font_size=22, color=GREY_B)
        want_text.move_to(UP * 0.0)
        send_arrow = Arrow(alice.get_right() + DOWN * 0.3, bob.get_left() + DOWN * 0.3,
                            buff=0.3, color=GOLD_D, stroke_width=2)
        btc_label = Text("0.5 BTC", font_size=20, color=GOLD_D, weight=BOLD)
        btc_label.next_to(send_arrow, UP, buff=0.1)
        self.play(FadeIn(want_text, shift=UP * 0.15), run_time=0.5)
        self.play(Create(send_arrow), FadeIn(btc_label), run_time=0.6)
        self.wait(0.5)

        self.play(FadeOut(want_text), FadeOut(send_arrow), FadeOut(btc_label), run_time=0.4)

        self.play(
            Transform(caption,
                      self._caption("She spends a UTXO (unspent coin) and creates new outputs")))

        utxo = UTXOBox("1.0 BTC", label="from prev. tx", color=GOLD_D, width=2.2)
        utxo.move_to(LEFT * 3.5 + DOWN * 0.6)
        utxo_title = Text("Alice's UTXO", font_size=18, color=GOLD_D)
        utxo_title.next_to(utxo, UP, buff=0.15)
        self.play(GrowFromCenter(utxo), FadeIn(utxo_title), run_time=0.6)
        self.wait(0.4)

        tx = TransactionBox(
            txid="a4f2...c7e1",
            inputs=[{"amount": "1.0 BTC", "label": "Alice's UTXO"}],
            outputs=[
                {"amount": "0.5 BTC", "label": "→ Bob"},
                {"amount": "0.4999 BTC", "label": "→ Alice (change)"},
            ],
            fee="0.0001 BTC",
            width=5.4,
        )
        tx.move_to(DOWN * 0.4)

        self.play(
            ReplacementTransform(utxo, tx.inputs_group),
            FadeOut(utxo_title),
            FadeIn(tx.outer), FadeIn(tx.txid_label),
            FadeIn(tx.outputs_group), FadeIn(tx.arrow_mob),
            FadeIn(tx.fee_label),
            run_time=0.9,
        )
        self.wait(0.4)

        self.play(Circumscribe(tx.inputs_group, color=GOLD_D), run_time=0.6)
        in_note = Text("Input consumed", font_size=15, color=GOLD_D)
        in_note.next_to(tx.inputs_group, DOWN, buff=0.15)
        self.play(FadeIn(in_note, shift=UP * 0.1), run_time=0.3)

        self.play(Circumscribe(tx.outputs_group, color=GREEN_D), run_time=0.6)
        out_note = Text("New UTXOs created", font_size=15, color=GREEN_D)
        out_note.next_to(tx.outputs_group, DOWN, buff=0.15)
        self.play(FadeIn(out_note, shift=UP * 0.1), run_time=0.3)

        self.play(Indicate(tx.fee_label, color=ORANGE), run_time=0.5)
        self.wait(0.8)

        self.play(FadeOut(in_note), FadeOut(out_note), run_time=0.3)

        self.tx_box = tx
        self.play(FadeOut(alice), FadeOut(bob), FadeOut(caption), run_time=0.5)

    # ------------------------------------------------ 3. digital signing
    def scene_digital_signing(self):
        caption = self._caption("3.  Alice signs the transaction with her private key")

        tx = self.tx_box
        self.play(tx.animate.move_to(RIGHT * 1.2 + DOWN * 0.2), run_time=0.5)

        priv_key = VGroup(
            RoundedRectangle(width=2.2, height=0.6, corner_radius=0.06,
                             color=RED_D, fill_opacity=0.2, stroke_width=2),
            Text("Private Key  🔑", font_size=16, color=RED_D),
        )
        priv_key[1].move_to(priv_key[0])
        priv_key.move_to(LEFT * 4.5 + UP * 0.8)
        self.play(FadeIn(priv_key, shift=RIGHT * 0.3), run_time=0.5)
        self.play(Indicate(priv_key, color=RED_D, scale_factor=1.08), run_time=0.4)

        sign_arrow = Arrow(priv_key.get_right(), tx.get_left() + UP * 0.3,
                            buff=0.2, color=YELLOW_D, stroke_width=2.5)
        sign_text = Text("Signs", font_size=18, color=YELLOW_D)
        sign_text.next_to(sign_arrow, UP, buff=0.08)
        self.play(Create(sign_arrow), FadeIn(sign_text), run_time=0.6)
        self.wait(0.3)

        sig_badge = VGroup(
            RoundedRectangle(width=2.6, height=0.55, corner_radius=0.06,
                             color=YELLOW_D, fill_opacity=0.25, stroke_width=2),
            Text("Digital Signature  ✓", font_size=16, color=YELLOW_D, weight=BOLD),
        )
        sig_badge[1].move_to(sig_badge[0])
        sig_badge.next_to(tx.outer, DOWN, buff=0.5)
        self.play(GrowFromCenter(sig_badge), run_time=0.5)
        self.play(
            Flash(sig_badge, color=YELLOW, flash_radius=0.6,
                  line_length=0.15, num_lines=12, run_time=0.5),
        )
        self.wait(0.4)

        verify_note = Text("Anyone can verify with Alice's public key",
                            font_size=18, color=GREEN_D)
        verify_note.next_to(sig_badge, DOWN, buff=0.25)
        self.play(FadeIn(verify_note, shift=UP * 0.15), run_time=0.5)
        self.wait(0.7)

        self.signing_scene = VGroup(tx, priv_key, sign_arrow, sign_text,
                                     sig_badge, verify_note)
        self.play(FadeOut(self.signing_scene), FadeOut(caption), run_time=0.6)

    # -------------------------------------------- 4. broadcast to network
    def scene_broadcast(self):
        caption = self._caption("4.  Alice broadcasts the signed transaction to the network")

        net_label = Text("Bitcoin P2P Network", font_size=20, color=GREY_B)
        net_label.move_to(RIGHT * 1.0 + UP * 2.2)

        network = P2PNetwork(scale_factor=0.7)
        network.move_to(RIGHT * 1.0 + DOWN * 0.1)

        alice_node = Circle(radius=0.28, color=BLUE_C, fill_opacity=0.7)
        alice_label = Text("Alice", font_size=18, color=BLUE_C)
        alice_label.next_to(alice_node, DOWN, buff=0.12)
        alice_group = VGroup(alice_node, alice_label)
        alice_group.move_to(LEFT * 4.8)

        conn_line = Line(alice_node.get_right(), network.nodes[0].get_left(),
                          color=GREY_B, stroke_width=1.5)

        self.play(FadeIn(alice_group), Create(network),
                  Create(conn_line), FadeIn(net_label), run_time=0.8)
        self.wait(0.3)

        packet = TxPacket("tx", color=BLUE_D)
        packet.move_to(alice_node.get_center())
        self.play(FadeIn(packet, scale=0.5), run_time=0.3)

        first_node_idx = 0
        target = network.nodes[first_node_idx].get_center()
        self.play(packet.animate.move_to(target), run_time=0.6)
        self.play(FadeOut(packet), run_time=0.15)
        self.play(
            network.nodes[first_node_idx].animate.set_color(GREEN_D),
            Flash(network.nodes[first_node_idx], color=GREEN_D,
                  flash_radius=0.3, line_length=0.1, num_lines=8, run_time=0.3),
            run_time=0.3,
        )

        self.play(
            Transform(caption,
                      self._caption("Nodes relay the transaction across the peer-to-peer network")))

        waves = network.get_propagation_order(first_node_idx)
        for wave in waves:
            anims = []
            for idx in wave:
                anims.append(network.nodes[idx].animate.set_color(GREEN_D))
            flash_anims = []
            for idx in wave:
                flash_anims.append(Flash(network.nodes[idx], color=GREEN_D,
                                         flash_radius=0.35, line_length=0.12,
                                         num_lines=8, run_time=0.4))
            self.play(*anims, *flash_anims, run_time=0.45)
        self.wait(0.6)

        self.broadcast_scene = VGroup(alice_group, network, conn_line, net_label)
        self.play(FadeOut(self.broadcast_scene), FadeOut(caption), run_time=0.6)

    # ----------------------------------------- 5. mempool & validation
    def scene_mempool_validation(self):
        caption = self._caption("5.  Nodes validate the transaction before accepting it")

        val_title = Text("Validation Checks", font_size=28, color=BLUE_C, weight=BOLD)
        val_title.move_to(UP * 2.0)
        self.play(FadeIn(val_title, shift=DOWN * 0.15), run_time=0.5)

        checks = [
            ("Valid signature?", GREEN_D),
            ("Sufficient funds (UTXOs exist)?", GREEN_D),
            ("No double-spend?", GREEN_D),
            ("Proper format & size?", GREEN_D),
        ]
        check_group = VGroup()
        for text, color in checks:
            mark = Text("✓  " + text, font_size=22, color=color)
            check_group.add(mark)
        check_group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        check_group.move_to(LEFT * 0.5 + UP * 0.3)

        for mark in check_group:
            self.play(FadeIn(mark, shift=RIGHT * 0.2), run_time=0.35)
            self.wait(0.1)

        pass_text = Text("All checks passed!", font_size=24, color=GREEN_D, weight=BOLD)
        pass_text.next_to(check_group, DOWN, buff=0.4)
        self.play(FadeIn(pass_text, scale=1.2), run_time=0.5)
        self.wait(0.5)

        self.play(FadeOut(val_title), FadeOut(check_group), FadeOut(pass_text), run_time=0.4)

        self.play(
            Transform(caption,
                      self._caption("The transaction enters the mempool and waits for a miner")))

        mempool = MempoolPool(width=4.5, height=3.2)
        mempool.move_to(UP * 0.1)
        self.play(Create(mempool.container), Write(mempool.title), run_time=0.6)

        tx_data = [
            ("tx₁", "0.5 BTC → Bob", BLUE_D),
            ("tx₂", "0.3 BTC → Carol", TEAL_D),
            ("tx₃", "1.2 BTC → Dave", PURPLE_B),
            ("tx₄", "0.05 BTC → Eve", MAROON_D),
        ]
        tx_items = []
        for i, (txid, desc, color) in enumerate(tx_data):
            tx_rect = RoundedRectangle(width=3.8, height=0.5, corner_radius=0.06,
                                        color=color, fill_opacity=0.15, stroke_width=2)
            bubble = Circle(radius=0.17, color=color, fill_opacity=0.85)
            tx_text = Text(txid, font_size=14, weight=BOLD)
            tx_text.move_to(bubble)
            desc_text = Text(desc, font_size=15, color=GREY_B)

            txid_group = VGroup(bubble, tx_text)
            txid_group.move_to(tx_rect.get_left() + RIGHT * 0.5)
            desc_text.next_to(txid_group, RIGHT, buff=0.2)

            item = VGroup(tx_rect, txid_group, desc_text)
            pos = mempool.get_slot_position(i)
            item.move_to(pos)
            tx_items.append(item)

        for i, item in enumerate(tx_items):
            appear_from = mempool.container.get_right() + RIGHT * 1.0
            item_target = item.get_center().copy()
            item.move_to(appear_from)
            self.play(item.animate.move_to(item_target), run_time=0.4)

        alice_arrow = Arrow(ORIGIN, ORIGIN, buff=0)
        alice_arrow = Arrow(
            tx_items[0].get_left() + LEFT * 0.1,
            tx_items[0].get_left() + LEFT * 0.8,
            buff=0, color=BLUE_C, stroke_width=2.5,
        )
        alice_note = Text("Alice's tx", font_size=16, color=BLUE_C)
        alice_note.next_to(alice_arrow, LEFT, buff=0.1)
        self.play(Create(alice_arrow), FadeIn(alice_note), run_time=0.4)
        self.play(Circumscribe(tx_items[0], color=BLUE), run_time=0.7)
        self.wait(0.7)

        self.mempool_group = VGroup(mempool, *tx_items, alice_arrow, alice_note)
        self.play(FadeOut(self.mempool_group), FadeOut(caption), run_time=0.6)

    # ------------------------------------------------ 6. mining & block
    def scene_mining(self):
        caption = self._caption("6.  A miner selects transactions and mines a new block")

        miner = create_person("Miner", color=YELLOW_D).scale(0.7)
        miner.move_to(LEFT * 5.0 + UP * 1.0)
        self.play(FadeIn(miner, shift=RIGHT * 0.2), run_time=0.5)

        mini_mempool = RoundedRectangle(width=2.5, height=1.8, corner_radius=0.1,
                                         color=BLUE_C, fill_opacity=0.08, stroke_width=2)
        mini_mempool.move_to(LEFT * 1.5 + UP * 1.0)
        mp_title = Text("Mempool", font_size=18, color=BLUE_C)
        mp_title.next_to(mini_mempool, UP, buff=0.08)
        self.play(Create(mini_mempool), Write(mp_title), run_time=0.5)

        txs = []
        tx_labels = [("tx₁", BLUE_D), ("tx₂", TEAL_D), ("tx₃", PURPLE_B)]
        for tid, col in tx_labels:
            c = Circle(radius=0.18, color=col, fill_opacity=0.8)
            t = Text(tid, font_size=13)
            t.move_to(c)
            txs.append(VGroup(c, t))
        tx_group_mp = VGroup(*txs).arrange(DOWN, buff=0.15)
        tx_group_mp.move_to(mini_mempool.get_center())
        self.play(FadeIn(tx_group_mp), run_time=0.4)
        self.wait(0.3)

        block_rect = Rectangle(width=2.8, height=2.2, color=GREEN_D,
                                fill_opacity=0.12, stroke_width=2.5)
        block_header = Text("Block #7", font_size=20, weight=BOLD, color=GREEN_D)
        block_rect.move_to(RIGHT * 2.5 + UP * 1.0)
        block_header.next_to(block_rect, UP, buff=0.1)
        self.play(Create(block_rect), Write(block_header), run_time=0.6)

        pick_arrow = Arrow(mini_mempool.get_right(), block_rect.get_left(),
                            buff=0.15, color=YELLOW_D, stroke_width=2.5)
        pick_lbl = Text("Selects highest-fee txs", font_size=14, color=YELLOW_D)
        pick_lbl.next_to(pick_arrow, UP, buff=0.06)
        self.play(Create(pick_arrow), FadeIn(pick_lbl), run_time=0.5)

        tx_copies = tx_group_mp.copy()
        tx_copies.generate_target()
        tx_copies.target.arrange(DOWN, buff=0.12).move_to(block_rect.get_center() + DOWN * 0.1)
        self.play(MoveToTarget(tx_copies), run_time=0.6)
        self.wait(0.3)

        self.play(
            Transform(caption,
                      self._caption("The miner searches for a valid hash (Proof of Work)")))

        nonce_display = Text("Nonce: 0", font_size=20, color=ORANGE)
        nonce_display.next_to(block_rect, DOWN, buff=0.25)
        hash_display = Text("Hash: 0000...????", font_size=16, color=GREY_B)
        hash_display.next_to(nonce_display, DOWN, buff=0.15)
        self.play(FadeIn(nonce_display), FadeIn(hash_display), run_time=0.4)

        nonce_vals = [
            ("14,203", "8f3a...91cb"),
            ("51,887", "d20e...f4a2"),
            ("107,442", "b791...55e3"),
            ("248,991", "4c08...aa17"),
            ("301,556", "e2f1...3b09"),
            ("377,840", "1d9c...c8e4"),
        ]
        for nonce, hash_v in nonce_vals:
            new_nonce = Text(f"Nonce: {nonce}", font_size=20, color=ORANGE)
            new_nonce.move_to(nonce_display)
            new_hash = Text(f"Hash: {hash_v}", font_size=16, color=GREY_B)
            new_hash.move_to(hash_display)
            self.play(
                Transform(nonce_display, new_nonce),
                Transform(hash_display, new_hash),
                run_time=0.2,
            )

        final_nonce = Text("Nonce: 392,117", font_size=20, color=GREEN_D, weight=BOLD)
        final_nonce.move_to(nonce_display)
        final_hash = Text("Hash: 000000...7f2a", font_size=16, color=GREEN_D, weight=BOLD)
        final_hash.move_to(hash_display)
        self.play(
            Transform(nonce_display, final_nonce),
            Transform(hash_display, final_hash),
            run_time=0.3,
        )
        self.play(
            Flash(block_rect, color=GREEN, flash_radius=1.5,
                  line_length=0.25, num_lines=16, run_time=0.6),
            Circumscribe(VGroup(block_rect, block_header), color=GREEN, buff=0.1),
            run_time=0.8,
        )
        self.wait(0.3)

        found_text = Text("Block mined!", font_size=30, color=GREEN_D, weight=BOLD)
        found_text.next_to(hash_display, DOWN, buff=0.35)
        self.play(FadeIn(found_text, scale=1.3), run_time=0.5)
        self.wait(0.6)

        self.mining_scene = VGroup(
            miner, mini_mempool, mp_title, tx_group_mp,
            block_rect, block_header, pick_arrow, pick_lbl,
            tx_copies, nonce_display, hash_display, found_text,
        )
        self.play(FadeOut(self.mining_scene), FadeOut(caption), run_time=0.6)

    # ---------------------------------------- 7. confirmations & finality
    def scene_confirmations(self):
        caption = self._caption("7.  The block is added to the chain — confirmations begin")

        chain = SimpleChain(block_width=1.05, block_height=0.65, block_gap=0.12,
                            font_size=16, tx_font_size=10, tx_radius=0.10,
                            start_pos=LEFT * 5.8 + DOWN * 0.5)

        for i in range(5, 7):
            chain.add_block(self, str(i), color=BLUE_D)

        self.play(
            Transform(caption,
                      self._caption("Block 7 contains Alice's transaction")))

        b7 = chain.add_block(self, "7", txids=["tx"], color=GREEN_D)
        self.play(Circumscribe(b7, color=GREEN, buff=0.05), run_time=0.7)
        self.wait(0.3)

        conf_label = Text("1 confirmation", font_size=22, color=GREEN_D)
        conf_label.next_to(b7, UP, buff=0.35)
        conf_arrow = Arrow(conf_label.get_bottom(), b7.get_top(), buff=0.05,
                            color=GREEN_D, stroke_width=2, max_tip_length_to_length_ratio=0.2)
        self.play(FadeIn(conf_label, shift=DOWN * 0.15), Create(conf_arrow), run_time=0.4)
        self.wait(0.4)

        self.play(
            Transform(caption,
                      self._caption("Each new block on top adds another confirmation")))

        for i, num in enumerate([8, 9, 10, 11, 12]):
            chain.add_block(self, str(num), color=BLUE_D)
            new_conf = Text(f"{i + 2} confirmations", font_size=22, color=GREEN_D)
            new_conf.move_to(conf_label)
            self.play(Transform(conf_label, new_conf), run_time=0.25)

        self.wait(0.3)

        self.play(FadeOut(conf_arrow), run_time=0.2)
        final_conf = Text("6 confirmations — practically irreversible",
                           font_size=24, color=YELLOW_D, weight=BOLD)
        final_conf.next_to(chain, UP, buff=0.5)
        self.play(Transform(conf_label, final_conf), run_time=0.5)
        self.play(Circumscribe(conf_label, color=YELLOW), run_time=0.7)
        self.wait(0.8)

        self.chain_scene = VGroup(chain, conf_label)
        self.play(FadeOut(self.chain_scene), FadeOut(caption), run_time=0.6)

    # ------------------------------------------------------------ outro
    def scene_outro(self):
        self.play(FadeOut(self.top_title), run_time=0.4)

        recap_title = Text("Transaction Lifecycle — Recap", font_size=36,
                            color=WHITE, weight=BOLD)
        recap_title.move_to(UP * 3.0)
        recap_line = Line(LEFT * 3.2, RIGHT * 3.2, color=YELLOW_D, stroke_width=2)
        recap_line.next_to(recap_title, DOWN, buff=0.15)
        self.play(FadeIn(recap_title, shift=DOWN * 0.2), Create(recap_line), run_time=0.6)

        steps = [
            ("1", "Wallet & keys created", BLUE_C),
            ("2", "Transaction constructed", GOLD_D),
            ("3", "Digitally signed", YELLOW_D),
            ("4", "Broadcast to P2P network", GREEN_D),
            ("5", "Validated & enters mempool", BLUE_D),
            ("6", "Mined into a block", TEAL_D),
            ("7", "Confirmed on the blockchain", YELLOW_D),
        ]

        step_mobs = VGroup()
        for num, desc, color in steps:
            bullet = Circle(radius=0.12, color=color, fill_opacity=0.7)
            n = Text(num, font_size=14, weight=BOLD)
            n.move_to(bullet)
            d = Text(desc, font_size=22, color=GREY_B)
            row = VGroup(VGroup(bullet, n), d).arrange(RIGHT, buff=0.25)
            step_mobs.add(row)
        step_mobs.arrange(DOWN, buff=0.26, aligned_edge=LEFT)
        step_mobs.next_to(recap_line, DOWN, buff=0.4)

        for mob in step_mobs:
            self.play(FadeIn(mob, shift=RIGHT * 0.3), run_time=0.28)
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)

    # ---------------------------------------------------------- helpers
    def _caption(self, text: str):
        return Text(text, font_size=26).to_edge(DOWN, buff=0.4)
