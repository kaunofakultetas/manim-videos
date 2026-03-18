from manim import *
import numpy as np
from components.wallet import create_person, KeyIcon, CoinIcon, WalletShape, AddressLabel
from components.transaction import UTXOCoin, TransactionBox, TxPacket
from components.network import P2PNetwork, MempoolPool
from components.blockchain import SimpleChain, ChainBlock

BG = "#0e0e0e"

def bg_dots(scene):
    dots = VGroup()
    for x in np.arange(-7, 7.5, 1.0):
        for y in np.arange(-4, 4.5, 1.0):
            d = Dot(point=[x, y, 0], radius=0.015, color=GREY_E)
            d.set_opacity(0.25)
            dots.add(d)
    scene.add(dots)

def top_title(scene):
    t = Text("Bitcoin Transaction", font_size=56, weight=BOLD).scale(0.35)
    t.to_edge(UP, buff=0.18)
    scene.add(t)
    return t

def progress(scene, step, total=7):
    bar_w = 4.0; bar_h = 0.06
    bar_bg = RoundedRectangle(width=bar_w, height=bar_h, corner_radius=0.03,
                               color=GREY_E, fill_opacity=0.3, stroke_width=0)
    fill_w = max(0.08, bar_w * step / total)
    bar_fill = RoundedRectangle(width=fill_w, height=bar_h, corner_radius=0.03,
                                 color=YELLOW_D, fill_opacity=0.8, stroke_width=0)
    bar_fill.align_to(bar_bg, LEFT)
    lbl = Text(f"{step}/{total}", font_size=12, color=GREY_B)
    lbl.next_to(bar_bg, RIGHT, buff=0.15)
    p = VGroup(bar_bg, bar_fill, lbl).to_corner(DR, buff=0.3)
    scene.add(p)


class S1_Wallet(Scene):
    def construct(self):
        self.camera.background_color = BG
        bg_dots(self); top_title(self); progress(self, 1)
        cap = Text("A wallet is really just a pair of cryptographic keys", font_size=26).to_edge(DOWN, buff=0.35)
        self.add(cap)
        alice = create_person("Alice", color=BLUE_C).scale(0.75).move_to(LEFT * 5 + UP * 0.3)
        wallet = WalletShape("Alice", color=BLUE_C, width=3.4, height=2.0).move_to(RIGHT * 0.5 + UP * 0.5)
        self.add(alice, wallet)
        priv_key = KeyIcon(color=RED_D, label="Private Key", scale_f=1.2).move_to(wallet.body.get_center() + UP * 0.35)
        pub_key = KeyIcon(color=GREEN_D, label="Public Key", scale_f=1.2).move_to(wallet.body.get_center() + DOWN * 0.35)
        self.add(priv_key, pub_key)
        pn = Text("Keep secret!", font_size=15, color=RED_D).next_to(priv_key, RIGHT, buff=0.3)
        ppn = Text("Share with anyone", font_size=15, color=GREEN_D).next_to(pub_key, RIGHT, buff=0.3)
        self.add(pn, ppn)
        addr = AddressLabel("1A1zP1...QGefi2", color=TEAL_C).move_to(DOWN * 1.4 + RIGHT * 0.5)
        arrow = CurvedArrow(pub_key.get_bottom() + DOWN * 0.05, addr.get_top() + UP * 0.05,
                             color=TEAL_C, stroke_width=2.5, angle=-0.3)
        hl = Text("Hash", font_size=14, color=TEAL_C).next_to(arrow, RIGHT, buff=0.08)
        self.add(arrow, hl, addr)


class S2_Transaction(Scene):
    def construct(self):
        self.camera.background_color = BG
        bg_dots(self); top_title(self); progress(self, 2)
        cap = Text("She spends the coin, creating new outputs for Bob and herself", font_size=26).to_edge(DOWN, buff=0.35)
        self.add(cap)
        alice = create_person("Alice", color=BLUE_C).scale(0.65).move_to(LEFT * 5.5 + UP * 1.5)
        bob = create_person("Bob", color=GREEN_C).scale(0.65).move_to(RIGHT * 5.5 + UP * 1.5)
        self.add(alice, bob)
        tx = TransactionBox(txid="a4f2...c7e1",
            inputs=[{"amount": "1.0 BTC", "label": "Alice's coin"}],
            outputs=[{"amount": "0.5 BTC", "label": "→ Bob"},
                     {"amount": "0.4999", "label": "→ Alice (change)"}],
            fee="0.0001 BTC", width=5.4).move_to(DOWN * 0.3)
        self.add(tx)


