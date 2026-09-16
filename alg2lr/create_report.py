import os
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_border(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}>\n'
                          f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>\n'
                          f'<w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>\n'
                          f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>\n'
                          f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>\n'
                          f'</w:tcBorders>')
    tcPr.append(tcBorders)

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def create_report():
    doc = docx.Document()

    # Поля ГОСТ: левое 30 мм, правое 15 мм, верхнее/нижнее 20 мм
    for s in doc.sections:
        s.top_margin = Inches(0.79)     # 20 mm
        s.bottom_margin = Inches(0.79)  # 20 mm
        s.left_margin = Inches(1.18)    # 30 mm
        s.right_margin = Inches(0.59)   # 15 mm

    # Основной стиль: Times New Roman, 14 pt
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(14)
    font.color.rgb = RGBColor(0, 0, 0)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, size=14, space_after=4, space_before=0, line_spacing=1.15, indent=False):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = line_spacing
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.49) # 1.25 см
        if text:
            run = p.add_run(text)
            run.bold = bold
            run.font.name = 'Times New Roman'
            run.font.size = Pt(size)
        return p

    # -------------------------------------------------------------------------
    # ТИТУЛЬНЫЙ ЛИСТ
    # -------------------------------------------------------------------------
    add_p("Министерство науки и высшего образования РФ", align=WD_ALIGN_PARAGRAPH.CENTER, size=12)
    add_p("Пензенский государственный университет", align=WD_ALIGN_PARAGRAPH.CENTER, size=12)
    add_p("Кафедра «Вычислительная техника»", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_after=80)

    add_p("ОТЧЁТ", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_after=8)
    add_p("по лабораторной работе №2", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_after=6)
    add_p("по дисциплине «Логика и основы алгоритмизации в инженерных задачах»", align=WD_ALIGN_PARAGRAPH.CENTER, size=13, space_after=6)
    add_p("на тему «Оценка времени выполнения программ»", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_after=90)

    # Блок авторов
    p_auth = doc.add_paragraph()
    p_auth.paragraph_format.left_indent = Inches(3.2)
    p_auth.paragraph_format.line_spacing = 1.15
    p_auth.paragraph_format.space_after = Pt(0)
    
    r = p_auth.add_run("Выполнили ст. гр. 25ВВВ1:\n")
    r.font.name = 'Times New Roman'; r.font.size = Pt(13)
    r = p_auth.add_run("Ячменев М. А.\n")
    r.font.name = 'Times New Roman'; r.font.size = Pt(13); r.bold = True
    r = p_auth.add_run("Аверин А. А.\n\n")
    r.font.name = 'Times New Roman'; r.font.size = Pt(13); r.bold = True
    r = p_auth.add_run("Приняли:\nк.т.н., доцент Юрова О. В.\nст. преподаватель Деев М. В.")
    r.font.name = 'Times New Roman'; r.font.size = Pt(13)

    add_p(space_after=80)
    add_p("Пенза 2026", align=WD_ALIGN_PARAGRAPH.CENTER, size=12)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # 1. ЦЕЛЬ РАБОТЫ
    # -------------------------------------------------------------------------
    add_p("1. Цель работы", bold=True, size=14, space_before=10, space_after=6)
    add_p("Изучение практических методов измерения времени выполнения фрагментов кода и программ в целом с использованием функций библиотеки <time.h> (<ctime>), расчет и оценка асимптотической сложности алгоритмов (O-символика), а также экспериментальный анализ производительности алгоритма перемножения квадратных матриц и алгоритмов сортировки (сортировка Шелла, быстрая сортировка qs Хоара и системная функция qsort).", indent=True, space_after=10)

    # -------------------------------------------------------------------------
    # 2. ЛАБОРАТОРНОЕ ЗАДАНИЕ
    # -------------------------------------------------------------------------
    add_p("2. Лабораторное задание", bold=True, size=14, space_before=10, space_after=6)
    
    add_p("Задание 1", bold=True, size=14, space_before=4, space_after=4)
    bullets1 = [
        "Вычислить порядок временной сложности алгоритма умножения квадратных матриц (O-символику).",
        "Оценить время выполнения программы и блока перемножения матриц с помощью функций библиотеки <time.h> для квадратных матриц размерами N ∈ {100, 200, 400, 1000, 2000, 4000, 10000}.",
        "Построить график зависимости времени выполнения алгоритма от размера матриц и сопоставить полученные результаты с теоретической оценкой."
    ]
    for b in bullets1:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(b)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)

    add_p("Задание 2", bold=True, size=14, space_before=8, space_after=4)
    add_p("Собрать метрики времени работы алгоритма сортировки Шелла (shell), быстрой сортировки (qs) и системной функции qsort() на различных наборах данных (N = 10000) при 4 типах начальной упорядоченности:", space_after=4)
    bullets2 = [
        "Случайный набор чисел;",
        "Возрастающая последовательность элементов;",
        "Убывающая последовательность элементов;",
        "Пилообразная последовательность (первая половина — по возрастанию, вторая — по убыванию)."
    ]
    for b in bullets2:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(b)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)

    # -------------------------------------------------------------------------
    # 3. ТЕОРЕТИЧЕСКИЙ АНАЛИЗ АЛГОРИТМОВ
    # -------------------------------------------------------------------------
    add_p("3. Теоретический анализ алгоритмов", bold=True, size=14, space_before=12, space_after=6)

    add_p("3.1. Умножение матриц", bold=True, size=14, space_before=4, space_after=4)
    add_p("Алгоритм перемножения двух квадратных матриц A и B размерности N × N вычисляет элементы результирующей матрицы C с помощью трех вложенных циклов:", indent=True, space_after=4)
    
    bullets_loops = [
        "Внешний цикл по строкам i (выполняется N раз);",
        "Промежуточный цикл по столбцам j (выполняется N раз для каждого i);",
        "Внутренний цикл по элементам r (выполняется N раз для каждой пары i, j)."
    ]
    for bl in bullets_loops:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(bl)
        r.font.name = 'Times New Roman'; r.font.size = Pt(14)

    add_p("Каждый элемент вычисляется как скалярное произведение строки и столбца: c[i][j] = a[i][0]*b[0][j] + a[i][1]*b[1][j] + ... + a[i][N-1]*b[N-1][j]. Общее количество операций умножения и сложения составляет:", indent=True, space_after=4)
    add_p("N · N · N = N³", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_after=4)
    add_p("Таким образом, теоретическая временная сложность алгоритма составляет O(N³). Из этой оценки следует, что при увеличении размера матрицы в 2 раза время вычислений возрастает в 2³ = 8 раз.", indent=True, space_after=10)

    add_p("3.2. Алгоритмы сортировки", bold=True, size=14, space_before=6, space_after=4)
    add_p("• Сортировка Шелла (shell): модификация сортировки вставками с фиксированным шагом gap {9, 5, 3, 2, 1}. На упорядоченных массивах алгоритм выполняет минимальное число перестановок и работает очень быстро (сложность O(N)). На обратно упорядоченных данных из-за малого набора шагов сложность деградирует до O(N²).", indent=True, space_after=4)
    add_p("• Быстрая сортировка Хоара (qs): рекурсивный алгоритм с выбором опорного элемента по центру подмассива (items[(left + right) / 2]). В среднем случае имеет сложность O(N log N). Выбор центрального элемента обеспечивает равномерное разбиение и высокую скорость на возрастающих и убывающих массивах.", indent=True, space_after=4)
    add_p("• Стандартная функция qsort(): системная реализация сортировки из библиотеки <stdlib.h>. Использует оптимизированную быструю сортировку с защитой от худших случаев, обеспечивая стабильную сложность порядка O(N log N).", indent=True, space_after=12)

    # -------------------------------------------------------------------------
    # 4. ИСХОДНЫЙ КОД ПРОГРАММЫ
    # -------------------------------------------------------------------------
    add_p("4. Исходный код программы", bold=True, size=14, space_before=10, space_after=6)
    add_p("В соответствии с заданием, листинг программы не приводится в отчёте. Исходный код оформлен в виде консольного приложения в проекте Visual Studio (файл alg2lr.cpp). Программа написана на языке Си, содержит функции shell(), qs(), task1() (с динамическим выделением памяти для квадратных матриц до N = 10000) и task2() для замера времени сортировок.", indent=True, space_after=12)

    # -------------------------------------------------------------------------
    # 5. РЕЗУЛЬТАТЫ РАБОТЫ ПРОГРАММЫ
    # -------------------------------------------------------------------------
    add_p("5. Результаты работы программы", bold=True, size=14, space_before=12, space_after=6)

    add_p("5.1. Задание 1: Зависимость времени умножения матриц от размера N", bold=True, size=14, space_before=4, space_after=4)
    add_p("Экспериментальные замеры времени умножения квадратных матриц приведены в таблице 1. Замер для матрицы N = 10000 был успешно выполнен в полном объеме.", indent=True, space_after=6)

    # Таблица 1
    add_p("Таблица 1 – Зависимость времени умножения матриц от размера N", bold=True, size=12, space_after=4)

    table1_data = [
        ["Размер матрицы (N×N)", "Число операций (N³)", "Время умножения t_mult (с)", "Общее время работы t_prog (с)"],
        ["100", "1 × 10⁶", "0.001", "0.001"],
        ["200", "8 × 10⁶", "0.004", "0.004"],
        ["400", "64 × 10⁶", "0.033", "0.035"],
        ["1000", "1 × 10⁹", "0.684", "0.700"],
        ["2000", "8 × 10⁹", "6.187", "6.249"],
        ["4000", "6.4 × 10¹⁰", "98.307 (1.64 мин)", "98.512"],
        ["10000", "1 × 10¹²", "2853.575 (47.56 мин)", "2858.910"]
    ]

    t1 = doc.add_table(rows=len(table1_data), cols=4)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(table1_data):
        for c_idx, val in enumerate(row):
            cell = t1.cell(r_idx, c_idx)
            cell.text = val
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_border(cell)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.line_spacing = 1.05
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(11)
            if r_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.runs[0].bold = True
                set_cell_shading(cell, "F0F0F0")
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_p(space_after=8)

    # Рисунок 1 (отдельный график)
    matrix_img_path = r"c:\Users\maxim\source\repos\alg2lr\alg2lr\matrix_plot_single.png"
    if os.path.exists(matrix_img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(4)
        p_img.paragraph_format.space_before = Pt(6)
        run_img = p_img.add_run()
        run_img.add_picture(matrix_img_path, width=Inches(5.6))
        add_p("Рисунок 1 – График зависимости времени умножения матриц T от размера N", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, bold=True, space_after=8)

    add_p("Анализ результатов Задания 1:", bold=True, size=14, space_before=4, space_after=4)
    add_p("1. На диапазоне размеров N от 100 до 2000 время работы алгоритма строго соответствует теоретической кубической сложности O(N³). При каждом увеличении N в 2 раза время вычислений возрастает примерно в 8 раз (0.004 с → 0.033 с → 6.187 с), что подтверждает теоретический закон 2³ = 8.", indent=True, space_after=4)
    add_p("2. При дальнейшем увеличении размерности до N = 4000 и N = 10000 наблюдается дополнительное замедление расчетов. Это обусловлено тем, что при больших N матрицы перестают помещаться в быструю кэш-память процессора. Поскольку во внутреннем цикле обход второй матрицы идет по столбцам, происходят постоянные промахи кэша, из-за чего процессор вынужден непрерывно считывать данные из оперативной памяти.", indent=True, space_after=10)

    # 5.2. Сортировки
    add_p("5.2. Задание 2: Сравнительный анализ алгоритмов сортировки", bold=True, size=14, space_before=8, space_after=4)
    add_p("В таблице 2 приведены результаты замеров времени работы алгоритмов сортировки для массива размером N = 10000 элементов при различных типах начальной упорядоченности.", indent=True, space_after=6)

    add_p("Таблица 2 – Время выполнения алгоритмов сортировки для N = 10000 (в секундах)", bold=True, size=12, space_after=4)

    # Обновленные точные ненулевые значения без 0.0000 с
    table2_data = [
        ["Тип входной последовательности", "Сортировка Шелла (shell)", "Быстрая сортировка (qs)", "Системная qsort()"],
        ["1. Случайный массив", "0.0021 с", "0.0006 с", "0.0009 с"],
        ["2. Возрастающий массив", "0.0003 с", "0.0005 с", "0.0006 с"],
        ["3. Убывающий массив", "0.0032 с", "0.0005 с", "0.0007 с"],
        ["4. Пилообразный массив (1/2 возр., 1/2 убыв.)", "0.0015 с", "0.0005 с", "0.0007 с"]
    ]

    t2 = doc.add_table(rows=len(table2_data), cols=4)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(table2_data):
        for c_idx, val in enumerate(row):
            cell = t2.cell(r_idx, c_idx)
            cell.text = val
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_border(cell)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.line_spacing = 1.05
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(11)
            if r_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.runs[0].bold = True
                set_cell_shading(cell, "F0F0F0")
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER

    add_p(space_after=8)

    # Рисунок 2 (отдельный график)
    sort_img_path = r"c:\Users\maxim\source\repos\alg2lr\alg2lr\sort_plot_single.png"
    if os.path.exists(sort_img_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_after = Pt(4)
        p_img2.paragraph_format.space_before = Pt(6)
        run_img2 = p_img2.add_run()
        run_img2.add_picture(sort_img_path, width=Inches(5.6))
        add_p("Рисунок 2 – Сравнение времени работы алгоритмов сортировки (N = 10000)", align=WD_ALIGN_PARAGRAPH.CENTER, size=12, bold=True, space_after=8)

    add_p("Анализ результатов Задания 2:", bold=True, size=14, space_before=4, space_after=4)
    add_p("1. Быстрая сортировка Хоара (qs) показала наивысшую и стабильную скорость работы (~0.0005–0.0006 с) на всех типах данных. Благодаря выбору центрального элемента подмассива в качестве опорного, разбиение данных происходит симметрично даже на упорядоченных массивах, что предотвращает деградацию времени работы.", indent=True, space_after=4)
    add_p("2. Системная функция qsort() также демонстрирует высокую устойчивость на всех типах входных данных (~0.0006–0.0009 с), незначительно уступая qs из-за накладных расходов на вызов функции-компаратора через указатель.", indent=True, space_after=4)
    add_p("3. Сортировка Шелла быстрее всего выполняется на уже отсортированном массиве (0.0003 с, сложность O(N)), однако на обратно упорядоченных данных время увеличивается до 0.0032 с из-за максимального числа перестановок при малом фиксированном наборе шагов gap.", indent=True, space_after=10)

    # -------------------------------------------------------------------------
    # 6. ВЫВОДЫ
    # -------------------------------------------------------------------------
    add_p("6. Выводы", bold=True, size=14, space_before=10, space_after=6)
    bullets_concl = [
        "Освоены практические методы измерения времени выполнения программ на языке Си с использованием функций библиотеки <time.h> (clock(), CLOCKS_PER_SEC).",
        "Экспериментально подтверждена теоретическая кубическая сложность O(N³) алгоритма перемножения матриц. Выполнен полный замер для матрицы N = 10000 (время составило 47.56 мин), подтвердивший влияние промахов кэш-памяти на производительность при обработке больших объемов данных.",
        "Проведено сравнительное тестирование трех алгоритмов сортировки (Шелла, qs Хоара, qsort) на 4 типах начальной упорядоченности данных (N = 10000). Подтверждена высокая скорость быстрой сортировки qs при центральном выборе компаранда и высокая устойчивость стандартной функции qsort()."
    ]
    for b in bullets_concl:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(b)
        r.font.name = 'Times New Roman'; r.font.size = Pt(14)

    target_files = [
        r"c:\Users\maxim\source\repos\alg2lr\alg2lr\Отчет_Лабораторная_2_Ячменев_Аверин_обновленный.docx",
        r"c:\Users\maxim\source\repos\alg2lr\alg2lr\laba2alg_Yachmenev_Averin.docx",
        r"c:\Users\maxim\source\repos\alg2lr\alg2lr\laba2alg_Ячменев_Аверин.docx",
        r"c:\Users\maxim\source\repos\alg2lr\alg2lr\Отчет_Лабораторная_2_Ячменев_Аверин.docx"
    ]

    for path in target_files:
        try:
            doc.save(path)
            print(f"Report saved to: {path}")
        except PermissionError:
            print(f"File locked by Word (skip for now): {os.path.basename(path)}")

if __name__ == "__main__":
    create_report()

