from manim import *
import numpy as np
from components.wallet import create_avatar, KeyIcon, CoinIcon, WalletCard, AddressLabel
from components.transaction import UTXOCoin, TransactionCard, TxPacket
from components.network import NetworkGraph, MempoolContainer
from components.blockchain import BlockChain, Block3D

BG = "#080c14"
GOLD = "#f7b731"
CYAN = "#45aaf2"
ROYAL = "#4a6cf7"
NEON_GRN = "#26de81"
NEON_RED = "#fc5c65"
PURPLE_A = "#a55eea"


def _bg_dots(scene):
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
    scene.add(dots)


def _top_title(scene):
    t = Text("Bitcoin Transaction", font_size=54, weight=BOLD).scale(0.32)
    t.to_edge(UP, buff=0.18)
    scene.add(t)


def _progress(scene, step, total=7):
    bar_w, bar_h = 4.0, 0.06
    bg = RoundedRectangle(
        width=bar_w, height=bar_h, corner_radius=0.03,
        color=GREY_E, fill_opacity=0.25, stroke_width=0,
    )
    fill_w = max(0.08, bar_w * step / total)
    fill = RoundedRectangle(
        width=fill_w, height=bar_h, corner_radius=0.03,
        color=GOLD, fill_opacity=0.7, stroke_width=0,
    )
    fill.align_to(bg, LEFT)
    lbl = Text(f"{step}/{total}", font_size=11, color=GREY_B)
    lbl.next_to(bg, RIGHT, buff=0.12)
    VGroup(bg, fill, lbl).to_corner(DR, buff=0.3)
    scene.add(bg, fill, lbl)


class S1_Wallet(Scene):
    def construct(self):
        self.camera.background_color = BG
        _bg_dots(self)
        _top_title(self)
        _progress(self, 1)
        cap = Text(
            "A wallet is really just a pair of cryptographic keys",
            font_size=24,
        ).to_edge(DOWN, buff=0.4)
        self.add(cap)
        alice = create_avatar("Alice", color=BLUE_C, radius=0.45)
        alice.move_to(LEFT * 5.5 + UP * 0.3)
        wallet = WalletCard("Alice", color=BLUE_C, width=3.4, height=2.2)
        wallet.move_to(RIGHT * 0.5 + UP * 0.4)
        self.add(alice, wallet)
        priv = KeyIcon(color=NEON_RED, label="Private Key", scale_f=1.2)
        priv.move_to(wallet.body.get_center() + UP * 0.3)
        pub = KeyIcon(color=NEON_GRN, label="Public Key", scale_f=1.2)
        pub.move_to(wallet.body.get_center() + DOWN * 0.45)
        self.add(priv, pub)
        pn = Text("Keep secret!", font_size=14, color=NEON_RED, weight=BOLD)
        pn.next_to(priv, RIGHT, buff=0.25)
        ppn = Text("Share freely", font_size=14, color=NEON_GRN)
        ppn.next_to(pub, RIGHT, buff=0.25)
        self.add(pn, ppn)
        addr = AddressLabel("1A1zP1...QGefi2", color=CYAN)
        addr.move_to(DOWN * 1.8 + RIGHT * 0.5)
        arrow = CurvedArrow(
            pub.get_bottom() + DOWN * 0.05, addr.get_top() + UP * 0.05,
            color=CYAN, stroke_width=2.5, angle=-0.35,
        )
        hl = Text("SHA-256 + RIPEMD-160", font_size=11, color=CYAN)
        hl.next_to(arrow, RIGHT, buff=0.08)
        self.add(arrow, hl, addr)


class S2_Transaction(Scene):
    def construct(self):
        self.camera.background_color = BG
        _bg_dots(self)
        _top_title(self)
        _progress(self, 2)
        cap = Text(
            "She creates outputs for Bob and change back to herself",
            font_size=24,
        ).to_edge(DOWN, buff=0.4)
        self.add(cap)
        alice = create_avatar("Alice", color=BLUE_C, radius=0.4)
        alice.move_to(LEFT * 5.5 + UP * 1.5)
        bob = create_avatar("Bob", color=NEON_GRN, radius=0.4)
        bob.move_to(RIGHT * 5.5 + UP * 1.5)
        self.add(alice, bob)
        tx = TransactionCard(
            txid="a4f2...c7e1",
            inputs=[{"amount": "1.0 BTC", "label": "Alice's coin"}],
            outputs=[
                {"amount": "0.5 BTC", "label": "→ Bob"},
                {"amount": "0.4999 BTC", "label": "→ Alice (change)"},
            ],
            fee="0.0001 BTC", width=5.4,
        ).move_to(DOWN * 0.2)
        self.add(tx)


