# Theory Notes — BFS and DFS (Step 03)

Study notes for the **principles** part of the report.
Bullets and tables only. Write the report text **in your own words**.

Source: teacher slides `Docs/Search Algortihm.pptx` (slides 2–5 = DFS, 10–13 = BFS).

---

## 1. The Teacher's Tree

Input in the code (slide 8):

```
g.add_node(('A', ['B', 'C']))
g.add_node(('B', ['D', 'E']))
g.add_node(('C', ['F']))
```

Drawing:

```
Level 0            A
                 /   \
Level 1         B     C
               / \     \
Level 2       D   E     F
```

| Fact | Value |
|---|---|
| Root | A |
| Nodes (V) | 6 (A, B, C, D, E, F) |
| Edges (E) | 5 (A-B, A-C, B-D, B-E, C-F) |
| Leaves (no children) | D, E, F |
| Depth (levels below root) | 2 |
| Children order | always left to right (B before C, D before E) |

---

## 2. BFS Trace Table

How the teacher's `BFS` works (slide 9):

- Take a node from the **front** of the queue (`popleft`).
- Add it to the visit order.
- Add its children to the **back** of the queue (`search_queue += children`).

| Step | Node taken out | Children added | Queue after (front -> back) | Visit order so far |
|---|---|---|---|---|
| 0 | — (start) | — | [A] | — |
| 1 | A | B, C | [B, C] | A |
| 2 | B | D, E | [C, D, E] | A B |
| 3 | C | F | [D, E, F] | A B C |
| 4 | D | — (leaf) | [E, F] | A B C D |
| 5 | E | — (leaf) | [F] | A B C D E |
| 6 | F | — (leaf) | [] (empty -> stop) | A B C D E F |

**Final BFS order: A B C D E F** ✅ (matches expected)

Notice:
- Level 0 (A) -> level 1 (B, C) -> level 2 (D, E, F). One level is finished before the next starts.
- Biggest queue size = 3 (steps 2 and 3).

---

## 3. DFS Trace Table

How the teacher's `DFS` works (slide 13):

- It also uses a `deque`, but uses it as a **stack**.
- Take a node from the **left** (`popleft`) = the **top** of the stack.
- Add it to the visit order.
- Reverse the children, then push each one to the **left** (`appendleft`).
  - Example for A: children [B, C] -> reversed [C, B] -> push C, then push B -> stack [B, C].
  - Result: the **leftmost child ends up on top**, so it is visited next.

| Step | Node taken out | Children added | Stack after (top -> bottom) | Visit order so far |
|---|---|---|---|---|
| 0 | — (start) | — | [A] | — |
| 1 | A | B, C | [B, C] | A |
| 2 | B | D, E | [D, E, C] | A B |
| 3 | D | — (leaf) | [E, C] | A B D |
| 4 | E | — (leaf) | [C] | A B D E |
| 5 | C | F | [F] | A B D E C |
| 6 | F | — (leaf) | [] (empty -> stop) | A B D E C F |

**Final DFS order: A B D E C F** ✅ (matches expected)

Notice:
- After B, DFS goes **down** to D and E before it goes back up to C. This going back is called **backtracking**.
- C waits at the bottom of the stack from step 1 until step 5.
- Biggest stack size = 3 (step 2).

---

## 4. Key Points

### BFS (Breadth-First Search)

- **Data structure:** queue — FIFO (first in, first out).
- **Visit rule:** take from the front, add children to the back -> level by level, left to right.
- **Memory use:** high. The queue can hold a whole level of the tree at once.
- **Complete?** Yes — if a goal exists and each node has a finite number of children, BFS finds it.
- **Shortest path (optimal)?** Yes, in an **unweighted** graph (fewest edges). The first time BFS reaches a node, it is by the shortest path.
- **Time:** O(V + E) — each node is taken out once, each edge is looked at once.
- **Space:** O(V) in the worst case. For a tree with branching factor `b` and depth `d`: O(b^d) (the widest level).

### DFS (Depth-First Search)

- **Data structure:** stack — LIFO (last in, first out).
- **Visit rule:** take from the top, push children on top -> go deep along one branch, then backtrack.
- **Memory use:** low. The stack holds roughly one path plus the waiting siblings on that path.
- **Complete?** Yes on a **finite** graph with a visited check. No on an infinite (or very deep) branch — it can go down forever. Without a visited check, a cycle can make it loop.
- **Shortest path (optimal)?** No, not always. It returns the first path it finds, which may be long.
- **Time:** O(V + E) — same as BFS.
- **Space:** O(V) worst case. For a tree with branching factor `b` and max depth `m`: O(b·m) (this push-all-children version), or O(m) for the recursive version.

### Shared facts

- Both are **blind (uninformed) search**: no heuristic, no domain knowledge (slide 2).
- Both visit every node **once** on a tree, so both have 6 steps on the teacher's tree.
- The **only** code difference: where the children go — **back** of the deque (BFS) or **front** of the deque in reverse (DFS).

### Notes on the teacher's code (for Step 04)

- `tmp.reverse()` reverses the real `neighbor` list in place, so a second DFS run would use the wrong order. Use `reversed(...)` instead.
- The slide text has broken indentation (slide 13). Use the code images on slides 14–16.

---

## 5. BFS vs DFS

| Point | BFS | DFS |
|---|---|---|
| Visit order (teacher tree) | A B C D E F | A B D E C F |
| Data structure | Queue (FIFO) | Stack (LIFO) |
| Search style | Level by level | Branch by branch |
| Memory use | High (stores a whole level) | Low (stores one path) |
| Shortest path? | ✅ Yes (unweighted) | ❌ Not always |
| Time complexity | O(V + E) | O(V + E) |
| Good for | Shortest path, nearby nodes | Deep solutions, mazes, low memory |

---

## 6. Self-Check Questions

**Q1.** On the teacher's tree, BFS visits C before D, but DFS visits D before C. Why?

<details>
<summary>Answer</summary>

- BFS puts children at the **back** of the queue. C was added (step 1) before D (step 2), so C comes out first.
- DFS puts children on the **top** of the stack. D and E are pushed on top of C at step 2, so D comes out first.

</details>

**Q2.** Add a new node G as a child of D (`D -> G`). What are the new BFS and DFS orders?

<details>
<summary>Answer</summary>

- BFS: **A B C D E F G** — G is on level 3, so it comes last.
- DFS: **A B D G E C F** — DFS goes down to G right after D, then backtracks to E.

</details>

**Q3.** You want the path with the **fewest steps** from A to a goal node. Which search should you use, and why?

<details>
<summary>Answer</summary>

- **BFS.** It checks all nodes 1 step away, then all nodes 2 steps away, and so on.
- So the first time it reaches the goal, no shorter path can exist (in an unweighted graph).
- DFS may find a long path first, because it goes deep before it looks at nearby nodes.

</details>
