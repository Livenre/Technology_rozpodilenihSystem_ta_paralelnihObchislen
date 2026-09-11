import os, platform, sys
from time import perf_counter
import cProfile
import pstats

"""З кодом мені допомогав ШІ"""

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


def zberegty_pgm(dani, shlyah="mandelbrot.pgm"):
    with open(shlyah, "wb") as f:
        f.write(b"P5\n%d %d\n255\n" % (W, H))
        f.write(bytes(min(255, v * 255 // MAX_ITER) for r in dani for v in r))

def zamir(fn, prohoniv=3, *a):
    chasy = []
    for _ in range(prohoniv):
        t = perf_counter()
        r = fn(*a)
        chasy.append(perf_counter() - t)
    return min(chasy), chasy, r



if __name__ == "__main__":
    print("Виконую 3 прогони для заміру часу...\n")
    min_time, all_times, base = zamir(poslidovno, 3)
    
    rozkyd = (max(all_times) - min(all_times)) / min_time * 100
    
    runs_text = (
        f"Прогін перший: {all_times[0]:.3f} с\n"
        f"Прогін другий: {all_times[1]:.3f} с\n"
        f"Прогін третій: {all_times[2]:.3f} с"
    )
    
    print(runs_text)
    print(f"Мінімум із трьох прогонів: {min_time:.3f} с")
    print(f"Розкид між прогонами: {rozkyd:.1f} %")

    print("\nЗберігаю картинку...")
    t_start = perf_counter()
    zberegty_pgm(base, "mandelbrot.pgm")
    t_zapys = perf_counter() - t_start
    
    chastka_zapysu = (t_zapys / (min_time + t_zapys)) * 100
    print(f"Послідовна частка (запис): {t_zapys:.3f} с = {chastka_zapysu:.1f} %")

    print("\nЗапускаю cProfile (профілювання)...")
    profiler = cProfile.Profile()
    profiler.enable()
    
    r = poslidovno()
    
    profiler.disable()
    
    assert r == base, "результат розійшовся з послідовним"
    print("assert пройдено: результат збігається.")
    
    print("\n-_-_- cProfile -_-_-")
    stats_console = pstats.Stats(profiler)
    stats_console.sort_stats('tottime').print_stats(10)

    with open("profil.txt", "w", encoding="utf-8") as f:
        f.write("Деталі прогонів:\n")
        f.write(runs_text + "\n")
        f.write(f"Мінімум із трьох прогонів: {min_time:.3f} с\n")
        f.write(f"Розкид між прогонами: {rozkyd:.1f} %\n")
        f.write(f"Послідовна частка (запис): {t_zapys:.3f} с = {chastka_zapysu:.1f} %\n")
        
        f.write("\n-_-_- cProfile -_-_-\n")

        stats_file = pstats.Stats(profiler, stream=f)
        stats_file.sort_stats('tottime').print_stats()

