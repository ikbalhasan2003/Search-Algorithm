# -*- coding: utf-8 -*-
r"""
Experiment 1 - Compare BFS and DFS with real numbers from the program.

For every preset graph (and the custom city map example) it runs BFS and DFS
from the first node and measures:
  - visit order
  - steps            = number of nodes taken out and visited
  - max frontier     = the largest queue (BFS) or stack (DFS) = memory use
  - steps to target  = how many visits until a target node is found. Three targets:
                       deepest right-most (e.g. F in the teacher tree), deepest left-most (D),
                       and the right-most node on level 1 (C)

It also checks the trace tables in diagrams/theory_notes.md against graph.steps.
Results: printed to the console and written to diagrams/comparison.md.

Run:  D:\anaconda3\python.exe code\compare.py
"""
import re
from pathlib import Path

from sample_graphs import CUSTOM_EXAMPLE, PRESETS, build_graph, parse_graph_text
from tree_layout import compute_layout, spanning_tree

PROJECT_DIR = Path(__file__).resolve().parent.parent
NOTES = PROJECT_DIR / "diagrams" / "theory_notes.md"
REPORT = PROJECT_DIR / "diagrams" / "comparison.md"


def all_graphs():
    graphs = dict(PRESETS)
    graphs["Custom graph (city map)"] = parse_graph_text(CUSTOM_EXAMPLE)
    return graphs


TARGETS = ["deep right", "deep left", "level 1 right"]


def find_targets(adjacency, start):
    """{target kind: node}, using the levels and x positions of the drawing."""
    tree = spanning_tree(adjacency, start)
    depth = {start: 0}
    for parent in tree:                      # tree keys are in BFS order
        for child in tree[parent]:
            depth[child] = depth[parent] + 1
    deepest = max(depth.values())
    positions, _ = compute_layout(adjacency, start, 1000, 1000)

    def on_level(level):
        return sorted((n for n in depth if depth[n] == level), key=lambda n: positions[n][0])

    return {"deep right": on_level(deepest)[-1], "deep left": on_level(deepest)[0],
            "level 1 right": on_level(1)[-1]}


def measure(adjacency, algorithm, start, targets):
    graph = build_graph(adjacency)
    order = graph.BFS(start) if algorithm == "BFS" else graph.DFS(start)
    return {
        "order": order,
        "steps": len(graph.steps) - 1,                     # steps[0] is the start state
        "max_frontier": max(len(step["frontier"]) for step in graph.steps),
        # how many visits until each target is found
        "found": {kind: (node, order.index(node) + 1) for kind, node in targets.items()},
    }


def compare_all():
    rows = []
    for name, adjacency in all_graphs().items():
        start = next(iter(adjacency))
        targets = find_targets(adjacency, start)
        for algorithm in ("BFS", "DFS"):
            row = measure(adjacency, algorithm, start, targets)
            row.update(graph=name, algorithm=algorithm, start=start, nodes=len(row["order"]))
            rows.append(row)
    return rows


# ---------- Check the trace tables in theory_notes.md ----------
def read_trace_table(text, title):
    """Return the 'after' column (queue or stack) of one trace table as lists."""
    section = text.split(title, 1)[1].split("**Final", 1)[0]
    lists = []
    for line in section.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 5 and cells[0].isdigit():
            inside = re.search(r"\[(.*?)\]", cells[3]).group(1)
            lists.append([n.strip() for n in inside.split(",") if n.strip()])
    return lists


def check_trace_tables():
    text = NOTES.read_text(encoding="utf-8")
    results = {}
    for algorithm, title in (("BFS", "## 2. BFS Trace Table"), ("DFS", "## 3. DFS Trace Table")):
        graph = build_graph(PRESETS["Teacher tree (6 nodes)"])
        graph.BFS("A") if algorithm == "BFS" else graph.DFS("A")
        from_code = [step["frontier"] for step in graph.steps]
        results[algorithm] = (read_trace_table(text, title) == from_code, from_code)
    return results


