import matplotlib.pyplot as plt

x_potoky_obch = [1, 2, 4, 8, 12]
x_potoky_ochik = [1, 2, 4, 8, 16, 32]

y_obchyslennya = [1.0, 1.0, 1.03, 1.03, 1.03]
y_ochikuvannya = [1.0, 2.0, 4.0, 8.0, 16.0, 31.7]

plt.plot(x_potoky_obch, y_obchyslennya, "o-", label="Обчислення")
plt.plot(x_potoky_ochik, y_ochikuvannya, "s-", label="Очікування")
plt.xlabel("Кількість потоків")
plt.ylabel("Прискорення, разів")
plt.legend()
plt.grid(True)
plt.savefig("grafik.png", dpi=120)
