# -*- coding: utf-8 -*-
"""
Experiment 1 - Part 1: NumPy syntax learning
Topics follow Numpy.pptx. Examples come from the slides, fixed for NumPy 2.
Lines marked "Slide fix" show what was changed from the slide code.

Run all sections:      python code/numpy_demo.py
Run one section (1-10): python code/numpy_demo.py 3
Screenshot the output into screenshots/2_numpy/ (the code goes into the report as text).
"""
import sys

import numpy as np


def show(label, *values):
    """Print an expression and its result(s).

    A short result goes on the same line, so one section fits in one screenshot.
    Several results are split by " | " or printed one per line. They are passed
    one by one (not as a tuple), because printing a tuple shows noisy text like
    np.int64(5), and a real tuple such as a shape (3, 4) must stay as it is.
    """
    items = [str(value) for value in values]
    one_line = " | ".join(items)
    if "\n" not in one_line and len(label) + len(one_line) <= 90:
        print(f"{label} -> {one_line}")
    else:
        print(f"{label} ->")
        print("\n".join(items))


# ---------- 1. Create arrays ----------
# np.array, zeros, ones, empty, arange, linspace, logspace, full, fromfunction
def section_1_create_arrays():
    show("np.array([1, 2, 3])", np.array([1, 2, 3]))
    show("np.array([[1, 2, 3], [4, 5, 6]])", np.array([[1, 2, 3], [4, 5, 6]]))
    show("np.array([1, 2, 3, 4], float)", np.array([1, 2, 3, 4], float))
    show("np.zeros((3, 4))", np.zeros((3, 4)))
    show("np.ones((2, 3), dtype='float64')", np.ones((2, 3), dtype="float64"))
    # empty() only reserves memory, so the values are whatever was there before.
    # Slide fix: np.int was removed from NumPy, use int.
    show("np.empty((2, 3), int)", np.empty((2, 3), int))
    show("np.arange(1, 20, 5)", np.arange(1, 20, 5))
    show("np.arange(0, 1, 0.1)", np.arange(0, 1, 0.1))
    show("np.linspace(0, 1, 10)", np.linspace(0, 1, 10))
    show("np.linspace(0, 1, 10, endpoint=False)", np.linspace(0, 1, 10, endpoint=False))
    show("np.logspace(0, 2, 5)", np.logspace(0, 2, 5))
    show("np.full(4, np.pi)", np.full(4, np.pi))

    def func(i):
        return i % 4 + 1

    # fromfunction calls func with the index of every element.
    show("np.fromfunction(func, (10,))   # func(i) = i % 4 + 1",
         np.fromfunction(func, (10,)))


# ---------- 2. Array properties ----------
# shape, size, dtype, ndim, reshape
def section_2_properties():
    data = np.arange(12).reshape(3, 4)
    show("data = np.arange(12).reshape(3, 4)", data)
    show("type(data)", type(data))
    show("data.shape", data.shape)
    show("data.size", data.size)
    # The slide shows int32: old NumPy on Windows used 32-bit int, NumPy 2 uses 64-bit.
    show("data.dtype", data.dtype)
    show("data.ndim", data.ndim)

    a = np.array([1, 2, 3, 4], dtype=float)
    show("a = np.array([1, 2, 3, 4], dtype=float); a.dtype", a.dtype)
    # Slide fix: a.leshape -> a.reshape
    show("a.reshape((2, 2))", a.reshape((2, 2)))
    # -1 means "work out this size for me" (here 4 / 1 = 4 rows).
    show("a.reshape(-1, 1)", a.reshape(-1, 1))


