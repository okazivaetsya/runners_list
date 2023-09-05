import csv

from fpdf import FPDF


def get_pdf(file):
    class PDF(FPDF):
        # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-15)
            # Page number
            self.cell(0, 10, str(self.page_no()) + '/{nb}', 0, 0, 'C')

    # Создаем PDF файл
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.add_font('Ubuntu', '', 'UbuntuCondensed-Regular.ttf', uni=True)
    pdf.set_font('Ubuntu', size=10)

    PAGE_WIDTH = 210
    PAGE_HEIGHT = 297
    COLUMN_WIDTH = PAGE_WIDTH / 2
    ROW_HEIGHT = pdf.font_size * 1.5
    LAST_LETTER = '0'

    # Определяем максимальное количество строк на странице
    MAX_ROWS = 100

    # Определяем текущие координаты курсора
    x = 10
    y = 10

    # Опреелем значение индекса колонок
    column_index = 0

    # Устанавливаем курсор на первую колонку
    first_column = True


    def check_new_letter(row) -> bool:
        """Проверяем наличие новой буквы"""
        nonlocal LAST_LETTER
        if row[1][0] != LAST_LETTER:
            LAST_LETTER = row[1][0]
            return True
        return False


    def get_year(date: str) -> int:
        """Достаем год из даты рождения"""
        return date.split('-')[0]


    def column_switcher(value: bool) -> bool:
        """Переключалка колонок"""
        return True if value is False else False


    def add_row(row):
        """Добавляем строку"""
        nonlocal x, LAST_LETTER
        if check_new_letter(row):
            x -= 5
            pdf.set_x(x)
            pdf.cell(
                5,
                5,
                # Выводим новую букву
                txt=f"{LAST_LETTER}", ln=0
            )
            x += 5
            pdf.set_x(x)

        pdf.cell(
                COLUMN_WIDTH - 20,
                ROW_HEIGHT,
                # формат строки Фамилия Имя (год рождения) – BIB
                txt=f"{row[1]} {row[2]} ({get_year(row[3])}) – {row[0]}", ln=1
            )
    with open(file, encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        # Сортируем данные по фамилии
        sorted_data = sorted(reader, key=lambda row: row[1])
    # Добавляем данные в PDF файл
    for i, row in enumerate(sorted_data):
        column_index += 1
        if column_index > 50:
            column_index = 1
            first_column = column_switcher(first_column)
            y = 10

        # Если достигнуто макс количество строк на странице, добавляем новую стр
        if i % MAX_ROWS == 0 and i > 0:
            pdf.add_page()
            first_column = True
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
            y += ROW_HEIGHT

    # Сохраняем PDF файл
    pdf.output(f'{file.split(".")[0]}_by_alph.pdf')