class S3_Signing(Scene):
    def construct(self):
        self.camera.background_color = BG
        bg_dots(self); top_title(self); progress(self, 3)
        cap = Text("The private key creates a unique digital signature", font_size=26).to_edge(DOWN, buff=0.35)
        self.add(cap)
        tx = TransactionBox(txid="a4f2...c7e1",
            inputs=[{"amount": "1.0 BTC", "label": "Alice's coin"}],
            outputs=[{"amount": "0.5 BTC", "label": "→ Bob"},
                     {"amount": "0.4999", "label": "→ Alice (change)"}],
            fee="0.0001 BTC", width=5.4).move_to(RIGHT * 1.5 + DOWN * 0.1).scale(0.9)
        self.add(tx)
        pk = KeyIcon(color=RED_D, label="Alice's Private Key", scale_f=1.4).move_to(LEFT * 4.5 + UP * 0.5)
        self.add(pk)
        sa = CurvedArrow(pk.get_right() + RIGHT * 0.1, tx.get_left() + LEFT * 0.1 + UP * 0.2,
                          color=YELLOW_D, stroke_width=2.5, angle=-0.4)
        sl = Text("Signs", font_size=16, color=YELLOW_D).next_to(sa, UP, buff=0.05)
        self.add(sa, sl)
        lock = VGroup(
            RoundedRectangle(width=0.5, height=0.4, corner_radius=0.04, color=YELLOW_D, fill_opacity=0.3, stroke_width=2.5),
            Arc(radius=0.15, start_angle=0, angle=PI, color=YELLOW_D, stroke_width=3).shift(UP * 0.2))
        sg = VGroup(lock, Text("Signed ✓", font_size=16, color=YELLOW_D, weight=BOLD)).arrange(RIGHT, buff=0.15)
        sg.next_to(tx.outer, DOWN, buff=0.5)
        self.add(sg)
        vn = Text("Anyone with Alice's public key can verify this signature", font_size=17, color=GREEN_D)
        vn.next_to(sg, DOWN, buff=0.25)
        self.add(vn)


class S5_Mempool(Scene):
    def construct(self):
        self.camera.background_color = BG
        bg_dots(self); top_title(self); progress(self, 5)
        cap = Text("The transaction enters the mempool — a waiting room", font_size=26).to_edge(DOWN, buff=0.35)
        self.add(cap)
        mempool = MempoolPool(width=5.0, height=3.4).move_to(UP * 0.1)
        self.add(mempool)
        tx_data = [("tx₁", "0.5 BTC → Bob", BLUE_D), ("tx₂", "0.3 BTC → Carol", TEAL_D),
                   ("tx₃", "1.2 BTC → Dave", PURPLE_B), ("tx₄", "0.08 BTC → Eve", MAROON_D),
                   ("tx₅", "2.0 BTC → Frank", ORANGE)]
        for i, (txid, desc, color) in enumerate(tx_data):
            r = RoundedRectangle(width=4.2, height=0.45, corner_radius=0.06, color=color, fill_opacity=0.12, stroke_width=2)
            b = Circle(radius=0.15, color=color, fill_opacity=0.8)
            tt = Text(txid, font_size=12, weight=BOLD); tt.move_to(b)
            dt = Text(desc, font_size=14, color=GREY_B)
            tg = VGroup(b, tt); tg.move_to(r.get_left() + RIGHT * 0.45)
            dt.next_to(tg, RIGHT, buff=0.2)
            item = VGroup(r, tg, dt).move_to(mempool.get_slot_position(i))
            self.add(item)
            if i == 0:
                ptr = Arrow(item.get_left() + LEFT * 0.15, item.get_left() + LEFT * 1.2,
                             buff=0, color=BLUE_C, stroke_width=2.5)
                pl = Text("Alice's tx", font_size=15, color=BLUE_C, weight=BOLD).next_to(ptr, LEFT, buff=0.1)
                self.add(ptr, pl)