def check_self_check_q2():
    """theory_notes.md Q2: add G as a child of D."""
    adjacency = dict(PRESETS["Teacher tree (6 nodes)"], D=["G"])
    bfs = " ".join(build_graph(adjacency).BFS("A"))
    dfs = " ".join(build_graph(adjacency).DFS("A"))
    return bfs, dfs, bfs == "A B C D E F G" and dfs == "A B D G E C F"


# ---------- Output ----------
HEADERS = ["Graph", "Algo", "Nodes", "Steps", "Max queue/stack",
           "Find deep right", "Find deep left", "Find level-1 right", "Visit order"]


def table_cells(row):
    found = [f"{node}: {steps}" for node, steps in (row["found"][k] for k in TARGETS)]
    return [row["graph"], row["algorithm"], str(row["nodes"]), str(row["steps"]),
            str(row["max_frontier"])] + found + [" ".join(row["order"])]


def print_table(rows):
    lines = [HEADERS] + [table_cells(row) for row in rows]
    widths = [max(len(line[i]) for line in lines) for i in range(len(HEADERS))]
    for i, line in enumerate(lines):
        print("  ".join(cell.ljust(width) for cell, width in zip(line, widths)))
        if i == 0:
            print("  ".join("-" * width for width in widths))


def write_markdown(rows, traces, q2):
    out = ["# BFS vs DFS — Comparison With Real Numbers (Step 11)", "",
           "Made by `code/compare.py` (do not edit by hand, run the script again).",
           "Start node = the first node of each graph.", "",
           "## Table 1: Measured results", "",
           "| " + " | ".join(HEADERS) + " |",
           "|" + "---|" * len(HEADERS)]
    out += ["| " + " | ".join(table_cells(row)) + " |" for row in rows]
    out += ["", "- **Steps** = nodes taken out of the queue/stack and visited.",
            "- **Max queue/stack** = the most nodes waiting at one time (memory use). "
            "With a cycle, a node can wait twice, so it is counted twice.",
            "- **Find ...** = `node: k` means the node is found at visit number k "
            "(smaller = found sooner).",
            "  - *deep right* = deepest node, right-most;  *deep left* = deepest node, left-most;",
            "  - *level-1 right* = right-most child of the start node.", "",
            "## Table 2: General comparison", "",
            "| Point | BFS | DFS |", "|---|---|---|",
            "| Data structure | Queue (FIFO) | Stack (LIFO) |",
            "| Search style | Level by level | Branch by branch, then backtrack |",
            "| Memory use | High (a whole level) | Low (one path + waiting siblings) |",
            "| Shortest path (unweighted)? | Yes | Not always |",
            "| Time complexity | O(V + E) | O(V + E) |",
            "| Good for | Shortest path, nearby nodes | Deep goals, mazes, low memory |", "",
            "## Trace table check (diagrams/theory_notes.md vs graph.steps)", ""]
    for algorithm, (ok, _) in traces.items():
        out.append(f"- {algorithm} trace table: **{'matches the code' if ok else 'DIFFERENT'}**")
    out.append(f"- Self-check Q2 (add D -> G): BFS = {q2[0]}, DFS = {q2[1]} -> "
               f"**{'matches the notes' if q2[2] else 'DIFFERENT'}**")
    REPORT.write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    rows = compare_all()
    print("BFS vs DFS - measured results (start = first node)\n")
    print_table(rows)

    traces = check_trace_tables()
    q2 = check_self_check_q2()
    print("\nTrace tables in diagrams/theory_notes.md vs the real code:")
    for algorithm, (ok, from_code) in traces.items():
        print(f"  {algorithm}: {'OK' if ok else 'DIFFERENT'}  (code: {from_code})")
    print(f"  Self-check Q2 (D -> G): BFS {q2[0]} | DFS {q2[1]} -> {'OK' if q2[2] else 'DIFFERENT'}")

    write_markdown(rows, traces, q2)
    print(f"\nSaved {REPORT.relative_to(PROJECT_DIR)}")


if __name__ == "__main__":
    main()
