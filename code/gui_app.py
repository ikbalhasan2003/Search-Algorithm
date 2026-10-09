# -*- coding: utf-8 -*-
r"""
Experiment 1 - GUI: Search Algorithm Visualizer (BFS & DFS)

Step 05: window skeleton.  Step 06: draws the selected graph as a tree.
Step 07: animates BFS / DFS step by step (Play, Pause, Step, Reset, Speed).
Step 08: "Edit graph..." dialog for your own graph.
Step 09: keyboard shortcuts, "Save screenshot" button, button states.

Shortcuts:  Space = Play/Pause    Right arrow = Step    R = Reset

Run:  D:\anaconda3\python.exe code\gui_app.py
"""
import math
import re
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from sample_graphs import (CUSTOM_EXAMPLE, MAX_NAME_LENGTH, MAX_NODES, PRESETS,
                           build_graph, graph_to_text, parse_graph_text)
from step_player import StepPlayer, discovery_parents
from tree_layout import all_nodes, compute_layout

# ---------- Design tokens (change colors and fonts here only) ----------
COLORS = {
    "bg": "#F5F7FA",              # window background
    "panel": "#FFFFFF",           # control panel and info bar
    "text": "#1F2933",
    "muted": "#616E7C",           # hints and placeholder text
    "edge": "#9AA5B1",            # tree edges
    "unvisited_fill": "#FFFFFF",
    "unvisited_border": "#52606D",
    "frontier": "#F7C948",        # yellow = waiting in queue/stack
    "current": "#F0803C",         # orange = being visited now
    "visited": "#3EBD93",         # green = done
    "accent": "#3B82F6",          # Play button, highlighted edge
}

FONT_UI = ("Segoe UI", 10)
FONT_HEADER = ("Segoe UI", 11, "bold")
FONT_NODE = ("Segoe UI", 12, "bold")
FONT_BOX = ("Segoe UI", 10, "bold")

PANEL_WIDTH = 240                 # the control panel keeps this width when resizing
SPEED_MIN, SPEED_MAX, SPEED_DEFAULT = 100, 2000, 800   # ms per step

NODE_RADIUS = 22                  # normal node size; smaller when the graph is crowded
NODE_RADIUS_MIN = 10
CANVAS_MARGIN = 50                # free space around the tree, in pixels

PLAY_TEXT, PAUSE_TEXT, REPLAY_TEXT = "▶  Play", "❚❚  Pause", "↻  Replay"
CUSTOM_NAME = "Custom graph"

# Built from this file's location, so the app works from any working folder
PROJECT_DIR = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = PROJECT_DIR / "screenshots" / "4_gui"


def enable_high_dpi():
    """Make text sharp on Windows high-DPI screens. Must run before tk.Tk()."""
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (ImportError, AttributeError, OSError):
        pass  # not Windows, or an old Windows: the app still works, just less sharp