class S6_Mining(Scene):
    def construct(self):
        self.camera.background_color = BG
        bg_dots(self); top_title(self); progress(self, 6)
        cap = Text("The miner tries trillions of nonces to find a valid hash (Proof of Work)", font_size=26).to_edge(DOWN, buff=0.35)
        self.add(cap)
        miner = create_person("Miner", color=YELLOW_D).scale(0.65).move_to(LEFT * 5.2 + UP * 1.0)
        self.add(miner)
        mp = RoundedRectangle(width=2.2, height=2.0, corner_radius=0.12, color=BLUE_C, fill_opacity=0.06, stroke_width=2).move_to(LEFT * 1.8 + UP * 1.0)
        ml = Text("Mempool", font_size=16, color=BLUE_C).next_to(mp, UP, buff=0.08)
        self.add(mp, ml)
        block_r = Rectangle(width=3.0, height=2.4, color=GREEN_D, fill_opacity=0.1, stroke_width=2.5).move_to(RIGHT * 2.5 + UP * 1.0)
        bh = Text("Block #7", font_size=20, weight=BOLD, color=GREEN_D).next_to(block_r, UP, buff=0.1)
        self.add(block_r, bh)
        pa = Arrow(mp.get_right(), block_r.get_left(), buff=0.15, color=YELLOW_D, stroke_width=2.5)
        pl = Text("Highest-fee txs", font_size=13, color=YELLOW_D).next_to(pa, UP, buff=0.05)
        self.add(pa, pl)
        nd = Text("Nonce: 392,117", font_size=18, color=GREEN_D, weight=BOLD).next_to(block_r, DOWN, buff=0.2)
        hd = Text("Hash: 000000...7f2a ✓", font_size=14, color=GREEN_D, weight=BOLD).next_to(nd, DOWN, buff=0.12)
        tt = Text("Target: hash must start with 000000...", font_size=13, color=GREY).next_to(hd, DOWN, buff=0.12)
        mt = Text("Block mined!", font_size=28, color=GREEN_D, weight=BOLD).move_to(DOWN * 2.6)
        self.add(nd, hd, tt, mt)


class S7_Confirmations(Scene):
    def construct(self):
        self.camera.background_color = BG
        bg_dots(self); top_title(self); progress(self, 7)
        cap = Text("Every new block on top adds another confirmation", font_size=26).to_edge(DOWN, buff=0.35)
        self.add(cap)
        chain = SimpleChain(block_width=1.05, block_height=0.65, block_gap=0.12,
                            font_size=16, tx_font_size=10, tx_radius=0.10, start_pos=LEFT * 5.8 + DOWN * 0.3)
        for i in range(5, 13):
            c = GREEN_D if i == 7 else BLUE_D
            t = ["tx"] if i == 7 else None
            b = ChainBlock(str(i), txids=t, color=c, width=1.05, height=0.65, font_size=16, tx_font_size=10, tx_radius=0.10)
            if chain.blocks: b.next_to(chain.blocks[-1], RIGHT, buff=0.12)
            else: b.move_to(LEFT * 5.8 + DOWN * 0.3)
            chain.blocks.append(b); chain.add(b)
            if len(chain.blocks) > 1:
                p = chain.blocks[-2]
                l = Line(p.get_right(), b.get_left(), color=YELLOW_D, stroke_width=3)
                chain.connectors.add(l); chain.add(l)
        fl = Text("6 confirmations — practically irreversible", font_size=22, color=YELLOW_D, weight=BOLD)
        fl.next_to(chain, UP, buff=0.55)
        st = Text("Bob can now trust the payment is final", font_size=20, color=GREEN_D)
        st.next_to(fl, DOWN, buff=0.15)
        self.add(chain, fl, st)
