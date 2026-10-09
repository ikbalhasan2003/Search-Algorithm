# Experiment 1: Search Algorithm — Project Roadmap

**Course:** Introduction to Artificial Intelligence
**School:** Wuhan Institute of Technology, International College
**Lab hours:** 4
**Total work time (estimate):** about 15.5 hours (including the GUI)

---

## Project Overview

### Source files

| File | What it is |
|---|---|
| `Experiment1 Searching algorithm.docx` | The task and the report template (what you submit) |
| `Search Algortihm.pptx` | Teacher's slides on DFS and BFS, with Python code |
| `Numpy.pptx` | Teacher's slides on NumPy basics, with examples |

### Goal in one line

Set up Python, learn NumPy, build a small tree, and search it with **BFS** and **DFS**. Show it in a **Python GUI that animates the search**. Write it all up in the report template.

### Parts of the project

| Part | Phases | Required by teacher? |
|---|---|---|
| Environment + NumPy | 1–2 | ✅ Yes |
| Theory + search code | 3–4 | ✅ Yes |
| GUI: tree view + BFS/DFS animation | 5–9 | ⭐ Extra (your own idea, makes the report stronger) |
| Flow charts + comparison | 10–11 | ✅ Yes |
| Report + final check | 12–13 | ✅ Yes |

### GUI decisions

