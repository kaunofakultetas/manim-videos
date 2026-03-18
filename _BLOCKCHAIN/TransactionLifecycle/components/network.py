from manim import *
import numpy as np


class P2PNetwork(VGroup):
    """A peer-to-peer network with labeled nodes and propagation support."""

    NODE_POSITIONS = [
        [-2.5, 1.0, 0],
        [-1.0, 2.0, 0],
        [1.0, 2.0, 0],
        [2.5, 1.0, 0],
        [2.0, -0.8, 0],
        [0.0, -1.2, 0],
        [-2.0, -0.8, 0],
    ]

    CONNECTIONS = [
        (0, 1), (0, 6), (1, 2), (1, 6),
        (2, 3), (2, 5), (3, 4),
        (4, 5), (5, 6),
    ]

    def __init__(self, scale_factor=0.7, node_radius=0.2, **kwargs):
        super().__init__(**kwargs)
        self.nodes = VGroup()
        self.edges = VGroup()
        self.node_labels = VGroup()

        for i, pos in enumerate(self.NODE_POSITIONS):
            node = Circle(radius=node_radius, color=BLUE_C, fill_opacity=0.35,
                           stroke_width=2.5)
            node.move_to(np.array(pos) * scale_factor)
            lbl = Text(f"N{i+1}", font_size=10, color=GREY_B)
            lbl.move_to(node)
            self.nodes.add(node)
            self.node_labels.add(lbl)

        for i, j in self.CONNECTIONS:
            line = Line(
                self.nodes[i].get_center(), self.nodes[j].get_center(),
                stroke_width=1.2, color=GREY_B, stroke_opacity=0.5,
            )
            self.edges.add(line)

        self.add(self.edges, self.nodes, self.node_labels)

    def get_propagation_order(self, start_node: int):
        visited = {start_node}
        waves = []
        frontier = {start_node}
        adj = {i: set() for i in range(len(self.nodes))}
        for i, j in self.CONNECTIONS:
            adj[i].add(j)
            adj[j].add(i)
        while frontier:
            next_wave = set()
            for node in frontier:
                for neighbor in adj[node]:
                    if neighbor not in visited:
                        next_wave.add(neighbor)
                        visited.add(neighbor)
            if next_wave:
                waves.append(list(next_wave))
            frontier = next_wave
        return waves


class MempoolPool(VGroup):
    """A visual mempool container — styled as a waiting room."""

    def __init__(self, width=4.2, height=2.8, color=BLUE_C, **kwargs):
        super().__init__(**kwargs)
        self.container = RoundedRectangle(
            width=width, height=height, corner_radius=0.18,
            color=color, fill_opacity=0.05, stroke_width=2.5,
        )
        self.title = Text("Mempool", font_size=24, color=color)
        self.title.next_to(self.container, UP, buff=0.12)
        subtitle = Text("(unconfirmed transaction pool)", font_size=13, color=GREY_B)
        subtitle.next_to(self.title, DOWN, buff=0.05)
        self.tx_slots = VGroup()
        self.add(self.container, self.title, subtitle, self.tx_slots)
        self.subtitle = subtitle

    def get_slot_position(self, index: int):
        start = self.container.get_top() + DOWN * 0.6
        return start + DOWN * index * 0.55