class App:
    def __init__(self, root):
        self.root = root
        root.title("Search Algorithm Visualizer — BFS & DFS")
        root.geometry("1200x750")
        root.minsize(1000, 650)
        root.configure(bg=COLORS["bg"])

        # All graphs the user can pick: name -> adjacency dict
        self.graphs = dict(PRESETS)
        # Canvas item ids, so a step can recolor them with itemconfig (no full redraw)
        self.node_items = {}      # node -> (circle_id, text_id)
        self.edge_items = {}      # (parent, child) -> line_id

        # Animation state
        self.player = StepPlayer([])   # replaced by prepare_run()
        self.parents = {}              # node -> the node that put it in the queue/stack
        self.playing = False
        self.after_id = None           # id of the next scheduled tick (root.after)

        # Tk variables: the widgets read and write these
        self.graph_var = tk.StringVar(value=next(iter(self.graphs)))
        self.algo_var = tk.StringVar(value="BFS")
        self.start_var = tk.StringVar()
        self.speed_var = tk.IntVar(value=SPEED_DEFAULT)
        self.frontier_title_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Status: Ready")

        self._setup_styles()

        # Grid: the canvas cell (row 0, column 0) gets all extra space,
        # so the panel and the info bar keep their size.
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self._build_canvas()
        self._build_controls()
        self._build_info_bar()
        self.frontier_title_var.set("Queue (front → back):")
        self._on_graph_change()       # fill the Start list and prepare the first run
        self._bind_shortcuts()

    # ---------- Styles ----------
    def _setup_styles(self):
        style = ttk.Style(self.root)
        # "clam" lets us change button colors; the default Windows theme ignores them.
        style.theme_use("clam")
        style.configure(".", font=FONT_UI, background=COLORS["panel"],
                        foreground=COLORS["text"])
        style.configure("Panel.TFrame", background=COLORS["panel"])
        style.configure("Header.TLabel", font=FONT_HEADER)
        style.configure("Muted.TLabel", foreground=COLORS["muted"])
        style.configure("Hint.TLabel", foreground=COLORS["muted"], font=("Segoe UI", 9))
        style.configure("TButton", padding=4)
        style.configure("Small.TButton", padding=(4, 0))
        # Readonly comboboxes are gray in "clam"; make them white like normal fields
        style.map("TCombobox", fieldbackground=[("readonly", "white")])
        style.configure("Accent.TButton", background=COLORS["accent"], foreground="white")
        style.map("Accent.TButton", background=[("active", "#2563EB")])

    # ---------- 1. Tree canvas (left, grows with the window) ----------
    def _build_canvas(self):
        self.canvas = tk.Canvas(self.root, bg=COLORS["panel"], highlightthickness=1,
                                highlightbackground=COLORS["edge"])
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=(12, 6), pady=(12, 6))
        # The canvas size changes when the window is resized: draw the tree again
        self.canvas.bind("<Configure>", lambda _event: self.draw_tree())

    # ---------- Drawing the tree ----------
    def current_adjacency(self):
        return self.graphs[self.graph_var.get()]

    def draw_tree(self):
        """Delete everything and draw the current graph from the current start node."""
        self.canvas.delete("all")
        self.node_items, self.edge_items = {}, {}
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        start = self.start_var.get()
        if width < 50 or height < 50 or not start:
            return    # the window is not shown yet

        adjacency = self.current_adjacency()
        positions, extra_edges = compute_layout(adjacency, start, width, height,
                                                margin=CANVAS_MARGIN)
        radius = self._node_radius(positions)
        # Smaller nodes need a smaller font; 3-letter names need a bit smaller still
        longest = max(len(node) for node in positions)
        size = FONT_NODE[1] * radius / NODE_RADIUS * (0.8 if longest >= 3 else 1)
        node_font = (FONT_NODE[0], max(7, round(size)), "bold")

        # Edges first, so the nodes are drawn on top of them
        for parent, children in adjacency.items():
            for child in children:
                dashed = (parent, child) in extra_edges
                self.edge_items[(parent, child)] = self._draw_edge(
                    positions[parent], positions[child], radius, dashed)

        for node, (x, y) in positions.items():
            circle = self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                fill=COLORS["unvisited_fill"], outline=COLORS["unvisited_border"], width=2)
            label = self.canvas.create_text(x, y, text=node, font=node_font,
                                            fill=COLORS["text"])
            self.node_items[node] = (circle, label)

        self.render_step()   # after a resize, show the same step again

    def _node_radius(self, positions):
        """22 px normally; smaller if two nodes are close (so circles never overlap)."""
        points = list(positions.values())
        closest = min((math.dist(p, q) for i, p in enumerate(points) for q in points[i + 1:]),
                      default=4 * NODE_RADIUS)
        return max(NODE_RADIUS_MIN, min(NODE_RADIUS, closest * 0.38))

    def _draw_edge(self, start, end, radius, dashed):
        """A line from circle edge to circle edge, with a small arrow at the child end."""
        (x1, y1), (x2, y2) = start, end
        length = math.dist(start, end) or 1
        dx, dy = (x2 - x1) / length, (y2 - y1) / length
        return self.canvas.create_line(
            x1 + dx * radius, y1 + dy * radius, x2 - dx * radius, y2 - dy * radius,
            fill=COLORS["edge"], width=2, arrow=tk.LAST, arrowshape=(9, 11, 4),
            dash=(6, 4) if dashed else ())

    # ---------- 2. Control panel (right, fixed width) ----------
    def _build_controls(self):
        panel = ttk.Frame(self.root, style="Panel.TFrame", padding=12, width=PANEL_WIDTH)
        panel.grid(row=0, column=1, sticky="ns", padx=(6, 12), pady=(12, 6))
        panel.pack_propagate(False)       # keep PANEL_WIDTH even if the content is smaller

        def header(text):
            ttk.Label(panel, text=text, style="Header.TLabel").pack(anchor="w", pady=(0, 4))

        def label(text, top=0):
            ttk.Label(panel, text=text).pack(anchor="w", pady=(top, 0))

        header("CONTROLS")

        # Graph choice + the button that opens the graph editor
        graph_row = ttk.Frame(panel, style="Panel.TFrame")
        graph_row.pack(fill="x")
        ttk.Label(graph_row, text="Graph").pack(side="left")
        ttk.Button(graph_row, text="Edit graph...", style="Small.TButton",
                   command=self.open_graph_editor, takefocus=False).pack(side="right")
        self.graph_box = ttk.Combobox(panel, textvariable=self.graph_var,
                                      values=list(self.graphs), state="readonly")
        self.graph_box.pack(fill="x", pady=(2, 6))
        self.graph_box.bind("<<ComboboxSelected>>", lambda _event: self._on_graph_change())

        # Algorithm choice
        label("Algorithm")
        algo_row = ttk.Frame(panel, style="Panel.TFrame")
        algo_row.pack(fill="x", pady=(2, 0))
        for name in ("BFS", "DFS"):
            ttk.Radiobutton(algo_row, text=name, value=name, variable=self.algo_var,
                            command=self._on_algorithm_change, takefocus=False).pack(
                side="left", padx=(8, 16))

        # Start node (the list is filled when a graph is chosen)
        label("Start", top=6)
        self.start_box = ttk.Combobox(panel, textvariable=self.start_var, values=[],
                                      state="readonly")
        self.start_box.pack(fill="x", pady=(2, 8))
        self.start_box.bind("<<ComboboxSelected>>", lambda _event: self._on_start_change())

        # Buttons
        # takefocus=False: Space is our Play shortcut, it must not also press a focused button
        self.play_button = ttk.Button(panel, text=PLAY_TEXT, style="Accent.TButton",
                                      command=self.toggle_play, takefocus=False)
        self.play_button.pack(fill="x", pady=2)
        self.step_button = ttk.Button(panel, text="▶|  Step", command=self.step_once,
                                      takefocus=False)
        self.step_button.pack(fill="x", pady=2)
        ttk.Button(panel, text="Reset", command=self.reset_run, takefocus=False).pack(
            fill="x", pady=2)
        ttk.Label(panel, text="Space: play/pause   →: step   R: reset",
                  style="Hint.TLabel").pack(anchor="w", pady=(2, 0))

        # Speed slider: ms per step
        speed_row = ttk.Frame(panel, style="Panel.TFrame")
        speed_row.pack(fill="x", pady=(8, 0))
        ttk.Label(speed_row, text="Speed").pack(side="left")
        self.speed_label = ttk.Label(speed_row, style="Muted.TLabel")
        self.speed_label.pack(side="right")
        ttk.Scale(panel, from_=SPEED_MIN, to=SPEED_MAX, variable=self.speed_var,
                  command=self._on_speed_change).pack(fill="x")
        self._on_speed_change()

        header_gap = ttk.Frame(panel, style="Panel.TFrame", height=10)
        header_gap.pack()
        header("LEGEND")
        self._build_legend(panel)

    def _build_legend(self, panel):
        items = [
            (COLORS["unvisited_fill"], "Not visited"),
            (COLORS["frontier"], "In queue/stack"),
            (COLORS["current"], "Current"),
            (COLORS["visited"], "Visited"),
        ]
        for fill, text in items:
            line = ttk.Frame(panel, style="Panel.TFrame")
            line.pack(anchor="w", pady=1)
            dot = tk.Canvas(line, width=20, height=20, bg=COLORS["panel"],
                            highlightthickness=0)
            dot.create_oval(3, 3, 17, 17, fill=fill, outline=COLORS["unvisited_border"],
                            width=1.5)
            dot.pack(side="left")
            ttk.Label(line, text=text).pack(side="left", padx=(6, 0))

    # ---------- 3. Info bar (bottom, full width) ----------
    def _build_info_bar(self):
        bar = ttk.Frame(self.root, style="Panel.TFrame", padding=(12, 8))
        bar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=12, pady=(6, 12))
        bar.columnconfigure(1, weight=1)

        # Column 0 = titles, column 1 = the node boxes
        ttk.Label(bar, textvariable=self.frontier_title_var, width=22).grid(
            row=0, column=0, sticky="w", pady=2)
        self.frontier_frame = ttk.Frame(bar, style="Panel.TFrame")
        self.frontier_frame.grid(row=0, column=1, sticky="w")

        ttk.Label(bar, text="Visit order:", width=22).grid(row=1, column=0, sticky="w", pady=2)
        self.order_frame = ttk.Frame(bar, style="Panel.TFrame")
        self.order_frame.grid(row=1, column=1, sticky="w")

        ttk.Label(bar, textvariable=self.status_var).grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(4, 0))

        ttk.Button(bar, text="Save screenshot", command=self.save_screenshot,
                   takefocus=False).grid(row=0, column=2, rowspan=3, sticky="e")

    def _fill_boxes(self, frame, nodes, color):
        """Show nodes as small colored boxes in one row of the info bar."""
        for widget in frame.winfo_children():
            widget.destroy()
        if not nodes:
            ttk.Label(frame, text="(empty)", style="Muted.TLabel").pack(side="left")
        for node in nodes:
            tk.Label(frame, text=node, bg=color, fg=COLORS["text"], font=FONT_BOX,
                     width=max(3, len(node) + 1), relief="solid", borderwidth=1).pack(side="left", padx=2)

    # ---------- Running a search ----------
    def prepare_run(self):
        """Run BFS or DFS on the current graph and keep the steps for the animation."""
        graph = build_graph(self.current_adjacency())
        algorithm = self.algo_var.get()
        if algorithm == "BFS":
            graph.BFS(self.start_var.get())
        else:
            graph.DFS(self.start_var.get())
        self.player = StepPlayer(graph.steps)
        self.parents = discovery_parents(graph.steps, algorithm)

    def render_step(self):
        """Show the current step: node colors, highlighted edge, boxes, and status."""
        step = self.player.current()
        if step is None or not self.node_items:
            return
        current = step["current"]

        for node, (circle, _label) in self.node_items.items():
            if node == current:
                fill = COLORS["current"]
            elif node in step["visited"]:
                fill = COLORS["visited"]
            elif node in step["frontier"]:
                fill = COLORS["frontier"]
            else:
                fill = COLORS["unvisited_fill"]
            self.canvas.itemconfigure(circle, fill=fill)

        # Highlight only the edge the current node was reached by
        for line in self.edge_items.values():
            self.canvas.itemconfigure(line, fill=COLORS["edge"], width=2)
        edge = self.edge_items.get((self.parents.get(current), current))
        if edge is not None:
            self.canvas.itemconfigure(edge, fill=COLORS["accent"], width=4)

        self._fill_boxes(self.frontier_frame, step["frontier"], COLORS["frontier"])
        self._fill_boxes(self.order_frame, step["order"], COLORS["visited"])
        self.status_var.set("Status: " + self._status_text(step))
        self._update_buttons()

    def _status_text(self, step):
        algorithm = self.algo_var.get()
        container = "queue" if algorithm == "BFS" else "stack"
        if step["step"] == 0:
            return f"Start: put {self.start_var.get()} in the {container}"
        if self.player.is_done():
            text = f"Done! {algorithm} order: " + " ".join(step["order"])
            if step["frontier"]:
                # Cycles: a node can wait in the queue/stack twice. It is skipped later.
                text += (f"   ({', '.join(step['frontier'])} left in the {container}: "
                         "already visited, so skipped)")
            return text
        added = ", ".join(step["added"]) or "nothing"
        return (f"Step {step['step']} / {self.player.total - 1} — "
                f"visiting {step['current']}. Added: {added}")

    def _update_buttons(self):
        if self.player.is_done():
            text = REPLAY_TEXT
        elif self.playing:
            text = PAUSE_TEXT
        else:
            text = PLAY_TEXT
        self.play_button.configure(text=text)
        self.step_button.state(["disabled"] if self.player.is_done() else ["!disabled"])

    # ---------- Play / Pause / Step / Reset ----------
    def toggle_play(self):
        if self.playing:
            self.pause()
        else:
            if self.player.is_done():       # "Replay": start again from step 0
                self.player.reset()
                self.render_step()
            self.playing = True
            self._update_buttons()
            self._tick()

    def _tick(self):
        """One animation step. root.after calls it again, so the window never freezes."""
        self.after_id = None
        if not self.playing:
            return
        self.player.next()
        if self.player.is_done():
            self.playing = False
        self.render_step()
        if self.playing:
            # Read the speed every tick, so moving the slider works during playback
            self.after_id = self.root.after(self.speed_var.get(), self._tick)

    def pause(self):
        self.playing = False
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self._update_buttons()

    def step_once(self):
        self.pause()
        self.player.next()
        self.render_step()

    def reset_run(self):
        """Stop and go back to step 0 (also used when the graph, algorithm, or start changes)."""
        self.pause()
        self.prepare_run()
        self.render_step()

    # ---------- Custom graph editor (Step 08) ----------
    def open_graph_editor(self):
        """A small window where the user types a graph as text, e.g.  A: B C"""
        self.pause()
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit graph")
        dialog.configure(bg=COLORS["panel"], padx=14, pady=12)
        dialog.transient(self.root)       # stays on top of the main window
        dialog.grab_set()                 # the main window waits until the dialog closes

        ttk.Label(dialog, text="One parent per line:   A: B C", style="Header.TLabel").pack(
            anchor="w")
        ttk.Label(dialog, style="Muted.TLabel", justify="left", text=(
            "Children are separated by spaces or commas. Lines starting with # are comments.\n"
            f"Node names: letters, digits, or _ (at most {MAX_NAME_LENGTH} characters). "
            f"At most {MAX_NODES} nodes.")).pack(anchor="w", pady=(2, 8))

        text_box = tk.Text(dialog, width=56, height=14, font=("Consolas", 11), undo=True,
                           relief="solid", borderwidth=1)
        text_box.pack(fill="both", expand=True)
        text_box.insert("1.0", graph_to_text(self.current_adjacency()))
        text_box.focus_set()

        error_label = ttk.Label(dialog, foreground="#D64545", wraplength=480)
        error_label.pack(anchor="w", pady=(6, 0))

        def load_example():
            text_box.delete("1.0", "end")
            text_box.insert("1.0", CUSTOM_EXAMPLE)
            error_label.configure(text="")

        def apply(_event=None):
            try:
                adjacency = parse_graph_text(text_box.get("1.0", "end"))
            except ValueError as error:
                error_label.configure(text=str(error))   # keep the dialog open
                return "break"
            self.set_custom_graph(adjacency)
            dialog.destroy()
            return "break"

        buttons = ttk.Frame(dialog, style="Panel.TFrame")
        buttons.pack(fill="x", pady=(10, 0))
        ttk.Button(buttons, text="Load example", command=load_example).pack(side="left")
        ttk.Button(buttons, text="Cancel", command=dialog.destroy).pack(side="right")
        ttk.Button(buttons, text="Apply", style="Accent.TButton", command=apply).pack(
            side="right", padx=(0, 6))
        dialog.bind("<Control-Return>", apply)
        dialog.bind("<Escape>", lambda _event: dialog.destroy())
        # Kept so make_gui_screenshots.py can fill in the dialog by code
        self.editor = {"window": dialog, "text": text_box, "error": error_label,
                       "apply": apply}
        return dialog

    def set_custom_graph(self, adjacency):
        """Add (or replace) "Custom graph" in the Graph list, select it, and redraw."""
        self.graphs[CUSTOM_NAME] = adjacency
        self.graph_box.configure(values=list(self.graphs))
        self.graph_var.set(CUSTOM_NAME)
        self._on_graph_change()

    # ---------- Keyboard shortcuts + screenshot (Step 09) ----------
    def _bind_shortcuts(self):
        # Bound on the main window only, so typing in the "Edit graph" dialog is not affected
        self.root.bind("<space>", lambda _event: self.toggle_play())
        self.root.bind("<Right>", lambda _event: self.step_once())
        self.root.bind("<KeyPress-r>", lambda _event: self.reset_run())
        self.root.bind("<KeyPress-R>", lambda _event: self.reset_run())

    def screenshot_name(self):
        """For example  BFS_teacher_tree_6_nodes_step3.png"""
        graph = re.sub(r"[^a-z0-9]+", "_", self.graph_var.get().lower()).strip("_")
        return f"{self.algo_var.get()}_{graph}_step{self.player.index}.png"

    def save_screenshot(self, path=None):
        """Save a picture of the app window (default: screenshots/4_gui/<name>.png)."""
        try:
            from PIL import ImageGrab
        except ImportError:
            messagebox.showerror("Pillow is missing",
                                 "Saving a screenshot needs Pillow. Install it with:\n\n"
                                 "    conda install pillow")
            return None
        path = Path(path) if path else SCREENSHOT_DIR / self.screenshot_name()
        path.parent.mkdir(parents=True, exist_ok=True)
        self.root.update()        # draw everything before taking the picture
        x, y = self.root.winfo_rootx(), self.root.winfo_rooty()
        box = (x, y, x + self.root.winfo_width(), y + self.root.winfo_height())
        ImageGrab.grab(bbox=box).save(path)
        try:
            shown = path.relative_to(PROJECT_DIR)
        except ValueError:
            shown = path
        self.status_var.set(f"Status: Saved {shown}")
        return path

    # ---------- Event handlers ----------
    def _on_graph_change(self):
        # New graph: list its nodes as start choices; the first parent is the default
        nodes = all_nodes(self.current_adjacency())
        self.start_box.configure(values=nodes)
        self.start_var.set(nodes[0])
        self._on_start_change()

    def _on_start_change(self):
        self.pause()
        self.prepare_run()
        self.draw_tree()          # the layout depends on the start node; also renders step 0

    def _on_algorithm_change(self):
        # BFS keeps waiting nodes in a queue (FIFO), DFS in a stack (LIFO)
        if self.algo_var.get() == "BFS":
            self.frontier_title_var.set("Queue (front → back):")
        else:
            self.frontier_title_var.set("Stack (top → bottom):")
        self.reset_run()

    def _on_speed_change(self, _value=None):
        # ttk.Scale gives floats; round to whole milliseconds
        ms = int(float(self.speed_var.get()))
        self.speed_var.set(ms)
        self.speed_label.configure(text=f"{ms} ms / step")


def main():
    enable_high_dpi()
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
