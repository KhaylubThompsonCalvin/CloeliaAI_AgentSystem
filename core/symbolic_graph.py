# ---------------------------------------------------------------
# Module: symbolic_graph.py
# Location: core/
# Purpose: Defines Metatron’s Cube-based logic engine using
#          NetworkX. Nodes = emotions, virtues, and symbolic traits.
# ---------------------------------------------------------------

import networkx as nx


class MetatronGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self._build_base_cube()

    def _build_base_cube(self):
        # Nodes: 6 emotions + center + 6 virtues (as a starting set)
        emotions = [
            'anger',
            'fear',
            'disgust',
            'sadness',
            'surprise',
            'happiness']
        virtues = [
            'patience',
            'courage',
            'empathy',
            'resilience',
            'focus',
            'compassion']

        # Add nodes
        for e in emotions:
            self.graph.add_node(e, type='emotion')

        for v in virtues:
            self.graph.add_node(v, type='virtue')

        # Add symbolic edges (Metatron’s Cube style)
        edges = [
            ('anger', 'patience'),
            ('fear', 'courage'),
            ('disgust', 'empathy'),
            ('sadness', 'resilience'),
            ('surprise', 'focus'),
            ('happiness', 'compassion'),

            # Inner cube: virtues connected to each other
            ('patience', 'resilience'),
            ('courage', 'focus'),
            ('empathy', 'compassion'),
        ]
        self.graph.add_edges_from(edges)

    def get_virtue_for_emotion(self, emotion):
        connected = list(self.graph.neighbors(emotion))
        return [n for n in connected if self.graph.nodes[n]['type'] == 'virtue']

    def get_path(self, from_node, to_node):
        try:
            return nx.shortest_path(
                self.graph, source=from_node, target=to_node)
        except nx.NetworkXNoPath:
            return []

    def visualize(self):
        import matplotlib.pyplot as plt
        color_map = ['red' if self.graph.nodes[n]['type'] ==
                     'emotion' else 'blue' for n in self.graph.nodes]
        nx.draw(self.graph, with_labels=True, node_color=color_map)
        plt.show()
