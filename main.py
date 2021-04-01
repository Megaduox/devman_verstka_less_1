from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas as pd
from collections import defaultdict
import argparse
import os

parser = argparse.ArgumentParser(description='Введите название файла в формате xlsx (Пример: wine.xlsx) '
                                             'и нажмите Enter. Из этого файла программа возмёт данные для '
                                             'формирования цен, названий и сортов вина. '
                                             'Файл нужно положить в папку со скриптом.')
parser.add_argument('file_name', help='Название файла')
args = parser.parse_args()

root_dir = os.getcwd() + "\\"
excel_file = pd.read_excel(root_dir+args.file_name, sheet_name="Лист1")
records_from_excel_file = excel_file.to_dict('records')

categories = defaultdict(list)

for key in records_from_excel_file:
    categories[key['Категория']].append(key)

cat_list = list(categories.keys())

cat1 = cat_list[0]
cat2 = cat_list[1]
cat3 = cat_list[2]

white_wine = categories[cat1]
napitki = categories[cat2]
red_wine = categories[cat3]

for elem in napitki:
    try:
        del elem['Сорт']
    except KeyError:
        pass

for elem in napitki:
    if elem["Акция"] == "Выгодное предложение":
        pass
    else:
        del elem['Акция']

for elem in white_wine:
    if elem["Акция"] == "Выгодное предложение":
        pass
    else:
        del elem['Акция']

for elem in red_wine:
    if elem["Акция"] == "Выгодное предложение":
        pass
    else:
        del elem['Акция']


def years():
    run_time = 1920
    now_time = datetime.datetime.today()
    years_with_you = now_time.year - run_time
    if years_with_you == 100:
        ending = "лет"
    elif years_with_you == 102 or years_with_you == 103 or years_with_you == 104:
        ending = "года"
    elif years_with_you == 101:
        ending = "год"
    else:
        ending = "лет"

    return f"Уже {years_with_you} {ending} с Вами"


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    years_with_you=years(),
    items=categories,
    drinks=napitki,
    white=white_wine,
    red=red_wine,
    cat1=cat1,
    cat2=cat2,
    cat3=cat3
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
server.serve_forever()


