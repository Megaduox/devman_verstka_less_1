from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas as pd
from collections import defaultdict
from pprint import pprint


excel_data_frame = pd.read_excel('wine4.xlsx', sheet_name="Лист1")
data_from_excel = excel_data_frame.to_dict('records')

new_dict = defaultdict(list)
new_list = list()

for key in data_from_excel:
    new_dict[key['Категория']].append(key)

cat_list = list(new_dict.keys())

cat1 = cat_list[0]
cat2 = cat_list[1]
cat3 = cat_list[2]

white_wine = new_dict[cat1]
napitki = new_dict[cat2]
red_wine = new_dict[cat3]

# удаляю в напитках элемент "Сорт", т.к. по задаче его не должно быть ни в коде, ни в шаблоне
for elem in napitki:
    try:
        del elem['Сорт']
    except KeyError:
        pass

# проверка на "выгодное предложение"
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

# pprint(napitki)
# pprint(white_wine)
# pprint(red_wine)
# breakpoint()


def years():
    run_time = datetime.datetime(year=1920, month=1, day=1, hour=1)
    now_time = datetime.datetime.today()
    years_with_you = now_time.year - run_time.year
    return years_with_you


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    years_with_you=years(),
    items=new_dict,
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


