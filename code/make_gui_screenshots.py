# -*- coding: utf-8 -*-
r"""
Experiment 1 - Make the GUI screenshots for the report automatically.

It opens the app, chooses the settings by code, steps by code, saves each picture
into screenshots/4_gui/, and closes the app. Do not move the mouse over the window
or cover it while it runs (about 10 seconds): the picture is taken from the screen.

Run:  D:\anaconda3\python.exe code\make_gui_screenshots.py
"""
import tkinter as tk

import gui_app
from sample_graphs import CUSTOM_EXAMPLE, parse_graph_text

TEACHER = "Teacher tree (6 nodes)"
WAIT_MS = 600     # time for Windows to paint the window before the picture is taken


def choose(app, graph, algorithm, steps=None):
    """Select a graph and algorithm, then step forward (steps=None means to the end)."""
    app.graph_var.set(graph)
    app._on_graph_change()
    app.algo_var.set(algorithm)
    app._on_algorithm_change()
    if steps is None:
        while not app.player.is_done():
            app.step_once()
    else:
        for _ in range(steps):
            app.step_once()


def grab_window(window, path):
    from PIL import ImageGrab
    window.update()
    x, y = window.winfo_rootx(), window.winfo_rooty()
    ImageGrab.grab(bbox=(x, y, x + window.winfo_width(), y + window.winfo_height())).save(path)


def main():
    gui_app.enable_high_dpi()
    root = tk.Tk()
    app = gui_app.App(root)
    root.geometry("1200x750+40+40")
    root.attributes("-topmost", True)     # keep the app in front of other windows
    out = gui_app.SCREENSHOT_DIR
    out.mkdir(parents=True, exist_ok=True)

    def open_editor():
        choose(app, TEACHER, "BFS", steps=0)
        dialog = app.open_graph_editor()
        dialog.geometry("+330+160")
        dialog.attributes("-topmost", True)
        app.editor["text"].delete("1.0", "end")
        app.editor["text"].insert("1.0", CUSTOM_EXAMPLE)
        return dialog

    def close_editor_and_use_custom():
        app.editor["window"].destroy()
        app.set_custom_graph(parse_graph_text(CUSTOM_EXAMPLE))
        choose(app, gui_app.CUSTOM_NAME, "BFS", steps=4)

    # (file name, what to do before the picture). Each picture shows the whole window.
    shots = [
        ("01_start.png", lambda: choose(app, TEACHER, "BFS", steps=0)),
        ("02_bfs_middle.png", lambda: choose(app, TEACHER, "BFS", steps=3)),
        ("03_bfs_done.png", lambda: choose(app, TEACHER, "BFS")),
        ("04_dfs_middle.png", lambda: choose(app, TEACHER, "DFS", steps=3)),
        ("05_dfs_done.png", lambda: choose(app, TEACHER, "DFS")),
        ("06_bigger_tree_bfs.png", lambda: choose(app, "Bigger tree (15 nodes)", "BFS")),
        ("07_cycle_graph_dfs.png", lambda: choose(app, "Graph with cycle", "DFS")),
        ("08_custom_graph.png", close_editor_and_use_custom),
    ]

    def take(index=0):
        if index == len(shots):
            # The edit dialog itself, for the report
            dialog = open_editor()
            root.after(WAIT_MS, lambda: finish(dialog))
            return
        name, action = shots[index]
        if name == "08_custom_graph.png":
            open_editor()        # the custom graph is entered through the dialog
        action()
        root.after(WAIT_MS, lambda: (grab_window(root, out / name),
                                     print("saved", out / name),
                                     take(index + 1)))

    def finish(dialog):
        grab_window(dialog, out / "09_edit_graph_dialog.png")
        print("saved", out / "09_edit_graph_dialog.png")
        root.destroy()

    root.after(WAIT_MS, take)
    root.mainloop()


if __name__ == "__main__":
    main()
