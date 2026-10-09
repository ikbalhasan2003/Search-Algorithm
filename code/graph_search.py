# -*- coding: utf-8 -*-
r"""
Experiment 1 - Part 2: Graph dataset + BFS + DFS
Based on the teacher's code (Search Algortihm.pptx, slides 14-16), with fixes.

Tree used:
          A
         / \
        B   C
       / \   \
      D   E   F
Expected output:
    BFS: A B C D E F
    DFS: A B D E C F

Run:  D:\anaconda3\python.exe code\graph_search.py
"""
from collections import deque  # double-ended queue: works as a queue (BFS) or a stack (DFS)


# ---------- 1. Graph class (adjacency list) ----------
class Graph(object):
    def __init__(self, *args, **kwargs):
        self.order = []      # visited order
        self.neighbor = {}   # node -> list of its children
        self.steps = []      # one snapshot per step, so the GUI can replay the search

    def add_node(self, node):
        """node = (key, [children]), for example ('A', ['B', 'C'])"""
        key, val = node
        if not isinstance(val, list):
            print('Nodes should be entered as a list, e.g. (\'A\', [\'B\', \'C\'])')
            # FIX: the teacher's code printed the error but still stored the bad value.
            return
        self.neighbor[key] = val

    def nodes(self):
        """All node names (parents and children), in the order they were first seen."""
        names = []
        for key, children in self.neighbor.items():
            for name in [key] + children:
                if name not in names:
                    names.append(name)
        return names

    # ---------- 2. BFS ----------
    def BFS(self, root):
        # First check whether the root node is valid
        if not self._root_ok(root):
            return []

        search_queue = deque()
        search_queue.append(root)
        visited = []
        self._save_step(None, [], search_queue, visited)

        while search_queue:
            person = search_queue.popleft()          # take from the FRONT (FIFO)
            # FIX: in a graph with a cycle, a node can be in the queue twice.
            # The teacher's code added it to the order again; now we skip it.
            if person in visited:
                continue
            self.order.append(person)
            visited.append(person)                   # FIX: mark leaves visited too

            children = self.neighbor.get(person, [])
            search_queue += children                 # add children to the BACK
            self._save_step(person, children, search_queue, visited)

        return list(self.order)

    # ---------- 3. DFS ----------
    def DFS(self, root):
        # First check whether the root node is valid
        if not self._root_ok(root):
            return []

        search_queue = deque()                       # used as a stack: the left end is the top
        search_queue.append(root)
        visited = []
        self._save_step(None, [], search_queue, visited)

        while search_queue:
            person = search_queue.popleft()          # take from the TOP (LIFO)
            # FIX: skip a node that was already visited (graphs with cycles).
            if person in visited:
                continue
            self.order.append(person)
            visited.append(person)

            children = self.neighbor.get(person, [])
            # FIX: the teacher's tmp.reverse() reversed the stored list itself,
            # so the next search used the wrong order. reversed() makes a reversed copy.
            # Reverse + push to the front = the leftmost child ends up on top.
            for index in reversed(children):
                search_queue.appendleft(index)
            self._save_step(person, children, search_queue, visited)

        return list(self.order)

    # ---------- 4. Helpers ----------
    def clear(self):
        self.order = []
        self.steps = []

    def node_print(self):
        for index in self.order:
            print(index, end='  ')

    def _root_ok(self, root):
        """Print a message and return False if the search cannot start from root."""
        if root is None:
            print('root is None')
            return False
        # FIX: the teacher's code did not check this. Now an unknown root gives an empty result.
        if root not in self.nodes():
            print('root', root, 'is not in the graph')
            return False
        return True

    def _save_step(self, current, added, frontier, visited):
        """Save a snapshot of the search. steps[0] is the start state."""
        self.steps.append({
            "step": len(self.steps),
            "current": current,           # node taken out in this step (None at the start)
            "added": list(added),         # children pushed in this step
            "frontier": list(frontier),   # queue (front -> back) or stack (top -> bottom)
            "order": list(self.order),
            "visited": list(visited),
        })


# ---------- 5. Main ----------
if __name__ == '__main__':
    # Create a tree
    g = Graph()
    g.add_node(('A', ['B', 'C']))
    g.add_node(('B', ['D', 'E']))
    g.add_node(('C', ['F']))

    # Breadth-first search
    g.BFS('A')
    print('BFS:', ' '.join(g.order))
    g.clear()

    # Depth-first search
    g.DFS('A')
    print('DFS:', ' '.join(g.order))
