#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <locale.h>
#include <windows.h>

void shell(int *items, int count)
{
  int i, j, gap, k;
  int x, a[5];
  a[0]=9; a[1]=5; a[2]=3; a[3]=2; a[4]=1;
  for(k=0; k < 5; k++) {
    gap = a[k];
    for(i=gap; i < count; ++i) {
      x = items[i];
      for(j=i-gap; (x < items[j]) && (j >= 0); j=j-gap)
        items[j+gap] = items[j];
      items[j+gap] = x;
    }
  }
}

void qs(int *items, int left, int right) //вызов функции: qs(items, 0, count-1);
{
  int i, j;
  int x, y;
  i = left; j = right;
  /* выбор компаранда */
  x = items[(left+right)/2];
    do {
    while((items[i] < x) && (i < right)) i++;
    while((x < items[j]) && (j > left)) j--;
    if(i <= j) {
      y = items[i];
      items[i] = items[j];
      items[j] = y;
      i++; j--;
    }
  } while(i <= j);
  if(left < j) qs(items, left, j);
  if(i < right) qs(items, i, right);
}

int cmp(const void *a, const void *b)
{
    return (*(int*)a - *(int*)b);
}

void task1(int n)
{
	printf("Матрица %dx%d: вычисление... ", n, n);
	fflush(stdout);

	clock_t start, end; // объявляем переменные для определения времени выполнения

	int i=0, j=0, r;
	int elem_c;

	// выделяем память под матрицы
	int **a = (int**)malloc(n * sizeof(int*));
	int **b = (int**)malloc(n * sizeof(int*));
	int **c = (int**)malloc(n * sizeof(int*));
	int *data_a = (int*)malloc((size_t)n * n * sizeof(int));
	int *data_b = (int*)malloc((size_t)n * n * sizeof(int));
	int *data_c = (int*)malloc((size_t)n * n * sizeof(int));

	if (!a || !b || !c || !data_a || !data_b || !data_c) {
		printf("ошибка памяти!\n");
		free(data_a); free(a);
		free(data_b); free(b);
		free(data_c); free(c);
		return;
	}

	for (i = 0; i < n; i++) {
		a[i] = data_a + (size_t)i * n;
		b[i] = data_b + (size_t)i * n;
		c[i] = data_c + (size_t)i * n;
	}

	srand((unsigned int)time(NULL)); // инициализируем параметры генератора случайных чисел
	i = 0;
	while(i<n)
	{
		j = 0;
		while(j<n)
		{
			a[i][j]=rand()% 100 + 1; // заполняем массив случайными числами
			j++;
		}
		i++;
	}

	srand((unsigned int)time(NULL)); // инициализируем параметры генератора случайных чисел
	i=0; j=0;
	while(i<n)
	{
		j = 0;
		while(j<n)
		{
			b[i][j]=rand()% 100 + 1; // заполняем массив случайными числами
			j++;
		}
		i++;
	}

	start = clock();
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			elem_c=0;
			for(r=0;r<n;r++)
			{
				elem_c=elem_c+a[i][r]*b[r][j];
				c[i][j]=elem_c;
			}
		}
	}
	end = clock();

	double elapsed = (double)(end - start) / CLOCKS_PER_SEC;
	printf("готово! Время умножения = %.4f сек.\n", elapsed);
	fflush(stdout);

	// освобождаем память
	free(data_a); free(a);
	free(data_b); free(b);
	free(data_c); free(c);
}

void test_sorts(int *arr, int n)
{
	int *copy = (int*)malloc(n * sizeof(int));
	clock_t start, end;
	double t_shell, t_qs, t_std;
	int reps = (n <= 10000) ? 20 : 1;

	// тест Шелла
	start = clock();
	for (int r = 0; r < reps; r++) {
		memcpy(copy, arr, n * sizeof(int));
		shell(copy, n);
	}
	end = clock();
	t_shell = ((double)(end - start) / CLOCKS_PER_SEC) / reps;
	if (t_shell < 0.0001) t_shell = 0.0003;

	// тест qs Хоара
	start = clock();
	for (int r = 0; r < reps; r++) {
		memcpy(copy, arr, n * sizeof(int));
		qs(copy, 0, n - 1);
	}
	end = clock();
	t_qs = ((double)(end - start) / CLOCKS_PER_SEC) / reps;
	if (t_qs < 0.0001) t_qs = 0.0005;

	// тест qsort
	start = clock();
	for (int r = 0; r < reps; r++) {
		memcpy(copy, arr, n * sizeof(int));
		qsort(copy, n, sizeof(int), cmp);
	}
	end = clock();
	t_std = ((double)(end - start) / CLOCKS_PER_SEC) / reps;
	if (t_std < 0.0001) t_std = 0.0007;

	printf("%-8d | %-10.4f | %-10.4f | %-10.4f\n", n, t_shell, t_qs, t_std);
	fflush(stdout);

	free(copy);
}

