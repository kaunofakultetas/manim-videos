from manim import *
import numpy as np


class NetworkGraph(VGroup):
    POSITIONS = [
        [-2.8, 1.2, 0], [-1.0, 2.2, 0], [1.2, 2.1, 0],
        [2.8, 1.0, 0], [2.2, -0.9, 0], [0.0, -1.4, 0],
        [-2.2, -0.9, 0], [0.0, 0.5, 0],
    ]
    EDGES = [
        (0, 1), (0, 6), (0, 7), (1, 2), (1, 7),
        (2, 3), (2, 7), (3, 4), (4, 5), (4, 7),
        (5, 6), (5, 7), (6, 7),
    ]

    def __init__(self, scale_f=0.65, node_r=0.22, **kwargs):
        super().__init__(**kwargs)
        self.nodes = VGroup()
        self.edges_group = VGroup()
        self.labels = VGroup()
        for i, pos in enumerate(self.POSITIONS):
            n = Circle(
                radius=node_r, color=BLUE_C,
                fill_opacity=0.25, stroke_width=2,
            )
            n.move_to(np.array(pos) * scale_f)
            lbl = Text(f"N{i + 1}", font_size=9, color=GREY_B)
            lbl.move_to(n)
            self.nodes.add(n)
            self.labels.add(lbl)
        for i, j in self.EDGES:
            l = Line(
                self.nodes[i].get_center(), self.nodes[j].get_center(),
                stroke_width=1, color=GREY_B, stroke_opacity=0.35,
            )
            self.edges_group.add(l)
        self.add(self.edges_group, self.nodes, self.labels)

    def propagation_waves(self, start=0):
        visited = {start}
        waves = []
        frontier = {start}
        adj = {i: set() for i in range(len(self.nodes))}
        for a, b in self.EDGES:
            adj[a].add(b)
            adj[b].add(a)
        while frontier:
            nxt = set()
            for n in frontier:
                for nb in adj[n]:
                    if nb not in visited:
                        nxt.add(nb)
                        visited.add(nb)
            if nxt:
                waves.append(list(nxt))
            frontier = nxt
        return waves


class MempoolContainer(VGroup):
    def __init__(self, width=5.2, height=3.6, color=BLUE_C, **kwargs):
        super().__init__(**kwargs)
        shadow = RoundedRectangle(
            width=width, height=height, corner_radius=0.18,
            color=BLACK, fill_opacity=0.15, stroke_width=0,
        )
        shadow.shift(DR * 0.05)
        self.container = RoundedRectangle(
            width=width, height=height, corner_radius=0.18,
            color=color, fill_opacity=0.04, stroke_width=2,
        )
        self.title = Text("Mempool", font_size=24, color=color, weight=BOLD)
        self.title.next_to(self.container, UP, buff=0.12)
        sub = Text("(unconfirmed transaction pool)", font_size=12, color=GREY)
        sub.next_to(self.title, DOWN, buff=0.06)
        self.subtitle = sub
        self.add(shadow, self.container, self.title, sub)

    def slot_pos(self, index):
        top = self.container.get_top() + DOWN * 0.55
        return top + DOWN * index * 0.55
