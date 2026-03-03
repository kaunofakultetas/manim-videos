from manim import *


class MiningTopView:
    """
    An animation demonstrating a blockchain fork and resolution scenario.
    This scene visualizes a network of nodes, mining of blocks, and how
    a blockchain is built.
    """

    # --- Configuration ---
    NODE_CONFIG = [
        {'pos': [-2, -1, 0], 'color': GREEN},   # Middle column 1
        {'pos': [0, 1, 0],  'color': RED},     # Top column 2
        {'pos': [0, -3, 0], 'color': ORANGE},  # Bottom column 2
        {'pos': [2, -1, 0],  'color': YELLOW},  # Middle column 3
        {'pos': [4, 1, 0],  'color': BLUE},    # Top column 4
        {'pos': [4, -3, 0], 'color': PURPLE},  # Bottom column 4
    ]
    NODE_CONNECTIONS = [
        (0, 1), (0, 2), # Node 0 to 1, 2
        (1, 3), (2, 3), # Nodes 1, 2 to 3
        (3, 4), (3, 5), # Node 3 to 4, 5
        (1, 4), (2, 5), # Direct connections for fork visualization
    ]
    BLOCK_HEIGHT = 0.6
    BLOCK_WIDTH = 0.6

    @staticmethod
    def construct(scene: Scene, group: VGroup = VGroup()):
        """Main method to construct the animation."""
        
        # self.create_title() # This was disabled in the original code
        nodes, connections = MiningTopView.create_node_network(scene)
        node_blocks = MiningTopView.display_genesis_blocks_on_nodes(scene, nodes)
        main_blockchain, main_blockchain_blocks = MiningTopView.setup_main_blockchain(scene)

        # Block 1 mined by node 0
        MiningTopView.animate_simultaneous_mining(scene, [(0, 1)], nodes, node_blocks, main_blockchain, main_blockchain_blocks)

        # Node 0 propagates block 1
        MiningTopView.animate_block_propagation(scene, [(0, [1, 2])], nodes, node_blocks)
        MiningTopView.animate_block_propagation(scene, [
            (1, [3, 4]),
            (2, [5]),
        ], nodes, node_blocks)

        # Block 2 mined by node 3
        MiningTopView.animate_simultaneous_mining(scene, [(3, 2)], nodes, node_blocks, main_blockchain, main_blockchain_blocks)
        MiningTopView.animate_block_propagation(scene, [(3, [1, 2, 4, 5])], nodes, node_blocks)
        MiningTopView.animate_block_propagation(scene, [(2, [0])], nodes, node_blocks)

        # Block 3 is mined simultaneously by nodes 0 and 4, creating a fork
        MiningTopView.animate_simultaneous_mining(scene, [(0, 3), (4, 3)], nodes, node_blocks, main_blockchain, main_blockchain_blocks)
        MiningTopView.animate_block_propagation(scene, [
            (0, [1, 2]),
            (4, [1, 3]),
        ], nodes, node_blocks)
        MiningTopView.animate_block_propagation(scene, [(2, [5])], nodes, node_blocks)



        # Block 4 is mined simultaneously by nodes 3  which resolves the fork
        MiningTopView.animate_simultaneous_mining(scene, [(3, 4)], nodes, node_blocks, main_blockchain, main_blockchain_blocks)
        MiningTopView.animate_block_propagation(scene, [(3, [1, 2, 4, 5])], nodes, node_blocks)
        MiningTopView.animate_block_propagation(scene, [(1, [0])], nodes, node_blocks)
        

        # Block 5 is mined by node 1
        MiningTopView.animate_simultaneous_mining(scene, [(1, 5)], nodes, node_blocks, main_blockchain, main_blockchain_blocks)
        MiningTopView.animate_block_propagation(scene, [(1, [0,  3, 4])], nodes, node_blocks)
        MiningTopView.animate_block_propagation(scene, [(3, [2, 5])], nodes, node_blocks)

        scene.wait(2)
        
        group.add(nodes, connections, node_blocks, main_blockchain)

    @staticmethod
    def create_title(scene: Scene):
        """Creates and animates the title of the scene."""
        title = Text("Blockchain Fork and Resolution", font_size=60)
        scene.play(Write(title))
        scene.wait(1)
        scene.play(title.animate.scale(0.5).to_edge(UP))
        scene.wait(0.5)
        scene.add(title) # Keep it in the scene

    @staticmethod
    def create_node_network(scene: Scene):
        """Creates the visual representation of the node network."""
        # Create nodes (circles)
        nodes = VGroup()
        for config in MiningTopView.NODE_CONFIG:
            node = Circle(radius=0.3, color=config['color'], fill_opacity=0.5)
            node.move_to(config['pos'])
            nodes.add(node)

        # Create connections between nodes
        connections = VGroup()
        for start_idx, end_idx in MiningTopView.NODE_CONNECTIONS:
            connection = Line(nodes[start_idx], nodes[end_idx])
            connections.add(connection)

        # Animate the creation
        scene.play(Create(nodes), run_time=1)
        scene.wait(0.5)
        scene.play(Create(connections), run_time=1)
        scene.wait(1)
        return nodes, connections

    @staticmethod
    def display_genesis_blocks_on_nodes(scene: Scene, nodes):
        """Displays a '0' block above each node to represent their initial state."""
        node_blocks = VGroup()
        for node in nodes:
            block_shape = Rectangle(
                width=MiningTopView.BLOCK_WIDTH,
                height=MiningTopView.BLOCK_HEIGHT,
                color=WHITE,
                fill_opacity=0.5,
            )
            block_text = Text("0").move_to(block_shape.get_center())
            block_vgroup = VGroup(block_shape, block_text)
            block_vgroup.next_to(node, UP, buff=0.2)
            node_blocks.add(block_vgroup)

        scene.play(Create(node_blocks))
        scene.wait(1)
        return node_blocks

    @staticmethod
    def setup_main_blockchain(scene: Scene):
        """Initializes the main blockchain visualization on the left side of the screen."""
        main_blockchain = VGroup()
        main_blockchain_blocks = []

        start_pos = LEFT * 6 + DOWN * 2.5

        # Create and animate the Genesis Block
        genesis_block_shape = Rectangle(
            width=MiningTopView.BLOCK_WIDTH,
            height=MiningTopView.BLOCK_HEIGHT,
            color=WHITE, # Neutral color for genesis
            fill_opacity=0.5
        ).move_to(start_pos)
        genesis_text = Text("0").move_to(genesis_block_shape.get_center())
        genesis_vgroup = VGroup(genesis_block_shape, genesis_text)

        scene.play(Create(genesis_vgroup))
        scene.wait(0.5)

        main_blockchain_blocks.append(genesis_vgroup)
        main_blockchain.add(genesis_vgroup)
        return main_blockchain, main_blockchain_blocks

    @staticmethod
    def animate_simultaneous_mining(scene: Scene, miners_info: list[tuple[int, int]], nodes, node_blocks, main_blockchain, main_blockchain_blocks):
        """
        Animates one or more blocks being mined simultaneously.
        If more than one miner is provided, it creates a fork in the main blockchain.

        Args:
            miners_info (list[tuple[int, int]]): A list of tuples, where each
                tuple contains a miner_node_index (int) and a block_number (int).
        """
        if not miners_info:
            return

        # --- Part 1: Indicate miners and create new blocks at their positions ---
        indicate_anims = []
        mined_blocks = []
        for miner_node_index, block_number in miners_info:
            miner_node = nodes[miner_node_index]
            indicate_anims.append(Indicate(miner_node, color=miner_node.get_color(), scale_factor=1.5))

            mined_block_shape = Rectangle(
                width=MiningTopView.BLOCK_WIDTH,
                height=MiningTopView.BLOCK_HEIGHT,
                color=miner_node.get_color(),
                fill_opacity=0.5,
            )
            mined_text = Text(f"{block_number}").move_to(mined_block_shape.get_center())
            mined_vgroup = VGroup(mined_block_shape, mined_text).move_to(miner_node.get_center())
            mined_blocks.append(mined_vgroup)

        scene.play(*indicate_anims)
        scene.wait(0.2)
        scene.play(*[FadeIn(b, scale=0.5) for b in mined_blocks])
        scene.wait(0.5)

        # --- Part 2: Prepare animations for block movements ---
        blocks_for_node_display = [b.copy() for b in mined_blocks]
        prev_main_chain_block = main_blockchain_blocks[-1]
        
        main_chain_anims = []
        num_forks = len(miners_info)
        if num_forks == 1:
            target_pos = prev_main_chain_block.get_center() + UP * (MiningTopView.BLOCK_HEIGHT + 0.15)
            main_chain_anims.append(mined_blocks[0].animate.move_to(target_pos))
        else:
            fork_spacing = MiningTopView.BLOCK_WIDTH + 0.2
            total_fork_width = (num_forks - 1) * fork_spacing
            start_x = prev_main_chain_block.get_center()[0] - total_fork_width / 2
            for i, block in enumerate(mined_blocks):
                target_x = start_x + i * fork_spacing
                target_y = prev_main_chain_block.get_center()[1] + MiningTopView.BLOCK_HEIGHT + 0.15
                target_position = [target_x, target_y, 0]
                main_chain_anims.append(block.animate.move_to(target_position))

        node_display_anims = []
        old_node_blocks_to_fade = VGroup()
        for i, (miner_node_index, _) in enumerate(miners_info):
            old_node_block = node_blocks[miner_node_index]
            node_display_anims.append(blocks_for_node_display[i].animate.move_to(old_node_block.get_center()))
            old_node_blocks_to_fade.add(old_node_block)

        # --- Part 3: Execute animations ---
        scene.play(*main_chain_anims, *node_display_anims, run_time=1.5)

        scene.play(FadeOut(old_node_blocks_to_fade, run_time=0.25))
        for i, (miner_node_index, _) in enumerate(miners_info):
            node_blocks.submobjects[miner_node_index] = blocks_for_node_display[i]

        connecting_lines = []
        for block in mined_blocks:
            line = Line(
                prev_main_chain_block.get_top(),
                block.get_bottom(),
                color=YELLOW,
                stroke_width=4
            )
            connecting_lines.append(line)
            main_blockchain_blocks.append(block)
            main_blockchain.add(block, line)

        scene.play(*[Create(line) for line in connecting_lines])
        scene.wait(1)

    @staticmethod
    def animate_block_propagation(scene: Scene, propagations: list[tuple[int, list[int]]], nodes, node_blocks):
        """
        Animates blocks propagating simultaneously from multiple source nodes.
        If a node is a recipient from multiple sources, the last one in the
        propagations list "wins", and the other blocks are removed.

        Args:
            propagations (list[tuple[int, list[int]]]): A list of tuples, where each
                tuple contains a source node index and a list of recipient node indices.
        """
        animations = []
        blocks_to_fade_out = VGroup()
        
        # This dictionary will track which source block a recipient node receives.
        # The last source to send to a recipient "wins".
        recipient_to_source_block = {}

        for source_node_index, recipient_indices in propagations:
            source_block = node_blocks[source_node_index]
            for recipient_node_index in recipient_indices:
                # If this recipient was already targeted, the previous block is discarded
                if recipient_node_index in recipient_to_source_block:
                    blocks_to_fade_out.add(recipient_to_source_block[recipient_node_index]['block'])
                
                # Create a copy of the source block to animate
                block_copy = source_block.copy()
                recipient_to_source_block[recipient_node_index] = {'block': block_copy, 'source_index': source_node_index}

        # Now, create the animations for the "winning" blocks
        old_blocks_to_fade = VGroup()
        for recipient_node_index, data in recipient_to_source_block.items():
            block_copy = data['block']
            old_block = node_blocks[recipient_node_index]
            
            animations.append(block_copy.animate.move_to(old_block.get_center()))
            old_blocks_to_fade.add(old_block)
            
        # Run animations
        if animations:
            scene.play(*animations, run_time=0.75)
        if blocks_to_fade_out:
            scene.play(FadeOut(blocks_to_fade_out), run_time=0.5)

        # Update the node_blocks list with the new blocks
        if old_blocks_to_fade:
            scene.play(FadeOut(old_blocks_to_fade), run_time=0.25)
            for recipient_node_index, data in recipient_to_source_block.items():
                node_blocks.submobjects[recipient_node_index] = data['block']

        scene.wait(1)

