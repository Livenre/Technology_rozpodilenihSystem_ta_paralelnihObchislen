import os
import time
from time import perf_counter, process_time
from concurrent.futures import ThreadPoolExecutor

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

#Новий
def potokamy(n):
    with ThreadPoolExecutor(max_workers=n) as ex:
        return list(ex.map(ryadok, range(H)))

#Новий
def navantazhennya(fn, *a):
    c0, t0 = process_time(), perf_counter()
    fn(*a)
    return (process_time() - c0) / (perf_counter() - t0)

#Новий
def zapyt(nomer):
    time.sleep(0.5)          # «запит у мережу»: процесор вільний
    return nomer

#Новий
def ochikuvannya_poslidovno():
    return [zapyt(i) for i in range(32)]

#Новий
def ochikuvannya_potokamy(n):
    with ThreadPoolExecutor(max_workers=n) as ex:
        return list(ex.map(zapyt, range(32)))


if __name__ == "__main__":
    print("-_-_- Крок 1. Потокова версія Мандельброта -_-_-")
    t_base, chasy, base = zamir(poslidovno, 3)
    print("послідовно", [round(c, 2) for c in chasy], "мінімум", round(t_base, 2))

    # os.cpu_count() для твоего Ryzen 5 3600 выдаст 12
    for n in (2, 4, 8, os.cpu_count()):
        t, chasy, r = zamir(potokamy, 3, n)
        assert r == base, "результат розійшовся з послідовним"
        print("потоків", n, [round(c, 2) for c in chasy],
              "мінімум", round(t, 2), "прискорення", round(t_base / t, 2))

    print("\n-_-_- Крок 2. Скільки ядер реально працювало -_-_-")
    print("процесорний / настінний, 8 потоків:", round(navantazhennya(potokamy, 8), 2))

    print("\n-_-_- Крок 3. Задача з очікуванням -_-_-")
    t0 = perf_counter()
    base_o = ochikuvannya_poslidovno()          # один прогін: 16 с, розкиду тут немає
    t_base_o = perf_counter() - t0
    print("очікування послідовно", round(t_base_o, 2))

    for n in (2, 4, 8, 16, 32):
        t, chasy, r = zamir(ochikuvannya_potokamy, 3, n)
        assert r == base_o, "результат очікування розійшовся"
        print("очікування, потоків", n, [round(c, 2) for c in chasy],
              "прискорення", round(t_base_o / t, 1))
