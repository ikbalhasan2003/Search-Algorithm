# -*- coding: utf-8 -*-
"""
Experiment 1 - Tree layout: where to draw each node on the canvas.
Pure Python (no Tkinter), so it can be tested.

Idea:
  1. Build a spanning tree with BFS from the root (the first parent that finds a node wins).
  2. y = the depth level, evenly spaced from top to bottom.
  3. x = leaves get evenly spaced slots from left to right,
         and each parent sits in the middle of its first and last child.
  4. Nodes the root cannot reach go on an extra row at the bottom.
  5. Edges that are not in the spanning tree (cycles, cross links) are returned
     as "extra edges", so the GUI can draw them dashed.
"""
from collections import deque


def all_nodes(neighbor):
    """Every node name (parents and children), in the order it is first seen."""
    names = []
    for parent, children in neighbor.items():
        for name in [parent] + list(children):
            if name not in names:
                names.append(name)
    return names


def spanning_tree(neighbor, root):
    """BFS from root. Returns {node: [tree children]} for every node the root can reach."""
    tree = {root: []}
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for child in neighbor.get(node, []):
            if child not in tree:          # first parent wins
                tree[child] = []
                tree[node].append(child)
                queue.append(child)
    return tree


def _depths(tree, root):
    depth = {root: 0}
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for child in tree[node]:
            depth[child] = depth[node] + 1
            queue.append(child)
    return depth


def _leaves_left_to_right(tree, root):
    """Leaves in drawing order (a depth-first walk keeps the children order)."""
    leaves = []
    stack = [root]
    while stack:
        node = stack.pop()
        if not tree[node]:
            leaves.append(node)
        stack.extend(reversed(tree[node]))   # reversed, so the first child is handled first
    return leaves


def _parent_x(tree, node, x):
    """Fill x[node] for inner nodes: the middle of the first and last child."""
    if node not in x:
        # Every child needs its x (not only the first and last: a middle child
        # can have its own children too)
        child_xs = [_parent_x(tree, child, x) for child in tree[node]]
        x[node] = (child_xs[0] + child_xs[-1]) / 2
    return x[node]


def _spread(count, start, end):
    """count positions evenly spread between start and end (centered slots)."""
    if count == 0:
        return []
    step = (end - start) / count
    return [start + (i + 0.5) * step for i in range(count)]


def compute_layout(neighbor, root, width, height, margin=50):
    """Return (positions, extra_edges).
    positions   = {node: (x, y)} in canvas pixels
    extra_edges = [(parent, child), ...] edges that are not in the spanning tree
    """
    tree = spanning_tree(neighbor, root)
    depth = _depths(tree, root)
    unreachable = [n for n in all_nodes(neighbor) if n not in tree]

    # x for the tree: leaves first, then parents from their children
    leaves = _leaves_left_to_right(tree, root)
    x = dict(zip(leaves, _spread(len(leaves), margin, width - margin)))
    _parent_x(tree, root, x)
    # Unreachable nodes: their own evenly spaced row
    x.update(zip(unreachable, _spread(len(unreachable), margin, width - margin)))

    # y: one row per depth level (+1 row for unreachable nodes)
    rows = max(depth.values()) + 1 + (1 if unreachable else 0)
    if rows == 1:
        row_y = [height / 2]
    else:
        gap = (height - 2 * margin) / (rows - 1)
        row_y = [margin + level * gap for level in range(rows)]
    level = dict(depth)
    for node in unreachable:
        level[node] = rows - 1

    positions = {node: (x[node], row_y[level[node]]) for node in all_nodes(neighbor)}

    tree_edges = {(parent, child) for parent, children in tree.items() for child in children}
    extra_edges = [(parent, child)
                   for parent, children in neighbor.items()
                   for child in children
                   if (parent, child) not in tree_edges]
    return positions, extra_edges
