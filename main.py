import datetime
import os
import argparse

from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd

from jinja2 import Environment, FileSystemLoader, select_autoescape


def years():
    run_time = 1920
    now_time = datetime.datetime.today()
    years_with_you = now_time.year - run_time

    if (years_with_you % 10 == 1) and (years_with_you != 11) and (years_with_you != 111):
        ending = "год"
    elif (years_with_you % 10 > 1) and (years_with_you % 10 < 5) and (years_with_you != 12) \
            and (years_with_you != 13) and (years_with_you != 14):
        ending = "года"
    else:
        ending = "лет"

    return f"Уже {years_with_you} {ending} с Вами"


def main():

    parser = argparse.ArgumentParser(description='Введите название файла в формате xlsx (Пример: wine.xlsx) '
                                                 'и нажмите Enter. Из этого файла программа возмёт данные для '
                                                 'формирования цен, названий и сортов вина. '
                                                 'Файл нужно положить в папку со скриптом.')
    parser.add_argument('file_name', help='Название файла')
    args = parser.parse_args()
    excel_file = pd.read_excel(args.file_name, sheet_name="Лист1", na_values=False, keep_default_na=False)
    records_from_excel_file = excel_file.to_dict('records')
    pruduction = defaultdict(list)

    for record in records_from_excel_file:
        pruduction[record['Категория']].append(record)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        years_with_you=years(),
        items=pruduction
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
