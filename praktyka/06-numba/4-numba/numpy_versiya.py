import numpy as np
from time import perf_counter

W, H = 900, 600
MAX_ITER = 300
XMIN, XMAX = -2.0, 0.6
YMIN, YMAX = -1.2, 1.2

def ryadok(y):
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

def mandelbrot_numpy():
    cx, cy = np.meshgrid(np.linspace(XMIN, XMAX, W, endpoint=False),
                         np.linspace(YMIN, YMAX, H, endpoint=False))
    
    zx = np.zeros((H, W))
    zy = np.zeros((H, W))
    out = np.full((H, W), MAX_ITER, dtype=np.int32)
    aktyvni = np.ones((H, W), dtype=bool)          # точки, що ще не вилетіли
    
    for n in range(MAX_ITER):
        zx_n = zx * zx - zy * zy + cx
        zy_n = 2.0 * zx * zy + cy
        zx = np.where(aktyvni, zx_n, zx)
        zy = np.where(aktyvni, zy_n, zy)
        vyletily = aktyvni & (zx * zx + zy * zy > 4.0)
        out[vyletily] = n + 1
        aktyvni &= ~vyletily
        if not aktyvni.any():
            break
    return out

if __name__ == "__main__":
    base = np.array(poslidovno())
    t = perf_counter()
    r = mandelbrot_numpy()
    print("NumPy:", round(perf_counter() - t, 2), "с")
    print("розбіжних точок:", int((r != base).sum()), "із", base.size)
