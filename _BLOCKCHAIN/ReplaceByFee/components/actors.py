from manim import *
import numpy as np

# Helper for a person icon
def create_person(label: str, color=WHITE):
    body = Line(UP * 0.5, DOWN * 0.5)
    head = Circle(radius=0.25).next_to(body.get_start(), UP, buff=0)
    leg1 = Line(body.get_end(), body.get_end() + DOWN * 0.5 + LEFT * 0.3)
    leg2 = Line(body.get_end(), body.get_end() + DOWN * 0.5 + RIGHT * 0.3)
    arm1 = Line(body.get_center() + UP*0.1, body.get_center() + LEFT * 0.4 + DOWN*0.1)
    arm2 = Line(body.get_center() + UP*0.1, body.get_center() + RIGHT * 0.4 + DOWN*0.1)
    person_drawing = VGroup(body, head, leg1, leg2, arm1, arm2).set_color(color)
    person_label = Text(label, font_size=24).next_to(person_drawing, DOWN, buff=0.2)
    return VGroup(person_drawing, person_label)

# Helper for the network visualization
def create_network(num_nodes=7, radius=1.0):
    nodes = VGroup()
    for i in range(num_nodes):
        angle = TAU * i / num_nodes + (PI / num_nodes) # offset rotation
        pos = complex_to_R3(radius * np.exp(1j * angle))
        node = Circle(radius=0.15, color=BLUE_C, fill_opacity=0.5)
        node.move_to(pos)
        nodes.add(node)
    
    connections = VGroup()
    # Fully interconnect all nodes
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            line = Line(nodes[i].get_center(), nodes[j].get_center(), stroke_width=1.5, color=GREY_B)
            connections.add(line)
    
    network_drawing = VGroup(connections, nodes)
    label = Text("Blockchain Network", font_size=24).next_to(network_drawing, DOWN, buff=0.2)
    
    return VGroup(network_drawing, label)
