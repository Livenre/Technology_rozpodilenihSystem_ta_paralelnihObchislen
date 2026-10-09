import os, platform, sys
from time import perf_counter
import cProfile
import pstats
import numpy as np
from numba import njit, prange

W, H = 900, 600
MAX_ITER = 300
XMIN, XMAX = -2.0, 0.6
YMIN, YMAX = -1.2, 1.2

def ryadok(y):
    """Один рядок — незалежна одиниця роботи."""
    cy = YMIN + (YMAX - YMIN) * y / H
    out = []
    for x in range(W):
        cx = XMIN + (XMAX - XMIN) * x / W
        zx = zy = 0.0
        n = 0
        while zx * zx + zy * zy <= 4.0 and n < MAX_ITER:
            zx, zy = zx * zx - zy * zy + cx, 2.0 * zx * zy + cy
            n += 1
        out.append(n)
    return out

def poslidovno():
    all_rows = []
    for y in range(H):
        row = ryadok(y)
        all_rows.append(row)
    return all_rows

def zamir(fn, prohoniv=3, *a):
    chasy = []
    for _ in range(prohoniv):
        t = perf_counter()
        r = fn(*a)
        chasy.append(perf_counter() - t)
    return min(chasy), chasy, r

@njit
def mandelbrot_numba(W, H, MAX_ITER, XMIN, XMAX, YMIN, YMAX):
    out = np.empty((H, W), dtype=np.int32)
    for y in range(H):
        cy = YMIN + (YMAX - YMIN) * y / H
        for x in range(W):
            cx = XMIN + (XMAX - XMIN) * x / W
            zx = 0.0
            zy = 0.0
            n = 0
            while zx * zx + zy * zy <= 4.0 and n < MAX_ITER:
                zx, zy = zx * zx - zy * zy + cx, 2.0 * zx * zy + cy
                n += 1
            out[y, x] = n
    return out

@njit(parallel=True)
def mandelbrot_prange(W, H, MAX_ITER, XMIN, XMAX, YMIN, YMAX):
    out = np.empty((H, W), dtype=np.int32)
    for y in prange(H):                  # ТУТ БУЛО range, СТАЛО prange
        cy = YMIN + (YMAX - YMIN) * y / H
        for x in range(W):
            cx = XMIN + (XMAX - XMIN) * x / W
            zx = 0.0
            zy = 0.0
            n = 0
            while zx * zx + zy * zy <= 4.0 and n < MAX_ITER:
                zx, zy = zx * zx - zy * zy + cx, 2.0 * zx * zy + cy
                n += 1
            out[y, x] = n
    return out


if __name__ == "__main__":
    t_base, chasy, base = zamir(poslidovno, 1)       # чистий Python: один прогін, він довгий
    base = np.array(base)
    ARGS = (W, H, MAX_ITER, XMIN, XMAX, YMIN, YMAX)

    t0 = perf_counter()
    mandelbrot_numba(*ARGS)                          # перший виклик = компіляція
    print("компіляція @njit:", round(perf_counter() - t0, 2), "с")

    t, chasy, r = zamir(mandelbrot_numba, 3, *ARGS)
    assert np.array_equal(r, base), "результат розійшовся з еталоном"
    print("@njit", [round(c, 4) for c in chasy], "прискорення", round(t_base / t))

    print("\n")

    t0 = perf_counter()
    mandelbrot_prange(*ARGS)                          # перша компіляція prange
    print("компіляція prange:", round(perf_counter() - t0, 2), "с")

    t, chasy, r = zamir(mandelbrot_prange, 3, *ARGS)
    assert np.array_equal(r, base), "результат prange розійшовся з еталоном"
    print("prange", [round(c, 4) for c in chasy], "прискорення", round(t_base / t))
    