| Question | Decision |
|---|---|
| Type | Python GUI |
| Library | **Tkinter** (built into Python, no install needed) |
| What it does | Shows the tree and animates BFS/DFS step by step |
| Design method | Straight to code (the layout and colors are written in Step 05's prompt) |

### Grading

| Part | Points | What counts |
|---|---|---|
| Lab performance | 30 | Show up on time, follow the rules, finish all experiments |
| Report quality | 70 | Clean and correct code, complete content, shows what you learned |

> ⚠️ **Copying = 0 points.** You may discuss with classmates, but you must write your own report text.

---

## How to Use This Roadmap With the Prompts

Every phase (1–13) has its own prompt file in [`prompts/`](../prompts/README.md).

1. Open the prompt file for the next phase.
2. Copy the **PROMPT** box and send it to Claude Code.
3. Check the **Done when** list, then do **Your manual tasks**.
4. Tick the boxes here and move to the next phase.

The shared rules for all prompts are in [`prompts/README.md`](../prompts/README.md).

---

## Phase 0: Prepare (15 min) — ✅ Done

Folder structure (see `README.md` for the full tree):

```
New folder (2)/
├── README.md
├── Docs/                 (teacher files + this roadmap)
├── prompts/              (one prompt per phase)
├── code/                 (all Python files)
├── tests/                (unit tests, created in Phase 4)
├── screenshots/
│   ├── 1_setup/
│   ├── 2_numpy/
│   ├── 3_search/
│   └── 4_gui/            (created in Phase 9)
├── diagrams/             (notes, flow charts, comparison)
└── report/
    └── Experiment1_Report.docx
```

- [x] Create the folders.
- [x] Copy the report template into `report/`.
- [x] Write the step prompts in `prompts/`.

---

## Phase 1: Environment Setup (1 h)

**Prompt:** [01_environment_setup.md](../prompts/01_environment_setup.md)

| Step | Do this | Screenshot? |
|---|---|---|
| 1 | Install **Anaconda** (anaconda.com) | ✅ installer + finish page |
| 2 | In Anaconda Prompt, run `python --version` and `conda list numpy` | ✅ |
| 3 | Install **PyCharm Community** | ✅ |
| 4 | Open the project in PyCharm and select the **Anaconda interpreter** | ✅ interpreter settings |
| 5 | Run `code/check_env.py`: numpy, matplotlib, tkinter, Pillow should all show OK | ✅ output |

> Result (2026-10-07): Anaconda in `D:\anaconda3` (Python 3.14.6), PyCharm in `D:\PyCharm`. C: was almost full, so both went on D:. Details: README "Environment".

- [x] Anaconda installed
- [x] PyCharm installed, with the Anaconda interpreter selected
- [x] `check_env.py` shows all OK
- [x] Screenshots saved in `screenshots/1_setup/`

---

## Phase 2: Learn NumPy (1.5 h)

**Prompt:** [02_numpy_demo.md](../prompts/02_numpy_demo.md)

| # | Topic | Functions to show |
|---|---|---|
| 1 | Create arrays | `np.array`, `zeros`, `ones`, `empty`, `arange`, `linspace`, `logspace`, `full`, `fromfunction` |
| 2 | Array properties | `shape`, `size`, `dtype`, `ndim`, `reshape` |
| 3 | Slicing | `a[3:5]`, `a[::-1]`, 2D slicing, shared memory vs copy |
| 4 | Struct array | `np.dtype` with name/age/weight |
| 5 | ufunc | `np.sin`, `add`, `subtract`, `multiply`, comparisons, `frompyfunc` |
| 6 | Broadcasting | `arange(...).reshape(-1, 1) + arange(...)`, `ogrid` |
| 7 | Random | `rand`, `randint`, `normal`, `poisson`, `seed` |
| 8 | Statistics | `sum`, `mean`, `var`, `std`, `sort`, `percentile`, `unique`, `bincount`, `histogram` |
| 9 | Array join and split | `vstack`, `hstack`, `column_stack`, `split` |
| 10 | Polynomials | `poly1d`, `deriv`, `integ`, `roots`, `polyfit` |

> ⚠️ Use `int` instead of `np.int` (removed in new NumPy), and `print(x)` instead of the old `print x`.

- [x] `numpy_demo.py` runs all 10 sections with no errors
- [x] Each section can run alone (`python code/numpy_demo.py 3`)
- [x] Screenshots saved in `screenshots/2_numpy/`

---

## Phase 3: Learn the Theory (45 min)

**Prompt:** [03_theory_notes.md](../prompts/03_theory_notes.md)

### BFS (Breadth-First Search)

- Visits the tree level by level, left to right.
- Uses a **queue** (FIFO: first in, first out).
- Finds the shortest path in an unweighted graph.

### DFS (Depth-First Search)

- Goes deep along one branch first, then backtracks.
- Uses a **stack** (LIFO: last in, first out).
- Uses less memory, but may not find the shortest path.

```
      A
     / \
    B   C
   / \   \
  D   E   F
```

- [x] `diagrams/theory_notes.md` made (tree + BFS and DFS trace tables + key points)
- [x] I can explain BFS and DFS without looking
- [x] Principles section drafted **in my own words**

---

## Phase 4: Search Code (1.5 h)

**Prompt:** [04_search_code.md](../prompts/04_search_code.md)

| Step | Code part | Purpose |
|---|---|---|
| 1 | `from collections import deque` | Gives you the queue/stack structure |
| 2 | `class Graph` with `__init__` | Stores `order` (visit list) and `neighbor` (adjacency list) |
| 3 | `add_node(node)` | Adds a node and its children |
| 4 | `BFS(root)` | Pops from the left and adds children to the end |
| 5 | `DFS(root)` | Pops from the left and adds children to the front, in reverse order |
| 6 | `clear()` / `node_print()` | Reset / print the visit order |
| 7 | `self.steps` | Records every step, so the GUI can animate it |
| 8 | `if __name__ == '__main__'` | Builds the tree and runs BFS, then DFS |

Expected output:

```
BFS: A B C D E F
DFS: A B D E C F
```

Fixes to the teacher's code (mention them in your report):
- The slide text has wrong indentation, so copy from the code images on slides 14–16.
- The DFS `tmp.reverse()` changes the original list, so use `reversed(...)`.
- `add_node` stores bad input even after printing the error, so it now returns.
- A graph with a cycle could visit a node twice, so the code now has a visited check.

- [x] Tests written first, and all of them pass (`tests/test_graph_search.py`)
- [x] `graph_search.py` prints the expected output
- [x] Screenshots saved in `screenshots/3_search/`

---

## Phase 5: GUI Layout (1 h) ⭐

**Prompt:** [05_gui_layout.md](../prompts/05_gui_layout.md)

```
+-------------------------------+----------------+
|                               | Graph    [v]   |
|        TREE CANVAS            | (o) BFS ( ) DFS|
|                               | Start    [v]   |
|                               | [Play][Step]   |
|                               | [Reset] Speed  |
|                               | Legend         |
+-------------------------------+----------------+
| Queue (BFS):  [A] [B] [C]                      |
| Visit order:  [A] [B]                          |
| Status: Step 2 / 6 — visiting B                |
+------------------------------------------------+
```

Node colors: white = not visited · yellow = in the queue/stack · orange = current · green = visited.

- [x] The window opens with all regions and controls
- [x] Resizing works
- [ ] I am happy with the layout and colors (change them now if not)

---

## Phase 6: GUI — Draw the Tree (1 h) ⭐

**Prompt:** [06_gui_draw_tree.md](../prompts/06_gui_draw_tree.md)

Preset graphs: Teacher tree (6 nodes), Bigger tree (15 nodes), Unbalanced tree, Graph with cycle.

- [x] `sample_graphs.py` and `tree_layout.py` made, and the tests pass
- [x] Every preset draws cleanly (no overlap)
- [x] The tree redraws when the window is resized

---

## Phase 7: GUI — BFS/DFS Animation (2 h) ⭐

**Prompt:** [07_gui_animation.md](../prompts/07_gui_animation.md)

- [x] Play / Pause / Step / Reset / Speed all work
- [x] The queue/stack boxes and visit-order boxes update every step
- [x] The GUI shows BFS = A B C D E F and DFS = A B D E C F on the teacher tree
- [x] The animation matches the trace tables from Phase 3
- [x] `step_player.py` tests pass

---

## Phase 8: GUI — Custom Graph Editor (1.5 h) ⭐ Bonus

**Prompt:** [08_gui_custom_graph.md](../prompts/08_gui_custom_graph.md)

Format: one line per parent, e.g. `A: B C`.

- [x] "Edit graph..." dialog works
- [x] Bad input shows a clear error, with no crash
- [x] Parser tests pass
- [ ] I tested my own graph

---

## Phase 9: GUI — Polish + Screenshots (1 h) ⭐

**Prompt:** [09_gui_polish_screenshots.md](../prompts/09_gui_polish_screenshots.md)

- [x] Shortcuts: Space = play/pause, → = step, R = reset
- [x] "Save screenshot" button works
- [x] GUI screenshots saved in `screenshots/4_gui/`
- [x] README has a "How to run" section

---

## Phase 10: Flow Charts (45 min)

**Prompt:** [10_flow_charts.md](../prompts/10_flow_charts.md)

BFS flow (DFS is the same except one box: add the children to the **FRONT**, in reverse order):

```
Start → root empty? ─yes→ print error → End
            │no
     put root in queue
            ↓
  ┌→ queue empty? ─yes→ print order → End
  │         │no
  │   take node from FRONT
  │   already visited? ─yes→ (skip)
  │   add node to order, mark visited
  │   add children to BACK
  └─────────┘
```

- [x] `diagrams/`: tree.png, program_flowchart.png, bfs_flowchart.png, dfs_flowchart.png, gui_flowchart.png
- [x] Every chart is checked against the code

---

## Phase 11: Compare the Results (30 min)

**Prompt:** [11_compare_results.md](../prompts/11_compare_results.md)

| Point | BFS | DFS |
|---|---|---|
| Visit order (teacher tree) | A B C D E F | A B D E C F |
| Data structure | Queue (FIFO) | Stack (LIFO) |
| Search style | Level by level | Branch by branch |
| Memory use | High (stores a whole level) | Low (stores one path) |
| Shortest path? | ✅ Yes | ❌ Not always |
| Time complexity | O(V + E) | O(V + E) |
| Good for | Shortest path, nearby nodes | Deep solutions, mazes, low memory |

`compare.py` adds real numbers: steps, max queue/stack size, and steps to find a target.

- [x] `compare.py` runs, and `diagrams/comparison.md` is made
- [x] Trace tables checked against the real code
- [ ] Analysis written **in my own words**

---

## Phase 12: Write the Report (2.5 h)

**Prompt:** [12_write_report.md](../prompts/12_write_report.md)

| # | Section | What goes in |
|---|---|---|
| 1 | Procedure flow chart | Program, BFS, DFS, and GUI flow charts (Phase 10) |
| 2 | Results and analysis diagram | Console output + GUI screenshots + comparison table |
| 3 | Python setup | Phase 1 steps + screenshots |
| 4 | NumPy learning | Phase 2 code (as text) + output screenshots |
| 5 | BFS/DFS principles | Tree + trace tables + **your text** |
| 6 | Graph + BFS + DFS code steps | Code steps + output + GUI features |
| 7 | Compare results | Comparison table + **your analysis** |
| 8 | Source code + comments | `graph_search.py` (+ GUI code) |
| 9 | Summary and experience | **Your text**: what you learned, problems, fixes |

> 💡 Claude adds the code, images, and tables, and puts **yellow placeholders** where you write in your own words.

- [ ] Header filled in (name, ID, class, lab time, location, advisor)
- [x] All 9 sections added, in order
- [ ] Every yellow placeholder replaced with my own words

---

## Phase 13: Final Check (15 min)

**Prompt:** [13_final_check.md](../prompts/13_final_check.md)

- [x] All tests and scripts pass
- [x] The GUI opens and runs
- [x] All comments and GUI text in English
- [ ] Report: header filled, 9 sections in order, no placeholders left
- [ ] Every screenshot is clear and readable
- [ ] Written in my own words (copying = 0 points)
- [ ] Saved as `.docx` (or PDF if the teacher asks) and submitted

---

## Time Summary

| Phase | Task | Time |
|---|---|---|
| 0 | Prepare | ✅ done |
| 1 | Environment setup | 1 h |
| 2 | NumPy learning | 1.5 h |
| 3 | Theory | 45 min |
| 4 | Search code | 1.5 h |
| 5 | GUI layout ⭐ | 1 h |
| 6 | GUI draw tree ⭐ | 1 h |
| 7 | GUI animation ⭐ | 2 h |
| 8 | GUI custom graph ⭐ (bonus) | 1.5 h |
| 9 | GUI polish + screenshots ⭐ | 1 h |
| 10 | Flow charts | 45 min |
| 11 | Compare results | 30 min |
| 12 | Write report | 2.5 h |
| 13 | Final check | 15 min |
| | **Total** | **about 15.5 h** |

### Order you can follow

```
01 → 02 → 03 → 04 → 05 → 06 → 07 → (08) → 09 → 10 → 11 → 12 → 13
                 ↑
  03 can be done any time (it does not need code)
```
