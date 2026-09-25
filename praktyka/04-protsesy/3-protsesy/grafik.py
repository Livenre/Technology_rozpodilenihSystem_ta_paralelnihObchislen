import matplotlib.pyplot as plt

n = [1, 2, 4, 6, 8, 12]
pryskorennya = [1.03, 1.91, 3.26, 4.17, 4.46, 4.17]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))

a1.plot(n, pryskorennya, "o-", label="Виміряне")
a1.plot(n, n, "--", color="gray", label="Ідеал ×N")
a1.set_xlabel("Процесів");
a1.set_ylabel("Прискорення, разів")
a1.legend();
a1.grid(True)

a2.plot(n, [s / k * 100 for s, k in zip(pryskorennya, n)], "s-", color="tab:orange")
a2.set_xlabel("Процесів");
a2.set_ylabel("Ефективність, %")
a2.set_ylim(0, 110);
a2.grid(True)

fig.tight_layout()
fig.savefig("grafik.png", dpi=110)
