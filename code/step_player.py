# -*- coding: utf-8 -*-
"""
Experiment 1 - StepPlayer: walks through the saved search steps one by one.
Pure Python (no Tkinter), so it can be tested. The GUI asks it for the current step
and draws that step.

A step is one dict from Graph.steps (see graph_search.py):
    {"step", "current", "added", "frontier", "order", "visited"}
"""


class StepPlayer:
    def __init__(self, steps):
        self.steps = list(steps)   # a copy: the graph may be cleared later
        self.index = 0

    @property
    def total(self):
        return len(self.steps)

    def current(self):
        """The step dict at the current index, or None if there are no steps."""
        return self.steps[self.index] if self.steps else None

    def next(self):
        """Move one step forward. Returns False (and stays) if already at the end."""
        if self.is_done():
            return False
        self.index += 1
        return True

    def reset(self):
        self.index = 0

    def is_done(self):
        return self.index >= self.total - 1


def discovery_parents(steps, algorithm):
    """Which node put each visited node into the queue/stack: {node: parent}.
    The GUI highlights the edge parent -> node when node is visited.

    A node can be pushed more than once (graphs with cycles). The copy that is
    taken out first decides the parent:
      BFS (queue, FIFO): the FIRST push is nearest the front.
      DFS (stack, LIFO): the LAST push is nearest the top.
    """
    if not steps:
        return {}
    root = steps[0]["frontier"][0]
    pushed_by = {root: None}
    parents = {}
    for step in steps[1:]:
        node = step["current"]
        parents[node] = pushed_by[node]          # taken out now: remember who pushed it
        for child in step["added"]:
            if algorithm == "DFS" or child not in pushed_by:
                pushed_by[child] = node
    return parents
