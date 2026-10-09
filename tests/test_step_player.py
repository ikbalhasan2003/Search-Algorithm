# -*- coding: utf-8 -*-
"""
Tests for code/step_player.py.
Run from the project folder:
    D:\\anaconda3\\python.exe -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "code"))

from sample_graphs import PRESETS, build_graph  # noqa: E402
from step_player import StepPlayer, discovery_parents  # noqa: E402


def run_search(preset, algorithm, start="A"):
    g = build_graph(PRESETS[preset])
    g.BFS(start) if algorithm == "BFS" else g.DFS(start)
    return g.steps


class TestStepPlayer(unittest.TestCase):
    def setUp(self):
        self.player = StepPlayer(run_search("Teacher tree (6 nodes)", "BFS"))

    def test_starts_at_step_0(self):
        self.assertEqual(self.player.index, 0)
        self.assertEqual(self.player.current()["step"], 0)
        self.assertEqual(self.player.current()["frontier"], ["A"])

    def test_total(self):
        self.assertEqual(self.player.total, 7)   # start + 6 visits

    def test_next_moves_forward(self):
        self.assertTrue(self.player.next())
        self.assertEqual(self.player.index, 1)
        self.assertEqual(self.player.current()["current"], "A")

    def test_stops_at_the_end(self):
        while self.player.next():
            pass
        self.assertTrue(self.player.is_done())
        self.assertEqual(self.player.index, 6)
        self.assertFalse(self.player.next())     # stays on the last step
        self.assertEqual(self.player.index, 6)
        self.assertEqual(self.player.current()["order"], list("ABCDEF"))

    def test_reset_goes_back_to_0(self):
        self.player.next()
        self.player.next()
        self.player.reset()
        self.assertEqual(self.player.index, 0)
        self.assertFalse(self.player.is_done())

    def test_empty_steps_are_safe(self):
        player = StepPlayer([])
        self.assertEqual(player.total, 0)
        self.assertIsNone(player.current())
        self.assertFalse(player.next())
        self.assertTrue(player.is_done())
        player.reset()
        self.assertEqual(player.index, 0)

    def test_steps_list_is_copied(self):
        steps = run_search("Teacher tree (6 nodes)", "BFS")
        player = StepPlayer(steps)
        steps.clear()
        self.assertEqual(player.total, 7)


class TestDiscoveryParents(unittest.TestCase):
    def test_teacher_tree(self):
        parents = discovery_parents(run_search("Teacher tree (6 nodes)", "DFS"), "DFS")
        self.assertEqual(parents, {"A": None, "B": "A", "C": "A", "D": "B", "E": "B", "F": "C"})

    def test_cycle_bfs_first_push_wins(self):
        # BFS: D is put in the queue by B first, so B is the parent (FIFO)
        parents = discovery_parents(run_search("Graph with cycle", "BFS"), "BFS")
        self.assertEqual(parents["D"], "B")

    def test_cycle_dfs(self):
        # DFS from A visits A B D F C E; D is reached from B
        parents = discovery_parents(run_search("Graph with cycle", "DFS"), "DFS")
        self.assertEqual(parents, {"A": None, "B": "A", "D": "B", "F": "D", "C": "A", "E": "C"})

    def test_dfs_last_push_wins(self):
        # A: B C, B: C.  DFS pushes C twice; the copy on top (from B) is taken first.
        g = build_graph({"A": ["B", "C"], "B": ["C"]})
        g.DFS("A")
        self.assertEqual(discovery_parents(g.steps, "DFS")["C"], "B")


if __name__ == "__main__":
    unittest.main()
