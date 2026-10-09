# -*- coding: utf-8 -*-
"""
Tests for parse_graph_text() and graph_to_text() in code/sample_graphs.py.
Run from the project folder:
    D:\\anaconda3\\python.exe -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "code"))

from sample_graphs import (CUSTOM_EXAMPLE, PRESETS, graph_to_text,  # noqa: E402
                           parse_graph_text)


class TestParseValid(unittest.TestCase):
    def test_simple_graph(self):
        self.assertEqual(parse_graph_text("A: B C\nB: D E\nC: F"),
                         {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"]})

    def test_comments_and_blank_lines_ignored(self):
        text = "# my tree\n\nA: B C\n   \n# leaves below\nB: D\n"
        self.assertEqual(parse_graph_text(text), {"A": ["B", "C"], "B": ["D"]})

    def test_commas_and_spaces(self):
        self.assertEqual(parse_graph_text("A: B, C,D"), {"A": ["B", "C", "D"]})

    def test_parent_without_children(self):
        self.assertEqual(parse_graph_text("A: B\nB:"), {"A": ["B"], "B": []})

    def test_names_with_digits_and_underscore(self):
        self.assertEqual(parse_graph_text("WUH: S_1 42"), {"WUH": ["S_1", "42"]})

    def test_custom_example_is_valid(self):
        adjacency = parse_graph_text(CUSTOM_EXAMPLE)
        self.assertIn("WUH", adjacency)


class TestParseErrors(unittest.TestCase):
    def assert_error(self, text, *words):
        with self.assertRaises(ValueError) as caught:
            parse_graph_text(text)
        for word in words:
            self.assertIn(word, str(caught.exception))

    def test_missing_colon(self):
        self.assert_error("A: B\nB: C\nC D", "Line 3", "':'")

    def test_two_colons(self):
        self.assert_error("A: B: C", "Line 1", "':'")

    def test_bad_name(self):
        self.assert_error("A: B-1", "Line 1", "B-1")

    def test_name_too_long(self):
        self.assert_error("A: LONG", "Line 1", "LONG", "3")

    def test_empty_parent_name(self):
        self.assert_error(": B", "Line 1")

    def test_duplicate_parent(self):
        self.assert_error("A: B\nB: C\nA: D", "Line 3", "A", "twice")

    def test_node_is_its_own_child(self):
        self.assert_error("A: A", "Line 1")

    def test_child_listed_twice(self):
        self.assert_error("A: B B", "Line 1", "B")

    def test_too_many_nodes(self):
        names = [f"N{i}" for i in range(31)]          # 31 nodes
        self.assert_error("N0: " + " ".join(names[1:]), "30")

    def test_thirty_nodes_is_ok(self):
        names = [f"N{i}" for i in range(30)]
        self.assertEqual(len(parse_graph_text("N0: " + " ".join(names[1:]))["N0"]), 29)

    def test_empty_graph(self):
        self.assert_error("", "empty")
        self.assert_error("# only a comment\n\n", "empty")


class TestRoundTrip(unittest.TestCase):
    def test_graph_to_text_format(self):
        self.assertEqual(graph_to_text({"A": ["B", "C"], "B": []}), "A: B C\nB:")

    def test_every_preset_round_trips(self):
        for name, adjacency in PRESETS.items():
            self.assertEqual(parse_graph_text(graph_to_text(adjacency)), adjacency, name)


if __name__ == "__main__":
    unittest.main()
