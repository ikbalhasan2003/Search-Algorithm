# Experiment 1: Search Algorithm

Introduction to Artificial Intelligence — Wuhan Institute of Technology, International College.

- Full plan: [Docs/Experiment1_Roadmap.md](Docs/Experiment1_Roadmap.md)
- Step prompts (one per phase): [prompts/README.md](prompts/README.md)
- **What is left for me:** [MY_TODO.md](MY_TODO.md)

## Environment

Set up in Step 01 (2026-10-07). **All later steps must use this Python.**

| Item | Value |
|---|---|
| Anaconda | 2026.07-1, installed in `D:\anaconda3` (C: drive is almost full) |
| conda | 26.5.3 |
| Python interpreter | `D:\anaconda3\python.exe` (Python 3.14.6) |
| Libraries | numpy 2.4.6 · matplotlib 3.11.0 · tkinter 8.6 · Pillow 12.2.0 |
| PyCharm | installed in `D:\PyCharm`, project interpreter = Conda `D:\anaconda3` (base) |

Run command (from the project folder):

```
D:\anaconda3\python.exe code\check_env.py
```

Other scripts run the same way: `D:\anaconda3\python.exe code\<file>.py`.
In PyCharm: right-click the file → **Run**.

> ⚠️ Do not use `C:\Python314\python.exe`. It has no numpy or matplotlib.
> Anaconda is **not** on PATH, so a plain `python` in a normal terminal runs the wrong Python.
> Use the full path above, the **Anaconda Prompt**, or PyCharm.

## How to Run

All commands run from the project folder `C:\Users\admin\Desktop\New folder (2)`.

| What | Command |
|---|---|
| GUI (BFS/DFS animation) | `D:\anaconda3\python.exe code\gui_app.py` |
| All unit tests | `D:\anaconda3\python.exe -m unittest discover -s tests -v` |
| BFS + DFS console output | `D:\anaconda3\python.exe code\graph_search.py` |
| All preset graphs, BFS + DFS | `D:\anaconda3\python.exe code\sample_graphs.py` |
| GUI screenshots for the report | `D:\anaconda3\python.exe code\make_gui_screenshots.py` (do not touch the mouse for ~10 s) |
| Flow chart images | `D:\anaconda3\python.exe code\make_diagrams.py` |
| BFS vs DFS comparison | `D:\anaconda3\python.exe code\compare.py` |

GUI controls:

| Control | What it does |
|---|---|
| Graph | Choose a preset graph (or "Custom graph" after you made one) |
| Edit graph... | Type your own graph, one parent per line: `A: B C` |
| BFS / DFS | Choose the algorithm (resets the run) |
| Start | Choose the start node (resets the run) |
| Play / Pause / Replay | Run the animation · **Space** |
| Step | One step forward · **Right arrow** |
| Reset | Back to step 0 · **R** |
| Speed | 100–2000 ms per step |
| Save screenshot | Saves the window to `screenshots/4_gui/<algorithm>_<graph>_step<k>.png` |

Node colors: white = not visited · yellow = in the queue/stack · orange = current · green = visited.
Thick blue edge = the edge the current node was reached by. Dashed edge = not part of the tree (cycle or cross link).

## Folder Structure

