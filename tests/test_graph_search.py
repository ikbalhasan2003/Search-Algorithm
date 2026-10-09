# -*- coding: utf-8 -*-
"""
Tests for code/graph_search.py (Graph, BFS, DFS).
Run from the project folder:
    D:\\anaconda3\\python.exe -m unittest discover -s tests -v
"""
import contextlib
import io
import os
import sys
import unittest

# The code lives in code/, not in a package, so add that folder to the import path.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "code"))

from graph_search import Graph  # noqa: E402


def make_teacher_tree():
    """The tree from the slides: A -> B, C   B -> D, E   C -> F"""
    g = Graph()
    g.add_node(("A", ["B", "C"]))
    g.add_node(("B", ["D", "E"]))
    g.add_node(("C", ["F"]))
    return g


def make_cycle_graph():
    """A -> B, C   B -> D, A   C -> D   D -> A  (A and D can be reached twice)"""
    g = Graph()
    g.add_node(("A", ["B", "C"]))
    g.add_node(("B", ["D", "A"]))
    g.add_node(("C", ["D"]))
    g.add_node(("D", ["A"]))
    return g


def run_quietly(func, *args):
    """Call func(*args), hide what it prints, and return (result, printed text)."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        result = func(*args)
    return result, buffer.getvalue()


class TestTeacherTree(unittest.TestCase):
    def test_bfs_order(self):
        g = make_teacher_tree()
        self.assertEqual(g.BFS("A"), ["A", "B", "C", "D", "E", "F"])

    def test_dfs_order(self):
        g = make_teacher_tree()
        self.assertEqual(g.DFS("A"), ["A", "B", "D", "E", "C", "F"])

    def test_bfs_fills_self_order(self):
        g = make_teacher_tree()
        g.BFS("A")
        self.assertEqual(g.order, ["A", "B", "C", "D", "E", "F"])

    def test_returned_list_is_a_copy(self):
        g = make_teacher_tree()
        result = g.BFS("A")
        result.append("X")
        self.assertNotIn("X", g.order)

    def test_start_from_inner_node(self):
        g = make_teacher_tree()
        self.assertEqual(g.BFS("B"), ["B", "D", "E"])

    def test_start_from_leaf(self):
        # D has no children, but it is still a node of the graph.
        g = make_teacher_tree()
        self.assertEqual(g.DFS("D"), ["D"])


class TestDfsDoesNotChangeGraph(unittest.TestCase):
    def test_dfs_twice_gives_same_result(self):
        g = make_teacher_tree()
        g.DFS("A")
        g.clear()
        g.DFS("A")
        self.assertEqual(g.order, ["A", "B", "D", "E", "C", "F"])

    def test_bfs_after_dfs_still_correct(self):
        # The teacher's tmp.reverse() flipped the stored lists, so BFS after DFS went wrong.
        g = make_teacher_tree()
        g.DFS("A")
        g.clear()
        g.BFS("A")
        self.assertEqual(g.order, ["A", "B", "C", "D", "E", "F"])

    def test_neighbor_lists_unchanged_after_dfs(self):
        g = make_teacher_tree()
        g.DFS("A")
        self.assertEqual(g.neighbor, {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"]})


class TestCycle(unittest.TestCase):
    def test_bfs_visits_each_node_once(self):
        g = make_cycle_graph()
        self.assertEqual(g.BFS("A"), ["A", "B", "C", "D"])

    def test_dfs_visits_each_node_once(self):
        g = make_cycle_graph()
        self.assertEqual(g.DFS("A"), ["A", "B", "D", "C"])


class TestAddNode(unittest.TestCase):
    def test_non_list_value_is_rejected(self):
        g = Graph()
        _, printed = run_quietly(g.add_node, ("A", "B"))
        self.assertNotIn("A", g.neighbor)
        self.assertIn("list", printed)

    def test_list_value_is_stored(self):
        g = Graph()
        g.add_node(("A", ["B"]))
        self.assertEqual(g.neighbor, {"A": ["B"]})


class TestBadRoot(unittest.TestCase):
    def test_none_root_bfs(self):
        g = make_teacher_tree()
        result, printed = run_quietly(g.BFS, None)
        self.assertEqual(result, [])
        self.assertIn("None", printed)

    def test_none_root_dfs(self):
        g = make_teacher_tree()
        result, printed = run_quietly(g.DFS, None)
        self.assertEqual(result, [])
        self.assertIn("None", printed)

    def test_unknown_root_bfs(self):
        g = make_teacher_tree()
        result, printed = run_quietly(g.BFS, "Z")
        self.assertEqual(result, [])
        self.assertIn("Z", printed)

    def test_unknown_root_dfs(self):
        g = make_teacher_tree()
        result, printed = run_quietly(g.DFS, "Z")
        self.assertEqual(result, [])
        self.assertIn("Z", printed)


class TestSteps(unittest.TestCase):
    def test_bfs_one_step_per_visit_plus_start(self):
        g = make_teacher_tree()
        g.BFS("A")
        self.assertEqual(len(g.steps), len(g.order) + 1)

    def test_dfs_one_step_per_visit_plus_start_with_cycle(self):
        g = make_cycle_graph()
        g.DFS("A")
        self.assertEqual(len(g.steps), len(g.order) + 1)

    def test_start_step(self):
        g = make_teacher_tree()
        g.BFS("A")
        start = g.steps[0]
        self.assertEqual(start["step"], 0)
        self.assertEqual(start["frontier"], ["A"])
        self.assertEqual(start["order"], [])

    def test_bfs_steps_match_trace_table(self):
        # Same rows as the BFS table in diagrams/theory_notes.md
        g = make_teacher_tree()
        g.BFS("A")
        frontiers = [s["frontier"] for s in g.steps]
        self.assertEqual(frontiers, [
            ["A"], ["B", "C"], ["C", "D", "E"], ["D", "E", "F"], ["E", "F"], ["F"], [],
        ])
        self.assertEqual(g.steps[2]["current"], "B")
        self.assertEqual(g.steps[2]["added"], ["D", "E"])
        self.assertEqual(g.steps[2]["order"], ["A", "B"])

    def test_dfs_steps_match_trace_table(self):
        # Same rows as the DFS table in diagrams/theory_notes.md (top of stack first)
        g = make_teacher_tree()
        g.DFS("A")
        frontiers = [s["frontier"] for s in g.steps]
        self.assertEqual(frontiers, [
            ["A"], ["B", "C"], ["D", "E", "C"], ["E", "C"], ["C"], ["F"], [],
        ])
        self.assertEqual(g.steps[1]["added"], ["B", "C"])
        self.assertEqual(g.steps[3]["added"], [])

    def test_visited_grows_each_step(self):
        g = make_teacher_tree()
        g.BFS("A")
        self.assertEqual(g.steps[-1]["visited"], ["A", "B", "C", "D", "E", "F"])


class TestHelpers(unittest.TestCase):
    def test_clear_resets_order_and_steps(self):
        g = make_teacher_tree()
        g.BFS("A")
        g.clear()
        self.assertEqual(g.order, [])
        self.assertEqual(g.steps, [])

    def test_node_print(self):
        g = make_teacher_tree()
        g.BFS("A")
        _, printed = run_quietly(g.node_print)
        self.assertEqual(printed.split(), ["A", "B", "C", "D", "E", "F"])

    def test_nodes_in_first_seen_order(self):
        g = make_teacher_tree()
        self.assertEqual(g.nodes(), ["A", "B", "C", "D", "E", "F"])


if __name__ == "__main__":
    unittest.main()