class S3_Signing(Scene):
    def construct(self):
        self.camera.background_color = BG
        _bg_dots(self)
        _top_title(self)
        _progress(self, 3)
        cap = Text(
            "The private key creates a unique digital signature",
            font_size=24,
        ).to_edge(DOWN, buff=0.4)
        self.add(cap)
        tx = TransactionCard(
            txid="a4f2...c7e1",
            inputs=[{"amount": "1.0 BTC", "label": "Alice's coin"}],
            outputs=[
                {"amount": "0.5 BTC", "label": "→ Bob"},
                {"amount": "0.4999 BTC", "label": "→ Alice (change)"},
            ],
            fee="0.0001 BTC", width=5.4,
        ).move_to(RIGHT * 1.5 + DOWN * 0.1).scale(0.9)
        self.add(tx)
        pk = KeyIcon(color=NEON_RED, label="Alice's Private Key", scale_f=1.4)
        pk.move_to(LEFT * 4.5 + UP * 0.5)
        self.add(pk)
        beam = Line(
            pk.icon.get_right() + RIGHT * 0.1,
            tx.outer.get_left() + LEFT * 0.05,
            color=YELLOW_D, stroke_width=3, stroke_opacity=0.7,
        )
        sl = Text("Signs", font_size=15, color=YELLOW_D, weight=BOLD)
        sl.next_to(beam, UP, buff=0.08)
        self.add(beam, sl)
        lock_body = RoundedRectangle(
            width=0.5, height=0.4, corner_radius=0.04,
            color=YELLOW_D, fill_opacity=0.25, stroke_width=2.5,
        )
        lock_arc = Arc(
            radius=0.15, start_angle=0, angle=PI,
            color=YELLOW_D, stroke_width=3,
        ).shift(UP * 0.2)
        lock = VGroup(lock_body, lock_arc)
        sg = VGroup(lock, Text("Signed ✓", font_size=16, color=YELLOW_D, weight=BOLD))
        sg.arrange(RIGHT, buff=0.15)
        sg.next_to(tx.outer, DOWN, buff=0.55)
        self.add(sg)
        vn = Text(
            "Anyone with Alice's public key can verify this signature",
            font_size=16, color=NEON_GRN,
        )
        vn.next_to(sg, DOWN, buff=0.2)
        self.add(vn)


class S5_Mempool(Scene):
    def construct(self):
        self.camera.background_color = BG
        _bg_dots(self)
        _top_title(self)
        _progress(self, 5)
        cap = Text(
            "The transaction enters the mempool — a waiting room",
            font_size=24,
        ).to_edge(DOWN, buff=0.4)
        self.add(cap)
        mempool = MempoolContainer(width=5.0, height=3.4).move_to(UP * 0.1)
        self.add(mempool)
        tx_data = [
            ("tx₁", "0.5 BTC → Bob", ROYAL),
            ("tx₂", "0.3 BTC → Carol", TEAL_D),
            ("tx₃", "1.2 BTC → Dave", PURPLE_A),
            ("tx₄", "0.08 BTC → Eve", MAROON_D),
            ("tx₅", "2.0 BTC → Frank", ORANGE),
        ]
        for i, (txid, desc, color) in enumerate(tx_data):
            r = RoundedRectangle(
                width=4.2, height=0.45, corner_radius=0.06,
                color=color, fill_opacity=0.1, stroke_width=2,
            )
            b = Circle(radius=0.15, color=color, fill_opacity=0.75)
            tt = Text(txid, font_size=12, weight=BOLD)
            tt.move_to(b)
            dt = Text(desc, font_size=14, color=GREY_B)
            tg = VGroup(b, tt)
            tg.move_to(r.get_left() + RIGHT * 0.45)
            dt.next_to(tg, RIGHT, buff=0.2)
            item = VGroup(r, tg, dt).move_to(mempool.slot_pos(i))
            self.add(item)
            if i == 0:
                ptr = Arrow(
                    item.get_left() + LEFT * 0.15,
                    item.get_left() + LEFT * 1.2,
                    buff=0, color=BLUE_C, stroke_width=2.5,
                )
                pl = Text("Alice's tx", font_size=14, color=BLUE_C, weight=BOLD)
                pl.next_to(ptr, LEFT, buff=0.1)
                self.add(ptr, pl)