```
New folder (2)/
├── README.md                   ← this file
├── MY_TODO.md                  ← what I still must do by hand (header, own text, submit)
├── Docs/                       ← teacher files (do not edit) + roadmap
│   ├── Experiment1 Searching algorithm.docx   (task + template)
│   ├── Search Algortihm.pptx                  (BFS/DFS slides)
│   ├── Numpy.pptx                             (NumPy slides)
│   └── Experiment1_Roadmap.md                 (project plan)
├── prompts/                    ← one prompt file per phase (01–13)
├── code/
│   ├── check_env.py            ← Phase 1  (done) environment check
│   ├── numpy_demo.py           ← Phase 2  (done) 10 NumPy topics, run one: `numpy_demo.py 3`
│   ├── graph_search.py         ← Phase 4  (done) Graph + BFS + DFS + steps for the GUI
│   ├── gui_app.py              ← Phase 5–9 (done) the GUI: drawing, animation, editor, shortcuts
│   ├── sample_graphs.py        ← Phase 6, 8 (done) 4 preset graphs + parser for custom graphs
│   ├── tree_layout.py          ← Phase 6  (done) node positions on the canvas (no Tkinter)
│   ├── step_player.py          ← Phase 7  (done) walks through the search steps (no Tkinter)
│   ├── make_gui_screenshots.py ← Phase 9  (done) makes screenshots/4_gui/*.png automatically
│   ├── make_diagrams.py        ← Phase 10 (done) flow charts + tree.png (matplotlib)
│   └── compare.py              ← Phase 11 (done) BFS vs DFS numbers -> diagrams/comparison.md
├── tests/                      ← Phase 4+ unit tests
│   ├── test_graph_search.py    ← Phase 4  (done) tests for graph_search.py
│   ├── test_tree_layout.py     ← Phase 6  (done) tests for tree_layout.py + presets
│   ├── test_step_player.py     ← Phase 7  (done) tests for step_player.py
│   └── test_parse_graph.py     ← Phase 8  (done) tests for the custom graph parser
├── screenshots/
│   ├── 1_setup/                ← Phase 1: Anaconda, PyCharm, check_env
│   ├── 2_numpy/                ← Phase 2: NumPy output (code goes in report as text)
│   ├── 3_search/               ← Phase 4, 11: BFS/DFS output
│   └── 4_gui/                  ← Phase 9 (done): GUI screenshots 01–09
├── diagrams/                   ← Phase 3, 10, 11: notes, flow charts, comparison
│   ├── theory_notes.md         ← Phase 3  (done) tree, BFS/DFS trace tables, key points
│   ├── tree.png, *_flowchart.png ← Phase 10 (done) 1 tree + 4 flow charts
│   └── comparison.md           ← Phase 11 (done) measured BFS vs DFS tables
└── report/
    └── Experiment1_Report.docx ← Phase 12 (done by Claude): 9 sections; yellow boxes = my own text
```

## Which Phase Uses Which Folder

| Phase | Task | Prompt | Main output |
|---|---|---|---|
| 1 | Environment setup | `prompts/01_...` | `code/check_env.py`, `screenshots/1_setup/` |
| 2 | NumPy learning | `prompts/02_...` | `code/numpy_demo.py`, `screenshots/2_numpy/` |
| 3 | Theory | `prompts/03_...` | `diagrams/theory_notes.md` |
| 4 | Search code | `prompts/04_...` | `code/graph_search.py`, `tests/`, `screenshots/3_search/` |
| 5 | GUI layout ⭐ | `prompts/05_...` | `code/gui_app.py` |
| 6 | GUI draw tree ⭐ | `prompts/06_...` | `code/sample_graphs.py`, `code/tree_layout.py` |
| 7 | GUI animation ⭐ | `prompts/07_...` | `code/step_player.py`, `code/gui_app.py` |
| 8 | GUI custom graph ⭐ | `prompts/08_...` | `code/sample_graphs.py`, `code/gui_app.py` |
| 9 | GUI polish ⭐ | `prompts/09_...` | `screenshots/4_gui/` |
| 10 | Flow charts | `prompts/10_...` | `code/make_diagrams.py`, `diagrams/*.png` |
| 11 | Compare | `prompts/11_...` | `code/compare.py`, `diagrams/comparison.md` |
| 12 | Write report | `prompts/12_...` | `report/Experiment1_Report.docx` |
| 13 | Final check | `prompts/13_...` | checklist |

## Screenshot Naming Tip

Number your screenshots so they stay in order, e.g.:

```
1_setup/01_anaconda_download.png
2_numpy/01_create_arrays.png
3_search/01_output.png
4_gui/03_bfs_done.png
```
