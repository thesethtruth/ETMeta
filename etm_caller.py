# etm_caller.py

#%% packages
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json


# from etm api package
from etm import ETMapi


#%% prettify
# from openpyxl import load_workbook
# from openpyxl.styles import PatternFill
# import seaborn as sns

# df = pd.read_excel('G:/My Drive/0 Thesis/05 GIT/etm-api/test.xlsx', sheet_name='Sheet1', engine='openpyxl')

# n_colors = len(df['Section'].unique())
# muted = sns.color_palette('muted', n_colors=n_colors)
# muted = muted.as_hex()
# bright = sns.color_palette('bright', n_colors=n_colors)
# bright = bright.as_hex()

# section_number = lambda key : list(df.Section.unique()).index(key)
# subsection_number = lambda key : list(df.Subsection.unique()).index(key)
# tuple_gen = lambda row : (section_number(row.Section), subsection_number(row.Subsection))
# color_flipper = lambda x : muted[x[0]] if x[1] % 2 else bright[x[0]]

# colors = df.apply(tuple_gen, axis=1).apply(color_flipper)

# wb = load_workbook('test.xlsx')
# ws = wb[wb.sheetnames[0]]

# for index, cell in enumerate(ws['A']):
#     if index != 0:
#         fill = PatternFill(
#             fill_type='solid',
#             start_color= colors[index-1].replace("#", 'FF')
#         )
#         ws['B'][index].fill = fill
#         ws['C'][index].fill = fill
#         ws['D'][index].fill = fill

# wb.save('result.xlsx')
#%% scenario creator

ETM = ETMapi(scenario_id=None)


emiel1= [
        8737,
        9804,
        9429,
        9436,
        9437,
        9184,
        9438,
        9185,
        9439,
        9186,
        9440,
        9187,
]

ETM.generate_input_worksheet(
    filepath='emiel1.xlsx', 
    scenario_list=emiel1,
    prettify=True)

emiel2= [
        8303,
        8304,
        8308,
        8305,
        8306,
        8307,
        8309,
        8310,
]

ETM.generate_input_worksheet(
    filepath='emiel2.xlsx', 
    scenario_list=emiel2,
    prettify=True)



# scenario = ETM.get_all_inputs(outputformat="dataframe", scenario_id=ETM.scenario_id)
# ref = pd.read_csv('etm_ref/clean_scraped_inputs.csv', index_col=0)

#%% uploader (draft)

# group = 'International transport'
# subgroup = 'International navigation technology'
# name = 'LNG'

# index = ((ref.group == group) &\
#         (ref.subgroup== subgroup) &\
#         (ref.translated_name == name))

# key = ref[index]['key'].values[0]

# ETM.user_values.update({key: value})
