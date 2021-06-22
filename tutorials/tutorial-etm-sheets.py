# tutorial-etm-sheets.py

#%% Importing relevant packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# import ETM API object from ETMapi.py
from ETMapi import ETMapi

#%% ETMapi object initialization

# Create an instance of the ETMapi object.
# ETMa is used here to distinguish between the instance and class object

ETMa = ETMapi(
    area_code="nl",  # use ETMa.get_areas to discover all posible areas as csv
    scenario_id=None,  # if None, the current situation of the area is used
    end_year=2050,  # ending year of scenario (commonly 2030 or 2050)
    source="api-WB",  # default source argument
)

#%% Examples of various worksheets that can be generated
folder = "sheets/"
# Use ETMa to generate an empty Excel sheet in _bare_ format
file = "bare-etmsheet.xlsx"
ETMa.generate_input_worksheet(
    scenario_list=None,  # This argument is used if values of various scenarios should be included as column in the worksheet
    filepath=folder + file,  # filepath to the generated worksheet
    prettify=False,  # Prettify formats the output and removes the keys (used by ETM engine / ETE)
)

# Use ETMa to generate an empty Excel sheet in _pretty_ format AND with a user defined base scenario (template)
slist = [9436]
# 2030 energiesysteem NL volgens ontwerp KEA v1.1
# https://pro.energytransitionmodel.com/saved_scenarios/9436
# alternatively, this can be defined in the init of the ETMa object:
#     ETMa = ETMapi(scenario_id=9436)
# or
#     ETMa.scenario_id = 9436
file = "pretty-etmsheet.xlsx"
ETMa.generate_input_worksheet(
    scenario_list=slist,  # This argument is used if values of various scenarios should be included as column in the worksheet
    filepath=folder + file,  # filepath to the generated worksheet
    prettify=True,  # Prettify formats the output and removes the keys (used by ETM engine / ETE)
)

# Use ETMa to generate an empty Excel sheet in _pretty_ format AND with a user defined base scenario (template)
slist = [676766, 769764, 797952, 769771]

file = "pretty-multiple-scenarios-etmsheet.xlsx"
ETMa.generate_input_worksheet(
    scenario_list=slist,  # This argument is used if values of various scenarios should be included as column in the worksheet
    filepath=folder + file,  # filepath to the generated worksheet
    prettify=True,  # Prettify formats the output and removes the keys (used by ETM engine / ETE)
)


#%% Uploading scenarios based on the generated excel worksheets

# Create a new instance (ETMu -> ETMupload, suggested convention)
ETMu = ETMapi(scenario_id=None)

# if the colums of multiple scenarios you want to upload are in a range next to each other use
#    start_col: first column containing a scenario
#    end_col:   last column containing a scenario
# e.g.
start_col = "F"
end_col = "I"
# if the columns are not in a range but at arbitrary column locations use
#    scenario_cols: list of all letters of columns
# e.g.
scenario_cols = ["F", "H", "J"]

file_name = "sheets/demo-upload-etmsheet.xlsx"
ETMu.create_new_scenarios_from_excel(
    file_name=file_name,  # filename / path to read excel from
    start_col="F",  # first column containing a scenario
    end_col="F",  # last column containing a scenario
    start_row=3,  # first row containing a slider value
    end_row=485,  # last row containing a slider value
    ref_scenarios=769771,  # KEA reference scenario (if no user value supplied, fall back to value of scenario)
    end_years=2030,  # End year of scenario
    sheet_name=None,  # falls back to default 'sheet1'
    titles=None,  # note that excel headers (top rows) are automatically passed as title to the ETM for the new scenario if this is None (otherwise supply a list of titles)
)