# ---------- 3. Slicing ----------
# a[3:5], a[::-1], 2D slicing, shared memory vs copy
def section_3_slicing():
    a = np.arange(10)
    show("a = np.arange(10)", a)
    show("a[5], a[3:5], a[:5], a[:-1]", a[5], a[3:5], a[:5], a[:-1])
    show("a[1:-1:2], a[::-1], a[5:1:-2]", a[1:-1:2], a[::-1], a[5:1:-2])

    a[2:4] = 100, 101
    show("a[2:4] = 100, 101; a", a)

    # A slice is a VIEW: b and a share the same memory, so changing b changes a.
    b = a[3:7]
    b[2] = -10
    show("b = a[3:7]; b[2] = -10; a", a)

    # A list index makes a COPY: changing b does not change a.
    a = np.arange(10)
    b = a[[3, 3, -3, 8]]
    b[2] = 100
    show("a = np.arange(10); b = a[[3, 3, -3, 8]]; b[2] = 100; b, a", b, a)

    m = np.arange(0, 60, 10).reshape(-1, 1) + np.arange(0, 6)
    show("m = np.arange(0, 60, 10).reshape(-1, 1) + np.arange(0, 6)", m)
    show("m[0, 3:5]", m[0, 3:5])
    show("m[4:, 4:]", m[4:, 4:])
    show("m[2::2, ::2]", m[2::2, ::2])
    # Integer lists and Boolean arrays also make copies (slide 21).
    show("m[[0, 2, 5], [1, 3, 5]]", m[[0, 2, 5], [1, 3, 5]])
    show("m[m % 20 == 0]", m[m % 20 == 0])


# ---------- 4. Struct array ----------
# np.dtype with name / age / weight
def section_4_struct_array():
    # Slide fix: 'S30' stores bytes (prints b'Zhang'), 'U30' stores normal text.
    persontype = np.dtype({
        "names": ["name", "age", "weight"],
        "formats": ["U30", "i", "f"],
    })
    show("persontype", persontype)

    # Slide fix: np. Array -> np.array, and "." before dtype -> ","
    a = np.array([("Zhang", 32, 75.5), ("Wang", 24, 65.2)], dtype=persontype)
    show("a", a)
    # Slide fix: print a[0] -> print(a[0])
    show("a[0]", a[0])
    show("a['name']", a["name"])
    show("a[1]['age']", a[1]["age"])
    show("a['weight'].mean()", a["weight"].mean())


# ---------- 5. ufunc ----------
# np.sin, add, subtract, multiply, comparisons, frompyfunc
def section_5_ufunc():
    x = np.linspace(0, 2 * np.pi, 10)
    # The last value prints as -0. : sin(2*pi) is really about -2.4e-16 (rounding error).
    with np.printoptions(precision=3, suppress=True):
        show("np.sin(np.linspace(0, 2 * np.pi, 10))", np.sin(x))

    a = np.arange(0, 4)
    b = np.arange(1, 5)
    show("a = np.arange(0, 4); b = np.arange(1, 5)", a, b)
    show("np.add(a, b)  (same as a + b)", np.add(a, b))
    show("np.subtract(a, b)", np.subtract(a, b))
    show("np.multiply(a, b)", np.multiply(a, b))
    # In Python 3 / NumPy 2, divide always gives floats (the slide is from Python 2).
    show("np.divide(a, b)", np.divide(a, b))
    show("np.power(a, b)", np.power(a, b))

    show("np.array([1, 2, 3]) < np.array([3, 2, 1])",
         np.array([1, 2, 3]) < np.array([3, 2, 1]))
    show("np.less_equal([1, 2, 3], [3, 2, 1])", np.less_equal([1, 2, 3], [3, 2, 1]))

    def num_judge(x, a):
        """Return 0 if x is a multiple of 3 or 5, otherwise return a."""
        if x % 3 == 0:
            r = 0
        elif x % 5 == 0:
            r = 0
        else:
            r = a
        return r

    # frompyfunc(func, nin, nout) turns a normal Python function into a ufunc.
    numb_judge = np.frompyfunc(num_judge, 2, 1)
    x = np.linspace(0, 10, 11)
    y = numb_judge(x, 2)
    show("numb_judge = np.frompyfunc(num_judge, 2, 1); numb_judge(x, 2)", y)
    # Slide fix: y.astype(np.int) -> y.astype(int)
    show("y.astype(int)", y.astype(int))


