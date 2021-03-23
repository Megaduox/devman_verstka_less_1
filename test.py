import pandas as pd
from pprint import pprint
from collections import defaultdict


new_dict = defaultdict(list)
new_list = list()
new_cat = defaultdict(list)

excel_data_frame = pd.read_excel('wine3.xlsx', sheet_name="Лист1")
data_from_excel = excel_data_frame.to_dict('records')

for key in data_from_excel:
        new_dict[key['Категория']].append(key)

cat_list = list(new_dict.keys())

cat1 = cat_list[0]
cat2 = cat_list[1]
cat3 = cat_list[2]


# pprint(white_wine)
pprint(cat1)