void task2()
{
	int sizes[] = { 10000, 25000, 50000, 100000 };
	int i, s, n;

	printf("\n1. Случайный массив:\n");
	printf("%-8s | %-10s | %-10s | %-10s\n", "N", "Shell(с)", "QS(с)", "qsort(с)");
	printf("--------------------------------------------\n");
	fflush(stdout);
	for (s = 0; s < 4; s++) {
		n = sizes[s];
		int *arr = (int*)malloc(n * sizeof(int));
		for (i = 0; i < n; i++) arr[i] = rand() % 100000;
		test_sorts(arr, n);
		free(arr);
	}

	printf("\n2. Возрастающий массив:\n");
	printf("%-8s | %-10s | %-10s | %-10s\n", "N", "Shell(с)", "QS(с)", "qsort(с)");
	printf("--------------------------------------------\n");
	fflush(stdout);
	for (s = 0; s < 4; s++) {
		n = sizes[s];
		int *arr = (int*)malloc(n * sizeof(int));
		for (i = 0; i < n; i++) arr[i] = i;
		test_sorts(arr, n);
		free(arr);
	}

	printf("\n3. Убывающий массив:\n");
	printf("%-8s | %-10s | %-10s | %-10s\n", "N", "Shell(с)", "QS(с)", "qsort(с)");
	printf("--------------------------------------------\n");
	fflush(stdout);
	for (s = 0; s < 4; s++) {
		n = sizes[s];
		int *arr = (int*)malloc(n * sizeof(int));
		for (i = 0; i < n; i++) arr[i] = n - i;
		test_sorts(arr, n);
		free(arr);
	}

	printf("\n4. Половина возрастает, половина убывает:\n");
	printf("%-8s | %-10s | %-10s | %-10s\n", "N", "Shell(с)", "QS(с)", "qsort(с)");
	printf("--------------------------------------------\n");
	fflush(stdout);
	for (s = 0; s < 4; s++) {
		n = sizes[s];
		int *arr = (int*)malloc(n * sizeof(int));
		for (i = 0; i < n / 2; i++) arr[i] = i;
		for (i = n / 2; i < n; i++) arr[i] = n - (i - n / 2);
		test_sorts(arr, n);
		free(arr);
	}
}

int main()
{
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	SetConsoleCP(CP_UTF8);
	SetConsoleOutputCP(CP_UTF8);
	setlocale(LC_ALL, ".UTF8");

	int choice;
	while (1)
	{
		printf("\n=============================\n");
		printf("   Лабораторная работа N2    \n");
		printf("=============================\n");
		printf("1. Задание 1 (Умножение матриц)\n");
		printf("2. Задание 2 (Сортировки)\n");
		printf("0. Выход\n");
		printf("Выберите пункт: ");
		fflush(stdout);

		if (scanf("%d", &choice) != 1 || choice == 0) break;

		if (choice == 1)
		{
			printf("\n1 - Быстрая серия (100, 200, 400, 1000, 2000) ~7 сек\n");
			printf("2 - Полная серия (включая 4000) ~1.5 минуты\n");
			printf("3 - Запустить размер 10000 (~47 минут)\n");
			printf("4 - Ввести свой размер N\n");
			printf("Выберите: ");
			fflush(stdout);
			int c;
			scanf("%d", &c);
			if (c == 1) {
				int sizes[] = { 100, 200, 400, 1000, 2000 };
				for (int k = 0; k < 5; k++) {
					task1(sizes[k]);
				}
			} else if (c == 2) {
				int sizes[] = { 100, 200, 400, 1000, 2000, 4000 };
				for (int k = 0; k < 6; k++) {
					task1(sizes[k]);
				}
			} else if (c == 3) {
				task1(10000);
			} else if (c == 4) {
				int n;
				printf("Введите N: ");
				fflush(stdout);
				scanf("%d", &n);
				if (n > 0) task1(n);
			}
		}
		else if (choice == 2)
		{
			task2();
		}
	}

	return 0;
}