# ---------- 6. Broadcasting ----------
# arange(...).reshape(-1, 1) + arange(...), ogrid
def section_6_broadcasting():
    a = np.arange(0, 60, 10).reshape(-1, 1)
    b = np.arange(0, 5)
    show("a = np.arange(0, 60, 10).reshape(-1, 1)   (shape (6, 1))", a)
    show("b = np.arange(0, 5)   (shape (5,))", b)
    # a is stretched to 5 columns and b to 6 rows, so the result is 6 x 5.
    c = a + b
    show("c = a + b", c)
    show("c.shape", c.shape)

    x, y = np.ogrid[:5, :5]
    show("x, y = np.ogrid[:5, :5]; x", x)
    show("y", y)
    show("x + y", x + y)

    a = np.arange(4)
    # Slide fix: a.Rishape -> a.reshape. None adds a new axis of size 1.
    show("a[None, :]   (same as a.reshape(1, -1))", a[None, :])
    show("a[:, None]   (same as a.reshape(-1, 1))", a[:, None])


# ---------- 7. Random numbers ----------
# rand, randint, normal, poisson, seed
def section_7_random():
    # Same seed -> same "random" numbers every run, so the output can be checked.
    np.random.seed(42)
    with np.printoptions(precision=2):
        show("np.random.rand(4, 3)", np.random.rand(4, 3))
        show("np.random.randint(0, 10, size=(2, 5))", np.random.randint(0, 10, size=(2, 5)))
        show("np.random.normal(0, 1, 5)", np.random.normal(0, 1, 5))
        show("np.random.randn(5)", np.random.randn(5))
        show("np.random.uniform(1, 3, 5)", np.random.uniform(1, 3, 5))
        show("np.random.poisson(2.0, (4, 3))", np.random.poisson(2.0, (4, 3)))
        show("np.random.choice([10, 20, 30, 40], 3)", np.random.choice([10, 20, 30, 40], 3))
        a = np.arange(10)
        np.random.shuffle(a)
        show("a = np.arange(10); np.random.shuffle(a); a", a)


# ---------- 8. Statistics ----------
# sum, mean, var, std, sort, percentile, unique, bincount, histogram
def section_8_statistics():
    np.random.seed(42)
    a = np.random.randint(0, 10, size=(4, 5))
    show("np.random.seed(42); a = np.random.randint(0, 10, size=(4, 5))", a)
    show("np.sum(a)", np.sum(a))
    show("np.sum(a, axis=1), np.sum(a, axis=0)", np.sum(a, axis=1), np.sum(a, axis=0))
    show("np.sum(a, 1, keepdims=True)", np.sum(a, 1, keepdims=True))
    show("np.mean(a), np.var(a), np.std(a)", np.mean(a), np.var(a), round(np.std(a), 4))
    show("np.min(a), np.max(a), np.ptp(a), np.argmin(a), np.median(a)",
         np.min(a), np.max(a), np.ptp(a), np.argmin(a), np.median(a))
    show("np.sort(a)   (sort each row)", np.sort(a))
    show("np.sort(a, axis=0)   (sort each column)", np.sort(a, axis=0))
    show("np.argsort([30, 10, 20])", np.argsort([30, 10, 20]))

    b = np.array([1, 3, 5, 7])
    c = np.array([2, 4, 6])
    # Slide fix: maxinum -> maximum
    show("np.maximum(b[None, :], c[:, None])", np.maximum(b[None, :], c[:, None]))

    r = np.abs(np.random.randn(100000))
    with np.printoptions(precision=3):
        show("np.percentile(abs(randn(100000)), [68.3, 95.4, 99.7])",
             np.percentile(r, [68.3, 95.4, 99.7]))

    np.random.seed(42)
    a = np.random.randint(0, 8, 10)
    show("np.random.seed(42); a = np.random.randint(0, 8, 10)", a)
    show("np.unique(a)", np.unique(a))
    show("np.unique(a, return_index=True)", *np.unique(a, return_index=True))
    show("np.unique(a, return_inverse=True)", *np.unique(a, return_inverse=True))
    # bincount: result[i] = how many times i appears in a.
    show("np.bincount(a)", np.bincount(a))
    x = np.array([0, 1, 2, 2, 1, 1, 0])
    w = np.array([0.1, 0.3, 0.2, 0.4, 0.5, 0.8, 1.2])
    show("np.bincount(x, w)   (sum of weights per value)", np.bincount(x, w))

    d = np.random.rand(100)
    show("np.histogram(np.random.rand(100), bins=5, range=(0, 1))",
         *np.histogram(d, bins=5, range=(0, 1)))