class S6_Mining(Scene):
    def construct(self):
        self.camera.background_color = BG
        _bg_dots(self)
        _top_title(self)
        _progress(self, 6)
        cap = Text(
            "The miner tries trillions of nonces to find a valid hash",
            font_size=24,
        ).to_edge(DOWN, buff=0.4)
        self.add(cap)
        miner = create_avatar("Miner", color=GOLD, radius=0.4)
        miner.move_to(LEFT * 5.2 + UP * 1.0)
        self.add(miner)
        mp = RoundedRectangle(
            width=2.2, height=2.0, corner_radius=0.12,
            color=ROYAL, fill_opacity=0.05, stroke_width=2,
        ).move_to(LEFT * 1.8 + UP * 1.0)
        ml = Text("Mempool", font_size=15, color=ROYAL)
        ml.next_to(mp, UP, buff=0.08)
        self.add(mp, ml)
        block_r = Rectangle(
            width=3.0, height=2.4, color=NEON_GRN,
            fill_opacity=0.06, stroke_width=2.5,
        ).move_to(RIGHT * 2.5 + UP * 1.0)
        bh = Text("Block #7", font_size=20, weight=BOLD, color=NEON_GRN)
        bh.next_to(block_r, UP, buff=0.1)
        self.add(block_r, bh)
        pa = Arrow(
            mp.get_right(), block_r.get_left(),
            buff=0.15, color=GOLD, stroke_width=2.5,
        )
        pl = Text("Highest-fee txs", font_size=12, color=GOLD)
        pl.next_to(pa, UP, buff=0.05)
        self.add(pa, pl)
        nd = Text("Nonce: 392,117", font_size=17, color=NEON_GRN, weight=BOLD)
        nd.next_to(block_r, DOWN, buff=0.2)
        hd = Text("Hash: 000000...7f2a ✓", font_size=13, color=NEON_GRN, weight=BOLD)
        hd.next_to(nd, DOWN, buff=0.1)
        tt = Text("Target: hash must start with 000000...", font_size=12, color=GREY)
        tt.next_to(hd, DOWN, buff=0.1)
        mt = Text("Block Mined!", font_size=30, color=NEON_GRN, weight=BOLD)
        mt.move_to(DOWN * 2.8)
        self.add(nd, hd, tt, mt)


class S7_Confirmations(Scene):
    def construct(self):
        self.camera.background_color = BG
        _bg_dots(self)
        _top_title(self)
        _progress(self, 7)
        cap = Text(
            "Every new block on top adds another confirmation",
            font_size=24,
        ).to_edge(DOWN, buff=0.4)
        self.add(cap)
        chain = BlockChain(
            start_pos=LEFT * 5.8 + DOWN * 0.3, gap=0.12,
            block_width=1.05, block_height=0.65,
            font_size=16, tx_font_size=10, tx_radius=0.10,
        )
        for i in range(5, 13):
            c = NEON_GRN if i == 7 else ROYAL
            t = ["tx"] if i == 7 else None
            b = Block3D(
                str(i), txids=t, color=c,
                width=1.05, height=0.65,
                font_size=16, tx_font_size=10, tx_radius=0.10,
            )
            if chain.blocks:
                b.next_to(chain.blocks[-1], RIGHT, buff=0.12)
            else:
                b.move_to(LEFT * 5.8 + DOWN * 0.3)
            chain.blocks.append(b)
            chain.add(b)
            if len(chain.blocks) > 1:
                prev = chain.blocks[-2]
                conn = Arrow(
                    prev.get_right() + RIGHT * 0.02,
                    b.get_left() + LEFT * 0.02,
                    buff=0, color=YELLOW_D, stroke_width=2.5,
                    max_tip_length_to_length_ratio=0.4,
                )
                chain.connectors.add(conn)
                chain.add(conn)
        fl = Text(
            "6 confirmations — practically irreversible",
            font_size=21, color=YELLOW_D, weight=BOLD,
        )
        fl.next_to(chain, UP, buff=0.55)
        st = Text(
            "Bob can now trust the payment is final",
            font_size=19, color=NEON_GRN,
        )
        st.next_to(fl, DOWN, buff=0.15)
        self.add(chain, fl, st)
