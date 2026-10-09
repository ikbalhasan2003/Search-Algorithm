# -*- coding: utf-8 -*-
r"""
Experiment 1 - Flow charts and the tree picture for the report (matplotlib).

Saves into diagrams/:
    tree.png               the teacher's tree
    program_flowchart.png  what the main program of graph_search.py does
    bfs_flowchart.png      the BFS function
    dfs_flowchart.png      the DFS function (the one different box is orange)
    gui_flowchart.png      how the GUI animation works

Run:  D:\anaconda3\python.exe code\make_diagrams.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")    # draw to files only, no window
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Polygon  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent.parent / "diagrams"
DPI = 150
FONT_SIZE = 9.5

# Shape colors: (fill, border)
STYLE = {
    "terminal": ("#E3F7EF", "#2F9E78"),    # Start / End
    "process": ("#EAF2FE", "#3B82F6"),
    "decision": ("#FFF7E0", "#D9A400"),
    "highlight": ("#FDE6D6", "#F0803C"),   # the box that makes DFS different from BFS
}
LINE_COLOR = "#33414E"


class FlowChart:
    """A tiny helper: 1 unit = 1 inch, so the saved picture keeps readable text."""

    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.shapes = {}             # key -> (x, y, w, h)
        self.points = []             # every used point, to find the picture size

    # ----- shapes -----
    def terminal(self, key, x, y, text, w=1.6, h=0.5):
        self._box(key, x, y, w, h, text, "terminal", rounding=h / 2)

    def process(self, key, x, y, text, w=2.8, h=0.6, highlight=False):
        self._box(key, x, y, w, h, text, "highlight" if highlight else "process", rounding=0.06)

    def decision(self, key, x, y, text, w=3.0, h=1.0):
        fill, border = STYLE["decision"]
        corners = [(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)]
        self.ax.add_patch(Polygon(corners, closed=True, facecolor=fill, edgecolor=border,
                                  linewidth=1.5))
        self._register(key, x, y, w, h, text)

    def _box(self, key, x, y, w, h, text, style, rounding):
        fill, border = STYLE[style]
        self.ax.add_patch(FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h, boxstyle=f"round,pad=0,rounding_size={rounding}",
            facecolor=fill, edgecolor=border, linewidth=2 if style == "highlight" else 1.5))
        self._register(key, x, y, w, h, text)

    def _register(self, key, x, y, w, h, text):
        self.ax.text(x, y, text, ha="center", va="center", fontsize=FONT_SIZE,
                     color=LINE_COLOR, linespacing=1.3)
        self.shapes[key] = (x, y, w, h)
        self.points += [(x - w / 2, y - h / 2), (x + w / 2, y + h / 2)]

    def at(self, key, side):
        """A point on the edge of a shape: side = top, bottom, left, or right."""
        x, y, w, h = self.shapes[key]
        return {"top": (x, y + h / 2), "bottom": (x, y - h / 2),
                "left": (x - w / 2, y), "right": (x + w / 2, y)}[side]

    # ----- arrows -----
    def arrow(self, *points, label=None, head=True):
        """A line through the points; the arrow head is at the last point.
        label (e.g. "Yes") is written next to the first point."""
        points = [self.at(*p) if isinstance(p[1], str) else p for p in points]   # (key, side)
        self.points += points
        xs, ys = zip(*points[:-1]) if len(points) > 2 else ((), ())
        if xs:
            self.ax.plot(xs, ys, color=LINE_COLOR, linewidth=1.3, solid_capstyle="butt")
        start, end = points[-2], points[-1]
        if head:
            self.ax.annotate("", xy=end, xytext=start, arrowprops=dict(
                arrowstyle="-|>", color=LINE_COLOR, lw=1.3, shrinkA=0, shrinkB=0,
                mutation_scale=13))
        else:
            self.ax.plot([start[0], end[0]], [start[1], end[1]], color=LINE_COLOR,
                         linewidth=1.3)
        if label:
            (x1, y1), (x2, y2) = points[0], points[1]
            if abs(x2 - x1) > abs(y2 - y1):          # goes sideways: label above the line
                pos, align = ((x1 + (0.12 if x2 > x1 else -0.12)), y1 + 0.1), \
                    ("left" if x2 > x1 else "right", "bottom")
            else:                                    # goes down: label right of the line
                pos, align = (x1 + 0.1, y1 - 0.08), ("left", "top")
            self.ax.text(*pos, label, ha=align[0], va=align[1], fontsize=FONT_SIZE - 0.5,
                         fontweight="bold", color="#B42318" if label.startswith("Yes")
                         else "#1D6F42")

    def title(self, x, y, text):
        self.ax.text(x, y, text, ha="center", va="bottom", fontsize=FONT_SIZE + 2.5,
                     fontweight="bold", color=LINE_COLOR)
        self.points.append((x, y + 0.35))

    def save(self, name, pad=0.25):
        xs, ys = zip(*self.points)
        left, right = min(xs) - pad, max(xs) + pad
        bottom, top = min(ys) - pad, max(ys) + pad
        self.fig.set_size_inches(right - left, top - bottom)
        self.ax.set_xlim(left, right)
        self.ax.set_ylim(bottom, top)
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.fig.subplots_adjust(0, 0, 1, 1)
        path = OUT_DIR / name
        self.fig.savefig(path, dpi=DPI, facecolor="white")
        plt.close(self.fig)
        print("saved", path)


# ---------- 1. The teacher's tree ----------
def make_tree():
    positions = {"A": (2.0, 2.0), "B": (1.0, 1.0), "C": (3.0, 1.0),
                 "D": (0.5, 0.0), "E": (1.5, 0.0), "F": (3.0, 0.0)}
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F")]
    radius = 0.24
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    for parent, child in edges:
        (x1, y1), (x2, y2) = positions[parent], positions[child]
        ax.annotate("", xy=(x2, y2 + radius), xytext=(x1, y1 - radius), arrowprops=dict(
            arrowstyle="-|>", color="#7B8794", lw=1.5, shrinkA=0, shrinkB=0,
            mutation_scale=12))
    for node, (x, y) in positions.items():
        ax.add_patch(Circle((x, y), radius, facecolor="#EAF2FE", edgecolor="#3B82F6",
                            linewidth=2))
        ax.text(x, y, node, ha="center", va="center", fontsize=13, fontweight="bold",
                color=LINE_COLOR)
    for level in range(3):
        ax.text(-0.35, 2 - level, f"Level {level}", ha="right", va="center", fontsize=9,
                color="#616E7C")
    ax.set_xlim(-1.3, 3.5)
    ax.set_ylim(-0.4, 2.4)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.subplots_adjust(0, 0, 1, 1)
    path = OUT_DIR / "tree.png"
    fig.savefig(path, dpi=DPI, facecolor="white")
    plt.close(fig)
    print("saved", path)


# ---------- 2. Main program ----------
def make_program_flowchart():
    c = FlowChart()
    c.title(0, 0.45, "Main program (graph_search.py)")
    steps = [
        ("terminal", "Start"),
        ("process", "g = Graph()"),
        ("process", "add_node: A -> [B, C]\nB -> [D, E],  C -> [F]"),
        ("process", "g.BFS('A')"),
        ("process", "print  BFS: A B C D E F"),
        ("process", "g.clear()\n(empty order and steps)"),
        ("process", "g.DFS('A')"),
        ("process", "print  DFS: A B D E C F"),
        ("terminal", "End"),
    ]
    y = 0
    for i, (kind, text) in enumerate(steps):
        if kind == "terminal":
            c.terminal(i, 0, y, text)
        else:
            c.process(i, 0, y, text, h=0.7 if "\n" in text else 0.5)
        if i:
            c.arrow((i - 1, "bottom"), (i, "top"))
        y -= 0.95
    c.save("program_flowchart.png")


# ---------- 3. BFS and DFS ----------
def make_search_flowchart(algorithm):
    bfs = algorithm == "BFS"
    box = "queue" if bfs else "stack"
    c = FlowChart()
    c.title(0.6, 0.45, f"{algorithm}(root)" + ("  — queue, FIFO" if bfs else "  — stack, LIFO"))

    c.terminal("start", 0, 0, "Start")
    c.decision("root", 0, -1.15, "root is None or\nnot in the graph?")
    c.process("error", 3.4, -1.15, "print an error\nreturn [ ]", w=2.0)
    c.terminal("end1", 3.4, -2.2, "End")
    c.process("init", 0, -2.4, f"{box} = [root]\nvisited = [ ]")
    c.decision("empty", 0, -3.7, f"Is the {box}\nempty?")
    c.process("print", 3.4, -3.7, "return the\nvisit order", w=2.0)
    c.terminal("end2", 3.4, -4.75, "End")
    if bfs:
        c.process("pop", 0, -5.0, "node = queue.popleft()\n(take from the FRONT)")
    else:
        c.process("pop", 0, -5.0, "node = stack.popleft()\n(take from the TOP)")
    c.decision("seen", 0, -6.3, "node already\nvisited?")
    c.process("visit", 0, -7.6, "order.append(node)\nvisited.append(node)")
    if bfs:
        c.process("add", 0, -8.75, "queue += children\n(add children to the BACK)")
    else:
        c.process("add", 0, -8.95, "for child in reversed(children):\n    stack.appendleft(child)\n"
                  "(children to the FRONT, reversed)", w=3.2, h=1.0, highlight=True)

    c.arrow(("start", "bottom"), ("root", "top"))
    c.arrow(("root", "right"), ("error", "left"), label="Yes")
    c.arrow(("error", "bottom"), ("end1", "top"))
    c.arrow(("root", "bottom"), ("init", "top"), label="No")
    c.arrow(("init", "bottom"), ("empty", "top"))
    c.arrow(("empty", "right"), ("print", "left"), label="Yes")
    c.arrow(("print", "bottom"), ("end2", "top"))
    c.arrow(("empty", "bottom"), ("pop", "top"), label="No")
    c.arrow(("pop", "bottom"), ("seen", "top"))
    c.arrow(("seen", "bottom"), ("visit", "top"), label="No")
    c.arrow(("visit", "bottom"), ("add", "top"))
    # Loop back to "empty?" (the skip branch joins the same line)
    loop_x = -2.4
    add_left, empty_left = c.at("add", "left"), c.at("empty", "left")
    c.arrow(add_left, (loop_x, add_left[1]), (loop_x, empty_left[1]), empty_left)
    c.arrow(c.at("seen", "left"), (loop_x, c.at("seen", "left")[1]), label="Yes (skip)",
            head=False)
    c.save(f"{algorithm.lower()}_flowchart.png")


# ---------- 4. GUI animation ----------
def make_gui_flowchart():
    c = FlowChart()
    c.title(0.9, 0.45, "GUI animation (gui_app.py)")
    c.terminal("start", 0, 0, "Start")
    c.process("window", 0, -0.95, "Open the window\ndraw the tree (tree_layout)", w=3.0, h=0.7)
    c.process("choose", 0, -2.05, "User chooses graph,\nalgorithm, and start node", w=3.0,
              h=0.7)
    c.process("run", 0, -3.15, "Run BFS or DFS once,\nsave every step (StepPlayer)", w=3.0,
              h=0.7)
    c.process("render", 0, -4.25, "Render the current step:\nnode colors, queue/stack, order",
              w=3.0, h=0.7)
    c.decision("last", 0, -5.5, "Last step?")
    c.process("done", 3.6, -5.5, "Status: \"Done!\"\nPlay becomes Replay", w=2.4, h=0.7)
    c.terminal("end", 3.6, -6.55, "End")
    c.decision("playing", 0, -6.95, "Playing?")
    c.process("wait_user", 3.6, -8.0, "Wait for the user:\nPlay or Step", w=2.4, h=0.7)
    c.process("wait", 0, -8.25, "Wait speed ms\n(root.after)", w=2.4, h=0.7)
    c.process("next", 0, -9.4, "Next step\n(player.next())", w=2.4, h=0.7)

    c.arrow(("start", "bottom"), ("window", "top"))
    c.arrow(("window", "bottom"), ("choose", "top"))
    c.arrow(("choose", "bottom"), ("run", "top"))
    c.arrow(("run", "bottom"), ("render", "top"))
    c.arrow(("render", "bottom"), ("last", "top"))
    c.arrow(("last", "right"), ("done", "left"), label="Yes")
    c.arrow(("done", "bottom"), ("end", "top"))
    c.arrow(("last", "bottom"), ("playing", "top"), label="No")
    c.arrow(("playing", "bottom"), ("wait", "top"), label="Yes")
    c.arrow(c.at("playing", "right"), (c.at("wait_user", "top")[0], c.at("playing", "right")[1]),
            c.at("wait_user", "top"), label="No")
    c.arrow(("wait", "bottom"), ("next", "top"))
    c.arrow(c.at("wait_user", "bottom"), (c.at("wait_user", "bottom")[0], -9.4),
            c.at("next", "right"))
    # Loop back to "Render"
    loop_x = -2.2
    next_left, render_left = c.at("next", "left"), c.at("render", "left")
    c.arrow(next_left, (loop_x, next_left[1]), (loop_x, render_left[1]), render_left)
    c.ax.text(c.at("choose", "right")[0] + 0.15, c.at("choose", "right")[1],
              "a new choice at any time\n= Reset, start again here", ha="left", va="center",
              fontsize=FONT_SIZE - 1, style="italic", color="#616E7C")
    c.ax.text(loop_x - 0.1, -6.9, "loop", rotation=90, ha="right", va="center",
              fontsize=FONT_SIZE - 0.5, color="#616E7C")
    c.save("gui_flowchart.png")


def main():
    OUT_DIR.mkdir(exist_ok=True)
    make_tree()
    make_program_flowchart()
    make_search_flowchart("BFS")
    make_search_flowchart("DFS")
    make_gui_flowchart()


if __name__ == "__main__":
    main()