# ---------- 9. Join and split ----------
# vstack, hstack, column_stack, split
def section_9_join_split():
    a = np.arange(3)
    b = np.arange(10, 13)
    show("a = np.arange(3); b = np.arange(10, 13)", a, b)
    show("np.vstack((a, b))   (one on top of the other)", np.vstack((a, b)))
    show("np.hstack((a, b))   (side by side)", np.hstack((a, b)))
    show("np.column_stack((a, b))   (each array becomes a column)", np.column_stack((a, b)))

    a = np.array([6, 3, 7, 4, 6, 9, 2, 6, 7, 4, 3, 7])
    # Slide fix: the slide names this list b but then uses idx, and misses a ")".
    idx = np.array([1, 3, 6, 9, 10])
    show("a", a)
    show("np.split(a, [1, 3, 6, 9, 10])   (cut at these positions)", np.split(a, idx))
    show("np.split(a, 2)   (cut into 2 equal parts)", np.split(a, 2))


# ---------- 10. Polynomials ----------
# poly1d, deriv, integ, roots, polyfit
def section_10_polynomials():
    # Coefficients go from the highest power down: x^3 + 0x^2 - 2x + 1
    p = np.poly1d(np.array([1.0, 0, -2, 1]))
    show("p = np.poly1d([1.0, 0, -2, 1]); print(p)", p)
    # Slide fix: print type(p) -> print(type(p))
    show("type(p)", type(p))
    show("p(np.linspace(0, 1, 5))", p(np.linspace(0, 1, 5)))
    show("p + [-2, 1]", repr(p + [-2, 1]))
    show("p * p", repr(p * p))
    quotient, remainder = p / [1, 1]
    show("quotient, remainder = p / [1, 1]", repr(quotient), repr(remainder))
    show("p.deriv()", repr(p.deriv()))
    show("p.integ()", repr(p.integ()))
    show("np.roots(p)", np.roots(p))

    # polyfit finds the best polynomial for some points. Points taken from p
    # give back p's own coefficients, which proves the fit works.
    x = np.linspace(-2, 2, 9)
    with np.printoptions(precision=4, suppress=True):
        show("np.polyfit(x, p(x), 3)   (x = np.linspace(-2, 2, 9))", np.polyfit(x, p(x), 3))
    # poly() goes the other way: from roots back to coefficients.
    # round() hides tiny rounding errors; "+ 0" turns -0. into 0.
    show("np.poly(np.roots(p))", np.round(np.poly(np.roots(p)), 4) + 0)


# ---------- Main ----------
SECTIONS = [
    ("Create arrays", section_1_create_arrays),
    ("Array properties", section_2_properties),
    ("Slicing", section_3_slicing),
    ("Struct array", section_4_struct_array),
    ("ufunc", section_5_ufunc),
    ("Broadcasting", section_6_broadcasting),
    ("Random numbers", section_7_random),
    ("Statistics", section_8_statistics),
    ("Join and split", section_9_join_split),
    ("Polynomials", section_10_polynomials),
]


def run_section(number):
    title, func = SECTIONS[number - 1]
    print(f"=== {number}. {title} ===")
    func()
    print()


def main():
    if len(sys.argv) == 1:
        for number in range(1, len(SECTIONS) + 1):
            run_section(number)
        return 0

    arg = sys.argv[1]
    if not arg.isdigit() or not 1 <= int(arg) <= len(SECTIONS):
        print(f"Usage: python numpy_demo.py [1-{len(SECTIONS)}]")
        return 1
    run_section(int(arg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
