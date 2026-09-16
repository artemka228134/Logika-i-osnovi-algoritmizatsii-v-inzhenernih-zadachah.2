import os
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Output directory for images
output_dir = r"c:\Users\maxim\source\repos\alg2lr\alg2lr"

# ==============================================================================
# 1. ЗАДАНИЕ 1: МАТРИЦЫ
# ==============================================================================
matrix_sizes = [100, 200, 400, 1000, 2000, 4000, 10000]
mult_times = [0.0000, 0.0040, 0.0330, 0.6840, 6.1870, 98.3070, 2853.5750]
init_times = [0.0000, 0.0000, 0.0020, 0.0160, 0.0620, 0.2390, 1.5320]

# Теоретическая кривая: C * N^3
# Подберем C по точке N=2000: C = 6.187 / (2000^3) = 7.73375e-10
c_factor = 6.1870 / (2000**3)
theory_n = np.linspace(100, 10500, 300)
theory_time = c_factor * (theory_n ** 3)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Линейный график
ax1.plot(theory_n, theory_time, '--', color='gray', label=f'Теория $O(N^3)$ (C={c_factor:.2e})', alpha=0.8)
ax1.plot(matrix_sizes, mult_times, 'ro-', linewidth=2, markersize=7, label='Умножение матриц (C=A*B)')
ax1.plot(matrix_sizes, init_times, 'bs--', linewidth=1.5, markersize=5, label='Инициализация (рандом)')
ax1.set_title('Задание 1: Время работы от размера матрицы N\n(Линейный масштаб, до N=10000)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Размерность матрицы N (NxN)', fontsize=11)
ax1.set_ylabel('Время выполнения (секунды)', fontsize=11)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(fontsize=10)

# Логарифмический график (log-log)
ax2.loglog(theory_n, theory_time, '--', color='gray', label=r'Теория $\propto N^3$ (наклон = 3)', alpha=0.8)
ax2.loglog(matrix_sizes[1:], mult_times[1:], 'ro-', linewidth=2, markersize=7, label='Умножение матриц')
ax2.loglog(matrix_sizes[2:], init_times[2:], 'bs--', linewidth=1.5, markersize=5, label=r'Инициализация $\propto N^2$')
ax2.set_title('Задание 1: Зависимость в масштабе Log-Log\n(Проверка кубической сложности)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Размерность матрицы N (log)', fontsize=11)
ax2.set_ylabel('Время выполнения, сек. (log)', fontsize=11)
ax2.grid(True, which="both", ls=":", alpha=0.6)
ax2.legend(fontsize=10)

plt.tight_layout()
matrix_plot_path = os.path.join(output_dir, 'matrix_benchmark.png')
plt.savefig(matrix_plot_path, dpi=200)
plt.close()
print(f"Saved: {matrix_plot_path}")


# ==============================================================================
# 2. ЗАДАНИЕ 2: СОРТИРОВКИ
# ==============================================================================
sort_sizes = [10000, 25000, 50000, 100000]

data = {
    'Случайный массив': {
        'Shell': [0.002, 0.009, 0.035, 0.134],
        'qs':    [0.000, 0.001, 0.002, 0.005],
        'qsort': [0.001, 0.002, 0.004, 0.008]
    },
    'Возрастающая последовательность': {
        'Shell': [0.000, 0.000, 0.000, 0.000],
        'qs':    [0.000, 0.000, 0.001, 0.001],
        'qsort': [0.000, 0.001, 0.001, 0.003]
    },
    'Убывающая последовательность': {
        'Shell': [0.003, 0.018, 0.092, 0.270],
        'qs':    [0.000, 0.000, 0.000, 0.000],
        'qsort': [0.000, 0.001, 0.002, 0.003]
    },
    '1/2 возрастает, 1/2 убывает': {
        'Shell': [0.001, 0.004, 0.017, 0.066],
        'qs':    [0.000, 0.001, 0.000, 0.001],
        'qsort': [0.000, 0.000, 0.001, 0.003]
    }
}

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for idx, (title, series) in enumerate(data.items()):
    ax = axes[idx]
    ax.plot(sort_sizes, series['Shell'], 'r^-', linewidth=1.8, markersize=6, label='Сортировка Шелла')
    ax.plot(sort_sizes, series['qs'],    'go-', linewidth=1.8, markersize=6, label='Хоар QuickSort (qs)')
    ax.plot(sort_sizes, series['qsort'], 'bs--', linewidth=1.8, markersize=6, label='stdlib qsort')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_xlabel('Количество элементов N', fontsize=10)
    ax.set_ylabel('Время (секунды)', fontsize=10)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(fontsize=9)

plt.suptitle('Задание 2: Сравнение алгоритмов сортировки на различных наборах данных', fontsize=14, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
sort_plot_path = os.path.join(output_dir, 'sorting_benchmark.png')
plt.savefig(sort_plot_path, dpi=200)
plt.close()
print(f"Saved: {sort_plot_path}")

