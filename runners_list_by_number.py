import csv
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.add_font('Ubuntu', '', 'UbuntuCondensed-Regular.ttf', uni=True)
pdf.set_font('Ubuntu', size=10)

PAGE_WIDTH = 210
PAGE_HEIGHT = 297
COLUMN_WIDTH = PAGE_WIDTH / 2
ROW_HEIGHT = pdf.font_size * 1.5


def column_switcher(value: bool) -> bool:
    """Переключалка колонок"""
    return True if value is False else False


def get_year(date: str) -> int:
    return date.split('-')[0]


def add_row(row):
    """Добавляем строку"""
    pdf.cell(
            COLUMN_WIDTH - 20,
            ROW_HEIGHT,
            txt=f"{row[0]}   {row[1]} {row[2]} ({get_year(row[3])})", ln=1
        )


def get_pdf(file):
    # Читаем CSV файл с данными клиентов
    with open(file, encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        # Сортируем данные по фамилии
        sorted_data = sorted(reader, key=lambda row: int(row[0]))
    HUNDRED = int(sorted_data[0][0]) // 100

    # Определяем текущие координаты курсора
    x = 10
    y = 10

    # Опреелем значение индекса колонок
    column_index = 0

    # Устанавливаем курсор на первую колонку
    first_column = True
    # Добавляем данные в PDF файл
    for i, row in enumerate(sorted_data):
        column_index += 1
        if column_index > 50:
            column_index = 1
            first_column = column_switcher(first_column)
            y = 10

        # Если достигнуто макс количество строк на странице, добавляем новую стр
        if int(row[0]) // 100 != HUNDRED:
            HUNDRED = int(row[0]) // 100
            pdf.add_page()
            first_column = True
            column_index = 1
            # Сбрасываем координаты на начало страницы
            x = 10
            y = 10

        # Если это первая колонка, добавляем данные на текущую страницу
        if first_column is True:
            # Если достигнут конец страницы, переходим на следующую колонку
            if y + ROW_HEIGHT > PAGE_HEIGHT:
                x += COLUMN_WIDTH
                y = 10

            # Добавляем данные в первую колонку
            add_row(row)
            pdf.line(
                x1=x-3,
                y1=y+ROW_HEIGHT,
                x2=x+COLUMN_WIDTH-40,
                y2=y+ROW_HEIGHT
            )
            y += ROW_HEIGHT

        # Если это вторая колонка, добавляем данные на следующую страницу
        if first_column is False:
            # Если достигнут конец страницы, переходим на новую страницу
            if y + ROW_HEIGHT > PAGE_HEIGHT:
                pdf.add_page()
                first_column = True
                # Сбрасываем координаты на начало страницы
                x = 10
                y = 10
            x = 10 + COLUMN_WIDTH
            # Добавляем данные во вторую колонку
            pdf.set_xy(x, y)
            add_row(row)
            pdf.line(
                x1=x-3,
                y1=y+ROW_HEIGHT,
                x2=x+COLUMN_WIDTH-40,
                y2=y+ROW_HEIGHT
            )
            y += ROW_HEIGHT

    # Сохраняем PDF файл
    pdf.output(f'{file.split(".")[0]}_by_numbers.pdf')
