# BFS vs DFS — Comparison With Real Numbers (Step 11)

Made by `code/compare.py` (do not edit by hand, run the script again).
Start node = the first node of each graph.

## Table 1: Measured results

| Graph | Algo | Nodes | Steps | Max queue/stack | Find deep right | Find deep left | Find level-1 right | Visit order |
|---|---|---|---|---|---|---|---|---|
| Teacher tree (6 nodes) | BFS | 6 | 6 | 3 | F: 6 | D: 4 | C: 3 | A B C D E F |
| Teacher tree (6 nodes) | DFS | 6 | 6 | 3 | F: 6 | D: 3 | C: 5 | A B D E C F |
| Bigger tree (15 nodes) | BFS | 15 | 15 | 8 | O: 15 | H: 8 | C: 3 | A B C D E F G H I J K L M N O |
| Bigger tree (15 nodes) | DFS | 15 | 15 | 4 | O: 15 | H: 4 | C: 9 | A B D H I E J K C F L M G N O |
| Unbalanced tree | BFS | 8 | 8 | 3 | H: 8 | H: 8 | D: 4 | A B C D E F G H |
| Unbalanced tree | DFS | 8 | 8 | 3 | H: 8 | H: 8 | D: 5 | A B E C D F G H |
| Graph with cycle | BFS | 6 | 6 | 4 | F: 6 | F: 6 | C: 3 | A B C D E F |
| Graph with cycle | DFS | 6 | 6 | 3 | F: 4 | F: 4 | C: 5 | A B D F C E |
| Custom graph (city map) | BFS | 9 | 9 | 5 | SZX: 9 | TSN: 5 | CAN: 4 | WUH PEK SHA CAN TSN SHE NKG HGH SZX |
| Custom graph (city map) | DFS | 9 | 9 | 4 | SZX: 9 | TSN: 3 | CAN: 8 | WUH PEK TSN SHE SHA NKG HGH CAN SZX |

- **Steps** = nodes taken out of the queue/stack and visited.
- **Max queue/stack** = the most nodes waiting at one time (memory use). With a cycle, a node can wait twice, so it is counted twice.
- **Find ...** = `node: k` means the node is found at visit number k (smaller = found sooner).
  - *deep right* = deepest node, right-most;  *deep left* = deepest node, left-most;
  - *level-1 right* = right-most child of the start node.

## Table 2: General comparison

| Point | BFS | DFS |
|---|---|---|
| Data structure | Queue (FIFO) | Stack (LIFO) |
| Search style | Level by level | Branch by branch, then backtrack |
| Memory use | High (a whole level) | Low (one path + waiting siblings) |
| Shortest path (unweighted)? | Yes | Not always |
| Time complexity | O(V + E) | O(V + E) |
| Good for | Shortest path, nearby nodes | Deep goals, mazes, low memory |

## Trace table check (diagrams/theory_notes.md vs graph.steps)

- BFS trace table: **matches the code**
- DFS trace table: **matches the code**
- Self-check Q2 (add D -> G): BFS = A B C D E F G, DFS = A B D G E C F -> **matches the notes**
