# -*- coding: utf-8 -*-
r"""
Experiment 1 - Preset graphs for the GUI and for compare.py.

Each graph is an adjacency dict: parent -> list of children.
Python dicts keep insertion order, so the first key is the default start node.

Run (prints every preset):  D:\anaconda3\python.exe code\sample_graphs.py
"""
from graph_search import Graph

PRESETS = {
    # The tree from the teacher's slides
    "Teacher tree (6 nodes)": {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F"],
    },
    # Full binary tree with 4 levels: A on top, H..O are the leaves
    "Bigger tree (15 nodes)": {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["F", "G"],
        "D": ["H", "I"],
        "E": ["J", "K"],
        "F": ["L", "M"],
        "G": ["N", "O"],
    },
    # Branches of different depth: shows how DFS goes deep first
    "Unbalanced tree": {
        "A": ["B", "C", "D"],
        "B": ["E"],
        "D": ["F", "G"],
        "G": ["H"],
    },
    # D can be reached from B and from C, and D points back to A.
    # Without the visited check, the search would visit nodes twice.
    "Graph with cycle": {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D", "E"],
        "D": ["A", "F"],
    },
}


# Example for the "Edit graph..." dialog: a small map of Chinese cities (airport codes).
# The search starts in Wuhan. NKG -> HGH is a cross link, so the graph has a dashed edge.
CUSTOM_EXAMPLE = """\
# Small city map: one parent per line,  parent: children
WUH: PEK SHA CAN
PEK: TSN SHE
SHA: NKG HGH
CAN: SZX
NKG: HGH
"""

MAX_NODES = 30        # more nodes do not fit on the canvas
MAX_NAME_LENGTH = 3   # longer names do not fit inside a node circle


def _check_name(name, line_number):
    if not name:
        raise ValueError(f"Line {line_number}: a node name is missing")
    if not all(ch.isascii() and (ch.isalnum() or ch == "_") for ch in name):
        raise ValueError(f"Line {line_number}: bad name '{name}' "
                         "(use letters, digits, or _ only)")
    if len(name) > MAX_NAME_LENGTH:
        raise ValueError(f"Line {line_number}: name '{name}' is too long "
                         f"(at most {MAX_NAME_LENGTH} characters)")


def parse_graph_text(text):
    """Turn text like "A: B C" (one parent per line) into an adjacency dict.
    Children may be separated by spaces or commas. Blank lines and # comments are ignored.
    Raises ValueError with the line number if the text is wrong.
    """
    adjacency = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.count(":") != 1:
            raise ValueError(f"Line {line_number}: each line needs exactly one ':' "
                             "(example  A: B C)")
        parent, rest = (part.strip() for part in line.split(":"))
        _check_name(parent, line_number)
        if parent in adjacency:
            raise ValueError(f"Line {line_number}: parent '{parent}' is defined twice")

        children = rest.replace(",", " ").split()
        for child in children:
            _check_name(child, line_number)
        if parent in children:
            raise ValueError(f"Line {line_number}: '{parent}' cannot be its own child")
        if len(set(children)) != len(children):
            duplicate = next(c for c in children if children.count(c) > 1)
            raise ValueError(f"Line {line_number}: child '{duplicate}' is listed twice")
        adjacency[parent] = children

    if not adjacency:
        raise ValueError("The graph is empty: write at least one line like  A: B C")
    names = {name for parent, children in adjacency.items() for name in [parent] + children}
    if len(names) > MAX_NODES:
        raise ValueError(f"Too many nodes: {len(names)} (at most {MAX_NODES} fit on the screen)")
    return adjacency


def graph_to_text(adjacency):
    """The opposite of parse_graph_text: adjacency dict -> text for the editor."""
    return "\n".join(f"{parent}: {' '.join(children)}".rstrip()
                     for parent, children in adjacency.items())


def build_graph(adjacency):
    """Make a Graph object from an adjacency dict (uses add_node from graph_search.py)."""
    graph = Graph()
    for parent, children in adjacency.items():
        graph.add_node((parent, list(children)))   # list(...) = a copy, so presets stay safe
    return graph


if __name__ == "__main__":
    for name, adjacency in PRESETS.items():
        g = build_graph(adjacency)
        print(name)
        print("  nodes:", " ".join(g.nodes()))
        print("  BFS:  ", " ".join(g.BFS(g.nodes()[0])))
        g.clear()
        print("  DFS:  ", " ".join(g.DFS(g.nodes()[0])))
