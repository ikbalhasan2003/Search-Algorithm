# -*- coding: utf-8 -*-
"""
Tests for code/tree_layout.py and code/sample_graphs.py.
Run from the project folder:
    D:\\anaconda3\\python.exe -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "code"))

from sample_graphs import PRESETS, build_graph  # noqa: E402
from tree_layout import compute_layout, spanning_tree  # noqa: E402

WIDTH, HEIGHT, MARGIN = 800, 600, 50
TEACHER = PRESETS["Teacher tree (6 nodes)"]
CYCLE = PRESETS["Graph with cycle"]


def layout(adjacency, root="A"):
    return compute_layout(adjacency, root, WIDTH, HEIGHT, margin=MARGIN)


class TestPresets(unittest.TestCase):
    def test_four_presets(self):
        self.assertEqual(len(PRESETS), 4)

    def test_preset_node_counts(self):
        counts = {name: len(build_graph(adj).nodes()) for name, adj in PRESETS.items()}
        self.assertEqual(counts["Teacher tree (6 nodes)"], 6)
        self.assertEqual(counts["Bigger tree (15 nodes)"], 15)
        self.assertEqual(counts["Unbalanced tree"], 8)
        self.assertEqual(counts["Graph with cycle"], 6)

    def test_build_graph_copies_lists(self):
        g = build_graph(TEACHER)
        g.neighbor["A"].append("Z")
        self.assertEqual(TEACHER["A"], ["B", "C"])

    def test_teacher_tree_search_orders(self):
        g = build_graph(TEACHER)
        self.assertEqual(g.BFS("A"), list("ABCDEF"))
        g.clear()
        self.assertEqual(g.DFS("A"), list("ABDECF"))


class TestLayout(unittest.TestCase):
    def test_every_node_gets_a_position(self):
        for name, adjacency in PRESETS.items():
            positions, _ = layout(adjacency)
            self.assertEqual(set(positions), set(build_graph(adjacency).nodes()), name)

    def test_positions_inside_canvas(self):
        for name, adjacency in PRESETS.items():
            positions, _ = layout(adjacency)
            for node, (x, y) in positions.items():
                self.assertTrue(MARGIN <= x <= WIDTH - MARGIN, (name, node, x))
                self.assertTrue(MARGIN <= y <= HEIGHT - MARGIN, (name, node, y))

    def test_parent_above_child(self):
        for name, adjacency in PRESETS.items():
            positions, _ = layout(adjacency)
            for parent, children in spanning_tree(adjacency, "A").items():
                for child in children:
                    self.assertLess(positions[parent][1], positions[child][1], (name, child))

    def test_parent_between_first_and_last_child(self):
        for name, adjacency in PRESETS.items():
            positions, _ = layout(adjacency)
            for parent, children in spanning_tree(adjacency, "A").items():
                if children:
                    xs = [positions[c][0] for c in (children[0], children[-1])]
                    self.assertTrue(min(xs) <= positions[parent][0] <= max(xs), (name, parent))

    def test_teacher_root_centered_over_children(self):
        positions, _ = layout(TEACHER)
        middle = (positions["B"][0] + positions["C"][0]) / 2
        self.assertAlmostEqual(positions["A"][0], middle)

    def test_no_two_nodes_on_same_spot(self):
        for name, adjacency in PRESETS.items():
            positions, _ = layout(adjacency)
            spots = [(round(x), round(y)) for x, y in positions.values()]
            self.assertEqual(len(spots), len(set(spots)), name)

    def test_tree_has_no_extra_edges(self):
        _, extra = layout(TEACHER)
        self.assertEqual(extra, [])

    def test_cycle_graph_extra_edges(self):
        # BFS from A: B and C are found by A, D by B, E by C, F by D.
        # So C->D and D->A are the edges outside the spanning tree.
        _, extra = layout(CYCLE)
        self.assertEqual(extra, [("C", "D"), ("D", "A")])

    def test_unreachable_nodes_go_to_bottom_row(self):
        # Start from B: A, C, F cannot be reached, so they go on an extra bottom row.
        positions, _ = layout(TEACHER, root="B")
        bottom = max(y for _, y in positions.values())
        for node in ("A", "C", "F"):
            self.assertEqual(positions[node][1], bottom)
        self.assertLess(positions["D"][1], bottom)

    def test_middle_child_with_children(self):
        # B is neither the first nor the last child of A, but has its own children
        adjacency = {"A": ["X", "B", "Y"], "B": ["C", "D"]}
        positions, _ = compute_layout(adjacency, "A", WIDTH, HEIGHT)
        self.assertAlmostEqual(positions["B"][0], (positions["C"][0] + positions["D"][0]) / 2)

    def test_single_node(self):
        positions, extra = compute_layout({"A": []}, "A", WIDTH, HEIGHT)
        self.assertEqual(positions, {"A": (WIDTH / 2, HEIGHT / 2)})
        self.assertEqual(extra, [])


if __name__ == "__main__":
    unittest.main()
