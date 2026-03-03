from manim import *
from miningBlockchainView import BlockchainForkResolution
from miningTopView import MiningTopView


def fade_out(scene: Scene):
    animations = []
    for mobject in scene.mobjects:
        animations.append(FadeOut(mobject))
    scene.play(*animations)




class Main(Scene):
    def construct(self):
        # Title Fullscreen
        title = Text("Blockchain Fork and Resolution", font_size=60)
        self.play(Write(title))
        self.wait(1)
        
        # Move title to top
        self.play(title.animate.scale(0.5).to_edge(UP))
        self.wait(0.5)

        # Blockchain View
        blockchain_fork_resolution_mobjects = VGroup()
        BlockchainForkResolution.construct(self, blockchain_fork_resolution_mobjects)
        self.play(FadeOut(blockchain_fork_resolution_mobjects))

        # Top View
        mining_top_view_mobjects = VGroup()
        MiningTopView.construct(self, mining_top_view_mobjects)
        self.play(FadeOut(mining_top_view_mobjects), FadeOut(title))



