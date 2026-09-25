import os
from time import perf_counter
from concurrent.futures import ProcessPoolExecutor

# З кодом допомогав ШІ

W, H = 900, 600
MAX_ITER = 300
XMIN, XMAX = -2.0, 0.6
YMIN, YMAX = -1.2, 1.2

def ryadok(y):
    cy = YMIN + (YMAX - YMIN) * y / H
    out = []
    for x in range(W):
        cx = XMIN + (XMAX - XMIN) * x / W
        zx, zy = 0.0, 0.0
        n = 0
        while zx * zx + zy * zy <= 4.0 and n < MAX_ITER:
            zx, zy = zx * zx - zy * zy + cx, 2.0 * zx * zy + cy
            n += 1
        out.append(n)
    return out

def poslidovno():
    return [ryadok(y) for y in range(H)]

def zamir(fn, prohoniv=3, *a):
    chasy = []
    for _ in range(prohoniv):
        t = perf_counter()
        r = fn(*a)
        chasy.append(perf_counter() - t)
    return min(chasy), chasy, r

def protsesamy(n):
    with ProcessPoolExecutor(max_workers=n) as ex:
        return list(ex.map(ryadok, range(H), chunksize=8))

def porozhniy_pul(n):
    with ProcessPoolExecutor(max_workers=n) as ex:
        list(ex.map(abs, range(n)))

if __name__ == "__main__":
    print("-_-_- Крок 1. Процесна версія Мандельброта -_-_-")
    t_base, chasy, base = zamir(poslidovno, 3)
    print("послідовно", [round(c, 2) for c in chasy], "мінімум", round(t_base, 2))

    for n in (1, 2, 4, 6, 8, os.cpu_count()):
        t, chasy, r = zamir(protsesamy, 3, n)
        assert r == base, "результат розійшовся з послідовним"
        s = t_base / t
        print("процесів", n, [round(c, 2) for c in chasy], "мінімум", round(t, 2),
              "прискорення", round(s, 2), "ефективність", round(s / n * 100), "%")

    print("\n-_-_- Крок 3. Скільки коштує сам пул -_-_-")
    for n in (2, os.cpu_count()):
        t, chasy, _ = zamir(porozhniy_pul, 3, n)
        print("порожній пул,", n, "процесів:", round(t, 3), "с")
