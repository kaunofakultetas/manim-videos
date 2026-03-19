from manim import *
import numpy as np

from components.wallet import create_avatar, KeyIcon, CoinIcon, WalletCard, AddressLabel
from components.transaction import TransactionCard, TxPacket
from components.network import NetworkGraph, MempoolContainer
from components.blockchain import BlockChain

BG = "#080c14"
GOLD = "#f7b731"
CYAN = "#45aaf2"
ROYAL = "#4a6cf7"
NEON_GRN = "#26de81"
NEON_RED = "#fc5c65"
PURPLE_A = "#a55eea"
TXT_DIM = "#5a6c8a"


class Main(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG
        self.camera.frame.set(width=14.2)

        self._build_atmosphere()
        self.scene_title()
        self.scene_wallet_and_keys()
        self.scene_construct_tx()
        self.scene_signing()
        self.scene_broadcast()
        self.scene_mempool()
        self.scene_mining()
        self.scene_confirmations()
        self.scene_outro()

    # ── atmospheric background ─────────────────────────────────
    def _build_atmosphere(self):
        rng = np.random.default_rng(42)
        dots = VGroup()
        for x in np.arange(-7.5, 8.0, 0.9):
            for y in np.arange(-4.5, 5.0, 0.9):
                r = rng.uniform(0.008, 0.022)
                op = rng.uniform(0.06, 0.18)
                d = Dot(
                    [x + rng.uniform(-0.15, 0.15),
                     y + rng.uniform(-0.15, 0.15), 0],
                    radius=r, color=ROYAL,
                )
                d.set_opacity(op)
                dots.add(d)
        for _ in range(18):
            d = Dot(
                [rng.uniform(-7, 7), rng.uniform(-4, 4), 0],
                radius=0.018, color=CYAN,
            )
            d.set_opacity(rng.uniform(0.12, 0.30))
            dots.add(d)
        self.bg_dots = dots
        self.add(dots)

    # ── progress bar ───────────────────────────────────────────
    def _show_progress(self, step, total=7):
        bar_w, bar_h = 4.0, 0.06
        bg_bar = RoundedRectangle(
            width=bar_w, height=bar_h, corner_radius=0.03,
            color=GREY_E, fill_opacity=0.25, stroke_width=0,
        )
        fill_w = max(0.08, bar_w * step / total)
        fill_bar = RoundedRectangle(
            width=fill_w, height=bar_h, corner_radius=0.03,
            color=GOLD, fill_opacity=0.7, stroke_width=0,
        )
        fill_bar.align_to(bg_bar, LEFT)
        lbl = Text(f"{step}/{total}", font_size=11, color=GREY_B)
        lbl.next_to(bg_bar, RIGHT, buff=0.12)
        prog = VGroup(bg_bar, fill_bar, lbl).to_corner(DR, buff=0.3)
        if hasattr(self, "_progress"):
            self.play(ReplacementTransform(self._progress, prog), run_time=0.3)
        else:
            self.play(FadeIn(prog, shift=UP * 0.08), run_time=0.3)
        self._progress = prog

    # ── caption helpers ────────────────────────────────────────
    def _cap(self, text, color=WHITE):
        c = Text(text, font_size=24, color=color)
        c.to_edge(DOWN, buff=0.4)
        return c

    def _show_cap(self, text, color=WHITE):
        c = self._cap(text, color)
        self.play(FadeIn(c, shift=UP * 0.15), run_time=0.4)
        return c

    def _update_cap(self, old, text, color=WHITE):
        new = self._cap(text, color)
        self.play(
            FadeOut(old, shift=DOWN * 0.12),
            FadeIn(new, shift=UP * 0.12),
            run_time=0.45,
        )
        return new

    # ── section card ───────────────────────────────────────────
    def _section_card(self, step_num, title, color):
        num_bg = Circle(
            radius=0.28, color=color,
            fill_opacity=0.2, stroke_width=2,
        )
        num_txt = Text(str(step_num), font_size=24, color=color, weight=BOLD)
        num_txt.move_to(num_bg)
        title_txt = Text(title, font_size=28, color=color, weight=BOLD)
        card = VGroup(VGroup(num_bg, num_txt), title_txt)
        card.arrange(RIGHT, buff=0.3)
        self.play(FadeIn(card, scale=0.9), run_time=0.35)
        self.wait(0.5)
        self.play(FadeOut(card, shift=UP * 0.3, scale=1.05), run_time=0.3)

    # ── camera ─────────────────────────────────────────────────
    def _zoom(self, center, scale=1.0, rt=0.7):
        self.play(
            self.camera.frame.animate.set(width=14.2 / scale).move_to(center),
            run_time=rt, rate_func=smooth,
        )

    def _zoom_reset(self, rt=0.5):
        self.play(
            self.camera.frame.animate.set(width=14.2).move_to(ORIGIN),
            run_time=rt, rate_func=smooth,
        )

    # ═══════════════════════════════════════════════ TITLE
    def scene_title(self):
        top = Text("The Lifecycle of a", font_size=36, color=GREY_B)
        bot = Text("Bitcoin Transaction", font_size=54, weight=BOLD)
        title = VGroup(top, bot).arrange(DOWN, buff=0.2)

        self.play(FadeIn(top, shift=DOWN * 0.4), run_time=0.7)
        self.play(Write(bot), run_time=1.2)

        line = Line(ORIGIN, ORIGIN, color=GOLD, stroke_width=2.5)
        line.next_to(title, DOWN, buff=0.2)
        self.play(line.animate.set(width=7.6), run_time=0.5, rate_func=rush_from)

        glow_line = line.copy().set_stroke(opacity=0.15, width=8)
        self.add(glow_line)
        self.wait(1.0)

        target = bot.copy().scale(0.32)
        target.to_edge(UP, buff=0.18)
        self.play(
            FadeOut(top, shift=UP * 0.3),
            FadeOut(line), FadeOut(glow_line),
            ReplacementTransform(bot, target),
            run_time=0.8, rate_func=smooth,
        )
        self.top_title = target

    # ═══════════════════════════════════════════════ 1. WALLET & KEYS
    def scene_wallet_and_keys(self):
        self._show_progress(1)
        self._section_card(1, "Create Wallet & Keys", BLUE_C)
        cap = self._show_cap("Step 1 — Alice creates a wallet")

        alice = create_avatar("Alice", color=BLUE_C, radius=0.45)
        alice.move_to(LEFT * 5.5 + UP * 0.3)
        self.play(
            FadeIn(alice, shift=RIGHT * 0.8, scale=0.8),
            run_time=0.7, rate_func=smooth,
        )

        wallet = WalletCard("Alice", color=BLUE_C, width=3.4, height=2.2)
        wallet.move_to(RIGHT * 0.5 + UP * 0.4)
        self.play(
            DrawBorderThenFill(wallet.body, run_time=0.8),
            FadeIn(wallet.shadow, run_time=0.5),
            FadeIn(wallet.header, shift=DOWN * 0.1, run_time=0.5),
            Write(wallet.label, run_time=0.6),
        )
        self.wait(0.3)

        cap = self._update_cap(cap, "A wallet is really just a pair of cryptographic keys")

        priv = KeyIcon(color=NEON_RED, label="Private Key", scale_f=1.2)
        priv.move_to(wallet.body.get_center() + UP * 0.3)
        self.play(FadeIn(priv, shift=RIGHT * 0.5, scale=0.7), run_time=0.6)
        priv_note = Text("Keep secret!", font_size=14, color=NEON_RED, weight=BOLD)
        priv_note.next_to(priv, RIGHT, buff=0.25)
        self.play(FadeIn(priv_note, shift=LEFT * 0.12), run_time=0.3)

        pub = KeyIcon(color=NEON_GRN, label="Public Key", scale_f=1.2)
        pub.move_to(wallet.body.get_center() + DOWN * 0.45)
        self.play(FadeIn(pub, shift=RIGHT * 0.5, scale=0.7), run_time=0.6)
        pub_note = Text("Share freely", font_size=14, color=NEON_GRN)
        pub_note.next_to(pub, RIGHT, buff=0.25)
        self.play(FadeIn(pub_note, shift=LEFT * 0.12), run_time=0.3)
        self.wait(0.4)

        cap = self._update_cap(cap, "The public key is hashed to create a Bitcoin address")
        self._zoom(wallet.body.get_center() + DOWN * 0.5, scale=1.3, rt=0.6)

        addr = AddressLabel("1A1zP1...QGefi2", color=CYAN)
        addr.move_to(DOWN * 1.8 + RIGHT * 0.5)
        arrow = CurvedArrow(
            pub.get_bottom() + DOWN * 0.05,
            addr.get_top() + UP * 0.05,
            color=CYAN, stroke_width=2.5, angle=-0.35,
        )
        hash_lbl = Text("SHA-256 + RIPEMD-160", font_size=11, color=CYAN)
        hash_lbl.next_to(arrow, RIGHT, buff=0.08)
        self.play(Create(arrow, run_time=0.5), FadeIn(hash_lbl, run_time=0.4))
        self.play(GrowFromCenter(addr, run_time=0.5))
        self.play(Circumscribe(addr, color=CYAN, buff=0.05, run_time=0.5))
        self.wait(0.5)

        self._zoom_reset()
        scene = VGroup(alice, wallet, priv, pub, priv_note, pub_note, addr, arrow, hash_lbl)
        self.play(FadeOut(scene, shift=LEFT * 0.6), FadeOut(cap), run_time=0.6)

    # ═══════════════════════════════════════════════ 2. BUILD TX
    def scene_construct_tx(self):
        self._show_progress(2)
        self._section_card(2, "Build the Transaction", GOLD)
        cap = self._show_cap("Step 2 — Alice builds a transaction to pay Bob")

        alice = create_avatar("Alice", color=BLUE_C, radius=0.4)
        alice.move_to(LEFT * 5.5 + UP * 1.5)
        bob = create_avatar("Bob", color=NEON_GRN, radius=0.4)
        bob.move_to(RIGHT * 5.5 + UP * 1.5)
        self.play(
            FadeIn(alice, shift=RIGHT * 0.6, scale=0.8),
            FadeIn(bob, shift=LEFT * 0.6, scale=0.8),
            run_time=0.6,
        )

        thought = Text(
            '"I want to send Bob 0.5 BTC"', font_size=18,
            color=GREY_B, slant=ITALIC,
        )
        thought.next_to(alice, RIGHT, buff=0.3).shift(UP * 0.25)
        self.play(FadeIn(thought, shift=UP * 0.12), run_time=0.4)
        self.wait(0.5)
        self.play(FadeOut(thought, shift=UP * 0.1), run_time=0.3)

        cap = self._update_cap(cap, "She has an unspent coin (UTXO) worth 1.0 BTC")

        coin = CoinIcon("1.0 BTC", color=GOLD, radius=0.42)
        coin.move_to(LEFT * 3.5 + DOWN * 0.2)
        self.play(
            GrowFromCenter(coin, run_time=0.6),
            Flash(
                coin.get_center(), color=GOLD, flash_radius=0.8,
                line_length=0.12, num_lines=12, run_time=0.5,
            ),
        )
        coin_lbl = Text("Alice's unspent coin", font_size=15, color=GOLD)
        coin_lbl.next_to(coin, DOWN, buff=0.25)
        self.play(FadeIn(coin_lbl, shift=UP * 0.1), run_time=0.35)
        self.wait(0.4)

        cap = self._update_cap(
            cap, "She creates outputs for Bob and change back to herself",
        )

        tx = TransactionCard(
            txid="a4f2...c7e1",
            inputs=[{"amount": "1.0 BTC", "label": "Alice's coin"}],
            outputs=[
                {"amount": "0.5 BTC", "label": "→ Bob"},
                {"amount": "0.4999 BTC", "label": "→ Alice (change)"},
            ],
            fee="0.0001 BTC", width=5.4,
        )
        tx.move_to(DOWN * 0.2)

        self.play(
            coin.animate.move_to(tx.inputs_group.get_center()).scale(0.01).set_opacity(0),
            FadeOut(coin_lbl),
            run_time=0.6, rate_func=rush_into,
        )
        self.remove(coin)
        self.play(FadeIn(tx, shift=UP * 0.3, scale=0.92), run_time=0.7)
        self.wait(0.2)

        self.play(
            Indicate(tx.inputs_group, color=GOLD, scale_factor=1.04),
            run_time=0.5,
        )
        self.play(
            Indicate(tx.outputs_group, color=NEON_GRN, scale_factor=1.04),
            run_time=0.5,
        )
        self.play(
            Indicate(tx.fee_label, color=ORANGE, scale_factor=1.08),
            run_time=0.4,
        )
        self.wait(0.5)

        self.tx_card = tx
        self.play(
            FadeOut(alice, shift=LEFT * 0.5),
            FadeOut(bob, shift=RIGHT * 0.5),
            FadeOut(cap),
            run_time=0.5,
        )

    # ═══════════════════════════════════════════════ 3. SIGNING
    def scene_signing(self):
        self._show_progress(3)
        self._section_card(3, "Sign with Private Key", YELLOW_D)
        cap = self._show_cap("Step 3 — Alice signs the transaction with her private key")

        tx = self.tx_card
        self.play(
            tx.animate.move_to(RIGHT * 1.5 + DOWN * 0.1).scale(0.9),
            run_time=0.5,
        )

        priv = KeyIcon(color=NEON_RED, label="Alice's Private Key", scale_f=1.4)
        priv.move_to(LEFT * 4.5 + UP * 0.5)
        self.play(
            priv.shift(LEFT * 1.5).animate.shift(RIGHT * 1.5),
            run_time=0.6, rate_func=smooth,
        )

        cap = self._update_cap(cap, "The private key creates a unique digital signature")

        sign_beam = Line(
            priv.icon.get_right() + RIGHT * 0.1,
            tx.outer.get_left() + LEFT * 0.05,
            color=YELLOW_D, stroke_width=3, stroke_opacity=0.7,
        )
        beam_glow = sign_beam.copy().set_stroke(width=10, opacity=0.08)
        sign_lbl = Text("Signs", font_size=15, color=YELLOW_D, weight=BOLD)
        sign_lbl.next_to(sign_beam, UP, buff=0.08)
        self.play(
            Create(sign_beam, run_time=0.6),
            FadeIn(beam_glow), FadeIn(sign_lbl),
        )

        dot = Dot(color=YELLOW_D, radius=0.06)
        dot.move_to(sign_beam.get_start())
        self.play(
            MoveAlongPath(dot, sign_beam),
            run_time=0.5, rate_func=rush_from,
        )
        self.play(
            Flash(
                tx.outer.get_left(), color=YELLOW,
                flash_radius=0.4, line_length=0.1, num_lines=10,
            ),
            FadeOut(dot),
            run_time=0.3,
        )

        lock_body = RoundedRectangle(
            width=0.5, height=0.4, corner_radius=0.04,
            color=YELLOW_D, fill_opacity=0.25, stroke_width=2.5,
        )
        lock_arc = Arc(
            radius=0.15, start_angle=0, angle=PI,
            color=YELLOW_D, stroke_width=3,
        ).shift(UP * 0.2)
        lock = VGroup(lock_body, lock_arc)
        sig_txt = Text("Signed ✓", font_size=16, color=YELLOW_D, weight=BOLD)
        sig_group = VGroup(lock, sig_txt).arrange(RIGHT, buff=0.15)
        sig_group.next_to(tx.outer, DOWN, buff=0.55)

        self.play(GrowFromCenter(sig_group), run_time=0.5)
        self.play(
            Flash(
                sig_group.get_center(), color=YELLOW, flash_radius=0.7,
                line_length=0.15, num_lines=14, run_time=0.5,
            ),
        )

        verify = Text(
            "Anyone with Alice's public key can verify this signature",
            font_size=16, color=NEON_GRN,
        )
        verify.next_to(sig_group, DOWN, buff=0.2)
        self.play(FadeIn(verify, shift=UP * 0.1), run_time=0.5)
        self.wait(0.6)

        scene = VGroup(tx, priv, sign_beam, beam_glow, sign_lbl, sig_group, verify)
        self.play(FadeOut(scene, shift=LEFT * 0.3), FadeOut(cap), run_time=0.5)

    # ═══════════════════════════════════════════════ 4. BROADCAST
    def scene_broadcast(self):
        self._show_progress(4)
        self._section_card(4, "Broadcast to Network", NEON_GRN)
        cap = self._show_cap("Step 4 — Alice sends the transaction to the network")

        net_label = Text("Bitcoin P2P Network", font_size=17, color=GREY_B)
        net_label.move_to(RIGHT * 1.0 + UP * 2.4)
        network = NetworkGraph(scale_f=0.7, node_r=0.2)
        network.move_to(RIGHT * 1.0 + DOWN * 0.1)

        alice_node = VGroup(
            Circle(
                radius=0.3, color=BLUE_C,
                fill_opacity=0.5, stroke_width=2.5,
            ),
            Text("A", font_size=16, color=BLUE_C, weight=BOLD),
        )
        alice_node[1].move_to(alice_node[0])
        alice_node.move_to(LEFT * 4.8)

        self.play(
            FadeIn(alice_node, shift=RIGHT * 0.3),
            Create(network, run_time=1.0),
            FadeIn(net_label, shift=DOWN * 0.1),
        )

        conn = DashedLine(
            alice_node.get_right(), network.nodes[0].get_left(),
            color=GREY_B, stroke_width=1.5, dash_length=0.1,
        )
        self.play(Create(conn), run_time=0.4)

        packet = TxPacket("tx", color=ROYAL, radius=0.18)
        packet.move_to(alice_node.get_center())
        self.play(FadeIn(packet, scale=0.3), run_time=0.25)

        path = Line(alice_node.get_center(), network.nodes[0].get_center())
        trail = path.copy().set_stroke(color=ROYAL, width=2, opacity=0.3)
        self.play(
            MoveAlongPath(packet, path),
            Create(trail),
            run_time=0.6,
        )
        self.play(FadeOut(packet), FadeOut(trail), run_time=0.15)
        self.play(
            network.nodes[0].animate.set_color(NEON_GRN).set_fill(NEON_GRN, 0.35),
            Flash(
                network.nodes[0], color=NEON_GRN, flash_radius=0.35,
                line_length=0.12, num_lines=8, run_time=0.3,
            ),
            run_time=0.3,
        )

        cap = self._update_cap(cap, "Each node validates and relays to its neighbours")

        waves = network.propagation_waves(0)
        for wave in waves:
            anims = []
            for idx in wave:
                anims.append(
                    network.nodes[idx].animate.set_color(NEON_GRN).set_fill(NEON_GRN, 0.35),
                )
                anims.append(
                    Flash(
                        network.nodes[idx], color=NEON_GRN, flash_radius=0.3,
                        line_length=0.1, num_lines=8, run_time=0.35,
                    ),
                )
            self.play(*anims, run_time=0.4)

        done_txt = Text(
            "All nodes received the transaction", font_size=17,
            color=NEON_GRN, weight=BOLD,
        )
        done_txt.next_to(network, DOWN, buff=0.4)
        self.play(FadeIn(done_txt, shift=UP * 0.1), run_time=0.4)
        self.wait(0.5)

        scene = VGroup(alice_node, network, conn, net_label, done_txt)
        self.play(FadeOut(scene, shift=RIGHT * 0.3), FadeOut(cap), run_time=0.5)

    # ═══════════════════════════════════════════════ 5. MEMPOOL & VALIDATION
    def scene_mempool(self):
        self._show_progress(5)
        self._section_card(5, "Validate & Enter Mempool", ROYAL)
        cap = self._show_cap("Step 5 — Each node validates the transaction")

        checks = [
            ("Is the digital signature valid?", NEON_GRN),
            ("Do the input UTXOs exist and are unspent?", NEON_GRN),
            ("Is there no double-spend attempt?", NEON_GRN),
            ("Is the transaction format correct?", NEON_GRN),
        ]
        v_title = Text("Node Validation", font_size=28, color=ROYAL, weight=BOLD)
        v_title.move_to(UP * 2.3)
        self.play(FadeIn(v_title, shift=DOWN * 0.15), run_time=0.4)

        check_group = VGroup()
        for txt, col in checks:
            tick = Text("✓", font_size=22, color=col, weight=BOLD)
            tick.set_opacity(0)
            desc = Text(txt, font_size=18, color=col)
            row = VGroup(tick, desc).arrange(RIGHT, buff=0.15)
            check_group.add(row)
        check_group.arrange(DOWN, buff=0.26, aligned_edge=LEFT)
        check_group.move_to(UP * 0.4 + LEFT * 0.3)

        for row in check_group:
            self.play(FadeIn(row[1], shift=RIGHT * 0.2), run_time=0.28)
            self.play(row[0].animate.set_opacity(1), run_time=0.18)
            self.wait(0.06)

        passed = Text(
            "All checks passed — transaction accepted!",
            font_size=19, color=NEON_GRN, weight=BOLD,
        )
        passed.next_to(check_group, DOWN, buff=0.4)
        self.play(
            FadeIn(passed, scale=1.12),
            Flash(
                passed.get_center(), color=GREEN, flash_radius=1.0,
                line_length=0.15, num_lines=12, run_time=0.5,
            ),
            run_time=0.5,
        )
        self.wait(0.3)
        self.play(
            FadeOut(v_title), FadeOut(check_group), FadeOut(passed),
            run_time=0.4,
        )

        cap = self._update_cap(
            cap, "The transaction enters the mempool — a waiting room",
        )

        mempool = MempoolContainer(width=5.0, height=3.4)
        mempool.move_to(UP * 0.1)
        self.play(
            DrawBorderThenFill(mempool.container, run_time=0.6),
            Write(mempool.title), FadeIn(mempool.subtitle),
            run_time=0.7,
        )

        tx_data = [
            ("tx₁", "0.5 BTC → Bob", ROYAL, True),
            ("tx₂", "0.3 BTC → Carol", TEAL_D, False),
            ("tx₃", "1.2 BTC → Dave", PURPLE_A, False),
            ("tx₄", "0.08 BTC → Eve", MAROON_D, False),
            ("tx₅", "2.0 BTC → Frank", ORANGE, False),
        ]
        tx_items = []
        for i, (txid, desc, color, is_ours) in enumerate(tx_data):
            tx_rect = RoundedRectangle(
                width=4.2, height=0.45, corner_radius=0.06,
                color=color, fill_opacity=0.1, stroke_width=2,
            )
            bubble = Circle(radius=0.15, color=color, fill_opacity=0.75)
            tx_text = Text(txid, font_size=12, weight=BOLD)
            tx_text.move_to(bubble)
            desc_text = Text(desc, font_size=14, color=GREY_B)
            txid_grp = VGroup(bubble, tx_text)
            txid_grp.move_to(tx_rect.get_left() + RIGHT * 0.45)
            desc_text.next_to(txid_grp, RIGHT, buff=0.2)
            item = VGroup(tx_rect, txid_grp, desc_text)
            target_pos = mempool.slot_pos(i)
            item.move_to(mempool.container.get_right() + RIGHT * 2)
            tx_items.append((item, target_pos, is_ours))

        for item, pos, _ in tx_items:
            self.play(item.animate.move_to(pos), run_time=0.3)

        our_item = tx_items[0][0]
        ptr = Arrow(
            our_item.get_left() + LEFT * 0.15,
            our_item.get_left() + LEFT * 1.2,
            buff=0, color=BLUE_C, stroke_width=2.5,
        )
        ptr_lbl = Text("Alice's tx", font_size=14, color=BLUE_C, weight=BOLD)
        ptr_lbl.next_to(ptr, LEFT, buff=0.1)
        self.play(Create(ptr), FadeIn(ptr_lbl), run_time=0.4)
        self.play(Circumscribe(our_item, color=BLUE, buff=0.04), run_time=0.5)
        self.wait(0.5)

        all_items = VGroup(*[it for it, _, _ in tx_items])
        scene = VGroup(mempool, all_items, ptr, ptr_lbl)
        self.play(FadeOut(scene, shift=DOWN * 0.3), FadeOut(cap), run_time=0.5)

    # ═══════════════════════════════════════════════ 6. MINING
    def scene_mining(self):
        self._show_progress(6)
        self._section_card(6, "Mine Into a Block", GOLD)
        cap = self._show_cap("Step 6 — A miner picks transactions and builds a block")

        miner = create_avatar("Miner", color=GOLD, radius=0.4)
        miner.move_to(LEFT * 5.2 + UP * 1.0)
        self.play(
            FadeIn(miner, shift=RIGHT * 0.6, scale=0.8),
            run_time=0.5,
        )

        mp = RoundedRectangle(
            width=2.2, height=2.0, corner_radius=0.12,
            color=ROYAL, fill_opacity=0.05, stroke_width=2,
        )
        mp.move_to(LEFT * 1.8 + UP * 1.0)
        mp_lbl = Text("Mempool", font_size=15, color=ROYAL)
        mp_lbl.next_to(mp, UP, buff=0.08)
        self.play(DrawBorderThenFill(mp), FadeIn(mp_lbl), run_time=0.5)

        tx_colors = [ROYAL, CYAN, PURPLE_A, ORANGE]
        tx_names = ["tx₁", "tx₂", "tx₃", "tx₄"]
        tx_dots = VGroup()
        for col, nm in zip(tx_colors, tx_names):
            c = Circle(radius=0.16, color=col, fill_opacity=0.7, stroke_width=1.5)
            t = Text(nm, font_size=10, weight=BOLD)
            t.move_to(c)
            tx_dots.add(VGroup(c, t))
        tx_dots.arrange_in_grid(2, 2, buff=0.12)
        tx_dots.move_to(mp.get_center())
        self.play(FadeIn(tx_dots, scale=0.6), run_time=0.4)

        block_frame = Rectangle(
            width=3.0, height=2.4, color=NEON_GRN,
            fill_opacity=0.06, stroke_width=2.5,
        )
        block_frame.move_to(RIGHT * 2.5 + UP * 1.0)
        block_hdr = Text("Block #7", font_size=20, weight=BOLD, color=NEON_GRN)
        block_hdr.next_to(block_frame, UP, buff=0.1)
        self.play(
            DrawBorderThenFill(block_frame),
            Write(block_hdr),
            run_time=0.6,
        )

        pick_arrow = Arrow(
            mp.get_right(), block_frame.get_left(),
            buff=0.15, color=GOLD, stroke_width=2.5,
        )
        pick_lbl = Text("Highest-fee txs", font_size=12, color=GOLD)
        pick_lbl.next_to(pick_arrow, UP, buff=0.05)
        self.play(GrowArrow(pick_arrow), FadeIn(pick_lbl), run_time=0.5)

        tx_copies = tx_dots.copy()
        tx_copies.generate_target()
        tx_copies.target.arrange_in_grid(2, 2, buff=0.1)
        tx_copies.target.move_to(block_frame.get_center() + UP * 0.1)
        self.play(MoveToTarget(tx_copies), run_time=0.6)
        self.wait(0.2)

        cap = self._update_cap(
            cap, "The miner tries trillions of nonces to find a valid hash",
        )

        nonce_d = Text("Nonce: 0", font_size=17, color=ORANGE)
        nonce_d.next_to(block_frame, DOWN, buff=0.2)
        hash_d = Text("Hash: ????????...????", font_size=13, color=GREY_B)
        hash_d.next_to(nonce_d, DOWN, buff=0.1)
        target_txt = Text(
            "Target: hash must start with 000000...",
            font_size=12, color=GREY,
        )
        target_txt.next_to(hash_d, DOWN, buff=0.1)
        self.play(
            FadeIn(nonce_d), FadeIn(hash_d), FadeIn(target_txt),
            run_time=0.4,
        )

        mining_steps = [
            (0.22, "3,441", "8f3a1bc2...91cb"),
            (0.19, "18,203", "d20ef47a...f4a2"),
            (0.16, "51,887", "b791ccde...55e3"),
            (0.13, "107,442", "4c082139...aa17"),
            (0.10, "189,991", "e2f1ab73...3b09"),
            (0.08, "248,556", "1d9c07e4...c8e4"),
            (0.06, "301,012", "a33f19b8...ee71"),
            (0.05, "355,840", "7bc4f2e1...dd93"),
            (0.04, "377,291", "f8e12ca5...1107"),
            (0.03, "389,445", "c2f84d91...87b2"),
        ]
        for speed, nonce, hash_v in mining_steps:
            nn = Text(f"Nonce: {nonce}", font_size=17, color=ORANGE).move_to(nonce_d)
            hh = Text(f"Hash: {hash_v}", font_size=13, color=NEON_RED).move_to(hash_d)
            self.play(
                Transform(nonce_d, nn), Transform(hash_d, hh),
                run_time=speed,
            )

        self.wait(0.12)

        final_n = Text(
            "Nonce: 392,117", font_size=17,
            color=NEON_GRN, weight=BOLD,
        ).move_to(nonce_d)
        final_h = Text(
            "Hash: 000000...7f2a ✓", font_size=13,
            color=NEON_GRN, weight=BOLD,
        ).move_to(hash_d)
        self.play(
            Transform(nonce_d, final_n),
            Transform(hash_d, final_h),
            run_time=0.3,
        )

        self.play(
            Flash(
                block_frame.get_center(), color=NEON_GRN, flash_radius=2.0,
                line_length=0.3, num_lines=24, run_time=0.6,
            ),
            block_frame.animate.set_color(NEON_GRN).set_fill(NEON_GRN, 0.12),
            Circumscribe(
                VGroup(block_frame, block_hdr), color=NEON_GRN, buff=0.08,
            ),
            run_time=0.7,
        )

        self._zoom(block_frame.get_center() + DOWN * 0.5, scale=1.3, rt=0.4)

        mined_txt = Text("Block Mined!", font_size=30, color=NEON_GRN, weight=BOLD)
        mined_txt.move_to(DOWN * 2.8)
        self.play(
            FadeIn(mined_txt, scale=1.3),
            Flash(
                mined_txt.get_center(), color=NEON_GRN, flash_radius=1.5,
                line_length=0.2, num_lines=16, run_time=0.5,
            ),
            run_time=0.5,
        )
        self.wait(0.5)

        self._zoom_reset(rt=0.4)
        scene = VGroup(
            miner, mp, mp_lbl, tx_dots, block_frame, block_hdr,
            pick_arrow, pick_lbl, tx_copies,
            nonce_d, hash_d, target_txt, mined_txt,
        )
        self.play(FadeOut(scene, shift=UP * 0.3), FadeOut(cap), run_time=0.5)

    # ═══════════════════════════════════════════════ 7. CONFIRMATIONS
    def scene_confirmations(self):
        self._show_progress(7)
        self._section_card(7, "Confirm on Blockchain", YELLOW_D)
        cap = self._show_cap("Step 7 — The block is added to the blockchain")

        chain = BlockChain(
            start_pos=LEFT * 5.8 + DOWN * 0.3, gap=0.12,
            block_width=1.05, block_height=0.65,
            font_size=16, tx_font_size=10, tx_radius=0.10,
        )

        for i in range(5, 7):
            chain.add_block(self, str(i), color=ROYAL)

        cap = self._update_cap(
            cap,
            "Block 7 contains Alice's transaction — that's 1 confirmation",
        )

        b7 = chain.add_block(self, "7", txids=["tx"], color=NEON_GRN)
        self.play(
            Circumscribe(b7, color=GREEN, buff=0.06),
            Flash(
                b7.get_center(), color=GREEN, flash_radius=0.6,
                line_length=0.12, num_lines=10, run_time=0.5,
            ),
            run_time=0.7,
        )

        conf_lbl = Text("1 confirmation", font_size=20, color=NEON_GRN)
        conf_lbl.next_to(b7, UP, buff=0.45)
        conf_arrow = Arrow(
            conf_lbl.get_bottom(), b7.get_top(),
            buff=0.05, color=NEON_GRN, stroke_width=2,
            max_tip_length_to_length_ratio=0.25,
        )
        self.play(FadeIn(conf_lbl, shift=DOWN * 0.1), Create(conf_arrow), run_time=0.4)
        self.wait(0.3)

        cap = self._update_cap(
            cap, "Every new block on top adds another confirmation",
        )

        for i, num in enumerate([8, 9, 10, 11, 12]):
            chain.add_block(self, str(num), color=ROYAL)
            new_c = Text(
                f"{i + 2} confirmations", font_size=20, color=NEON_GRN,
            )
            new_c.move_to(conf_lbl)
            self.play(Transform(conf_lbl, new_c), run_time=0.2)

        self.play(FadeOut(conf_arrow), run_time=0.2)

        final_lbl = Text(
            "6 confirmations — practically irreversible",
            font_size=21, color=YELLOW_D, weight=BOLD,
        )
        final_lbl.next_to(chain, UP, buff=0.55)
        self.play(ReplacementTransform(conf_lbl, final_lbl), run_time=0.5)
        self.play(
            Circumscribe(final_lbl, color=YELLOW, buff=0.06),
            run_time=0.6,
        )
        self.wait(0.4)

        safe = Text(
            "Bob can now trust the payment is final",
            font_size=19, color=NEON_GRN,
        )
        safe.next_to(final_lbl, DOWN, buff=0.15)
        self.play(FadeIn(safe, shift=UP * 0.1), run_time=0.4)
        self.wait(0.6)

        scene = VGroup(chain, final_lbl, safe)
        self.play(FadeOut(scene, shift=DOWN * 0.3), FadeOut(cap), run_time=0.5)

    # ═══════════════════════════════════════════════ OUTRO
    def scene_outro(self):
        if hasattr(self, "_progress"):
            self.play(FadeOut(self._progress), run_time=0.3)
        self.play(FadeOut(self.top_title), FadeOut(self.bg_dots), run_time=0.4)

        recap = Text(
            "The Transaction Lifecycle", font_size=34, weight=BOLD,
        )
        recap.move_to(UP * 3.0)
        line = Line(LEFT * 3.2, RIGHT * 3.2, color=GOLD, stroke_width=2.5)
        line.next_to(recap, DOWN, buff=0.12)
        self.play(FadeIn(recap, shift=DOWN * 0.2), Create(line), run_time=0.5)

        steps = [
            ("1", "Create wallet & keys", BLUE_C),
            ("2", "Build the transaction", GOLD),
            ("3", "Sign with private key", YELLOW_D),
            ("4", "Broadcast to network", NEON_GRN),
            ("5", "Validate & enter mempool", ROYAL),
            ("6", "Mine into a block", GOLD),
            ("7", "Confirm on the blockchain", YELLOW_D),
        ]

        rows = VGroup()
        for num, desc, color in steps:
            bullet = Circle(
                radius=0.16, color=color,
                fill_opacity=0.5, stroke_width=2,
            )
            n_txt = Text(num, font_size=14, color=WHITE, weight=BOLD)
            n_txt.move_to(bullet)
            desc_txt = Text(desc, font_size=19, color=GREY_B)
            row = VGroup(VGroup(bullet, n_txt), desc_txt).arrange(RIGHT, buff=0.25)
            rows.add(row)
        rows.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        rows.next_to(line, DOWN, buff=0.35)

        timeline = VGroup()
        for i in range(len(rows) - 1):
            tl = Line(
                rows[i][0].get_bottom() + DOWN * 0.03,
                rows[i + 1][0].get_top() + UP * 0.03,
                color=GREY_E, stroke_width=1.5, stroke_opacity=0.4,
            )
            timeline.add(tl)

        for i, row in enumerate(rows):
            anims = [FadeIn(row, shift=RIGHT * 0.4)]
            if i > 0:
                anims.append(Create(timeline[i - 1]))
            self.play(*anims, run_time=0.22)

        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
