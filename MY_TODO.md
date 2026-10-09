# My To-Do List (after Steps 06–13)

Claude did all the code, tests, screenshots, diagrams, and the report layout.
What is left is **my own work**. Do it in this order.

---

## 1. Fill in the report header (5 min)

Open `report/Experiment1_Report.docx`. In the first table, replace the yellow boxes:

- [ ] `[MY CLASS]` (Professional Classes)
- [ ] `[LAB TIME]`
- [ ] `[MY STUDENT NUMBER]`
- [ ] `[LAB LOCATION]` (Location of the experiment)
- [ ] `[MY NAME]`
- [ ] Check "Faculty advisor" — the template says **Yellow Blue**. Change it if your teacher's name is different.

## 2. Write my own text in the report (about 1.5–2 h)

Each yellow box is a place where **I** must write. Copying = 0 points.
After writing, **remove the yellow highlight** (Home → Text Highlight Color → No Color).

| Section | Yellow box | Tip |
|---|---|---|
| 1 Flow chart | describe the flow charts | 3–5 sentences: the loop, and the one box where DFS is different (orange box) |
| 2 Results | analyse the results | Are the orders right? What do the colors and boxes show? |
| 3 Python setup | describe the setup | Mention the C: drive was full, so you installed on D: |
| 4 NumPy | what I learned | 2–4 sentences |
| 5 Principles | explain BFS | Use the BFS trace table (Table 2) |
| 5 Principles | explain DFS | Use the DFS trace table (Table 3) |
| 6 Code | explain the code steps | Use Table 4 (code steps) |
| 7 Compare | my analysis | Use the facts below |
| 9 Summary | summary + experience | Use the "NOTES FOR ME" list, then **delete that list** |

### Facts for section 7 (from `compare.py` — write the analysis in your own words)

- Teacher tree: both BFS and DFS take 6 steps, and both have max queue/stack size 3.
- 15-node tree: BFS max queue = **8**, DFS max stack = **4** → BFS needs about twice the memory.
- 15-node tree, node C (1 step from A): BFS finds it at visit **3**, DFS at visit **9**.
- 15-node tree, node H (deepest, left): DFS finds it at visit **4**, BFS at visit **8**.
- Graph with cycle: the visited check stops repeats; BFS max queue = 4 because D waits in the queue twice.
- City map: CAN (1 hop from WUH) → BFS visit 4, DFS visit 8. TSN (2 hops, left) → DFS visit 3, BFS visit 5.
- Both visit every reachable node once → steps = number of nodes, time O(V + E).

## 3. Check things by hand (20 min)

- [ ] Run the GUI: `D:\anaconda3\python.exe code\gui_app.py`. Try every graph with BFS and DFS, slow and fast.
      If you want other colors/layout, ask Claude.
- [ ] Click **Edit graph...** → **Load example** → **Apply**, or type your own graph (e.g. your home town map).
      This ticks "I tested my own graph" in the roadmap.
- [ ] Open `screenshots/4_gui/` and `diagrams/` and check every picture is clear.
- [ ] Optional: in PyCharm, take one screenshot of `compare.py` output inside PyCharm, if your teacher prefers PyCharm screenshots
      (a console screenshot is already in `screenshots/3_search/03_compare_output.png`).

## 4. Final read and submit (15 min)

- [ ] Search the report for `[MY` and `NOTES FOR ME` — nothing should be left.
- [ ] Read the whole report once (39 pages now; it gets a bit longer with your text).
- [ ] Ask the teacher: `.docx` or PDF? For PDF: Word → File → Save As → PDF.
- [ ] Tick the last boxes in `Docs/Experiment1_Roadmap.md` (Phase 12, 13), then submit.

---

### Good to know

- The report was built by a script that is **not** in the project, so nothing will overwrite your text.
- Two small tools were installed into Anaconda for building/checking the report: `python-docx` and `pymupdf`.
- All 71 tests pass: `D:\anaconda3\python.exe -m unittest discover -s tests -v`
