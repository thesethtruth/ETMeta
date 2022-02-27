#%% Imports & Folder set-up

'''It is necessaary to download and install the ETMeta package from TheSethTruth on GitHub. Look at https://github.com/thesethtruth/ETMeta for more information.'''

from os import write
from ETMeta import ETMapi

import pandas as pd
import pickle
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import openpyxl

FOLDER = Path(__file__).parent

#These locations of the folders need to be adapted per use
ETM_INPUTS_FOLDER = FOLDER / "ETM_inputs"
ETM_INPUTS_FOLDER.mkdir(exist_ok=True)

SHEET_FOLDER = FOLDER / "sheets"
SHEET_FOLDER.mkdir(exist_ok=True)

RESULT_FOLDER = FOLDER / "results"
RESULT_FOLDER.mkdir(exist_ok=True)

#-----------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------#
#%% IF necessary - Update the Chromedriver and ETM inputs (takes roughly 3 minutes)

# update chromedriver by webdriver-manager

# # muted because not necessary, unmute when necessary:
# ETMupdate = ETMapi()
# ETMupdate.update_webdriver_chrome()
# ETMupdate.update_etm_inputs()

#-----------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------#
#%% Create the base case - the current situation in the defined area:

#Fill in the data of the defined area
# - find area_code is retrievable in ETMeta/src/ETMeta/data/areacode.csv
# - Scenario_id is by default None as nothing is yet defined in the base_case
#       It is advised to make a base-case scenario on the website, save it and copy the _id
# - define end_year as current year
#       It is necessary to use the end-year of the created scenario
# - source is your source for the data
# - url_base is None as nothing is yet defined in the base_case

area_code = "GM0150_deventer"
scenario_id = 11485
end_year = 2020
source = "api-Witteveen+Bos"

ETMbc = ETMapi(area_code= area_code, scenario_id= scenario_id, end_year= end_year, source= source) #initialize the API with the ETM and store it in de ETMbc

#-----------------------------------------------------------------------------------------------#
#%% Create an Excel worksheet where the new scenarios can be defined:
# - file_name defines where the Excel-file is generated,  example: "base_case_{area}.xlsx"
# - scenario_list is a list of scenarios - if not --> None (will use scenario_id made with ETMapi())
# - prettify makes the Excel worksheet tidy, clear and colorful
file_name_bc = "base_case_deventer.xlsx"
scenario_list = [scenario_id]
prettify = True

filepath = SHEET_FOLDER / file_name_bc
ETMbc.generate_input_worksheet(filepath= filepath, scenario_list= scenario_list, prettify= prettify)


#-----------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------#
#%% Upload scenarios from Excel to run scenarios:
'''
It is necessary to create a copy of the base_case Excel-file created in the previous cell ..
.. in the same folder "sheets"!

Use the copy (advised to rename it) to create scenarios by inserting new columns and ..
.. filling them in with the desired values for the scenarios

Proposed file name for the copy: "scenarios_{area}.xlsx
'''

# New ETM instance to upload to ETM using the API:
area_code = "GM0150_deventer"
source = "api-Witteveen+Bos"

# Add the outputs you want to request from the ETM to be returned after running the scenarios:
output_parameters = [
    #General
    'factsheet_share_solar_and_wind_in_electricity_production',
    'electricity_produced_from_wind_and_solar',
    
    #Solar
    'energy_mix_capacity_per_panel_solar_pv',
    'factsheet_installed_capacity_of_solar_pv',

    'factsheet_supply_electricity_from_solar',
    'factsheet_supply_electricity_from_roof_solar_households',
    'factsheet_supply_electricity_from_roof_solar_buildings',
    'factsheet_supply_from_solar_pv_plants',

    #Wind
    'energy_mix_capacity_per_unit_wind_turbine_inland',
    'factsheet_installed_capacity_of_wind_turbine_inland_coastal',

    'factsheet_supply_electricity_from_wind',

    #For electrolyzer calculations for scenario 1
    "energy_export_electricity",

    #For electrolyzer calculations for scenario 2
    'households_solar_pv_solar_radiation',
    'buildings_solar_pv_solar_radiation',
    'energy_power_solar_pv_solar_radiation',
    'energy_power_wind_turbine_inland',
    ]

ETMu = ETMapi(area_code= area_code, source= source)
ETMu.gqueries.extend(output_parameters)

print(f"The following data are requested to be returned after running the scenarios: {ETMu.gqueries}")

# Excel file definition:
# - file_name_bc is the name of the base_case file in the "sheets"-folder (generated in cell above)
# - file_name_scen is the file name of the scenario file (the copied base case file)
# - scen_start_col is the column in which the first scenario is filled in
# - scen_stop_col is the column in which the last scenario is filled in
# - start_row is the row in which the first parameter is filled in
# - end_row is the row in which the last parameter is filled in
# - ref_scenario is the saved scenario for the base_case
# - end_years are the end years for the scenarios (in the same order)
# - sheet_name is the name in which the scenarios are defined (default = "Sheet1")
# - titles are the titles for the scenarios (in the same order) (default = None)

file_name_bc = "base_case_deventer.xlsx"

file_name_scen = "scenarios_deventer.xlsx"
scen_start_col = "F"
scen_end_col = "L"
scen_start_row = 2
scen_end_row = 611
ref_scenario = None
scen_end_years = [2020, 2025, 2030, 2035, 2025, 2030, 2035]
scen_sheet_name = "Sheet1"
scen_titles = None

#-----------------------------------------------------------------------------------------------#
#%% Run the scenarios from the Excel file named above:
file_path = SHEET_FOLDER / file_name_scen
ETMu.create_new_scenarios_from_excel(
    file_name= file_path,           # filename / path to read excel from
    start_col= scen_start_col,      # first column containing a scenario
    end_col= scen_end_col,          # last column containing a scenario
    start_row= scen_start_row,      # first row containing a slider value
    end_row= scen_end_row,          # last row containing a slider value
    ref_scenarios= ref_scenario,    # KEA reference scenario (if no user value supplied, fall back to value of scenario)
    end_years= scen_end_years,      # End year of scenario
    sheet_name= scen_sheet_name,    # falls back to default 'Sheet1'
    titles= scen_titles,            # note that excel headers (top rows) are automatically passed as title to the ETM for the new scenario if this is None (otherwise supply a list of titles)
)   

#-----------------------------------------------------------------------------------------------#
#%% Reading in the results from the ETM and exporting them to an Excel-file

# Set the max capacity of the electrolyzer manually:
electrolyzer_cap = 2    # unit = MW

#Create results excel-file name
file_name_results = file_name_scen.replace('.xlsx','')
filepath_results = RESULT_FOLDER / f"{file_name_results}_results_{electrolyzer_cap}MW.xlsx"

df = pd.DataFrame({"index":["Here the returned gqueries are listed"],
                        "present":["This is the present value (initial value)"],
                        "future":["This is the future value (end value)"],
                        "unit":["All returns have a certain unit specified here"]})
df.set_index("index", inplace=True)
df.to_excel(filepath_results, sheet_name = f"Dashboard", index=True, engine="openpyxl")

#Store the results from the different scenarios in the results excel-file
for key in ETMu.scenario_batch_result.keys():
    df = ETMu.scenario_batch_result[key]['metrics']
    
    #-----------#
    #Scenario 1: Calculating the used energy by the electrolyzer from the exported electricity
    exported_energy_ph = df.loc["energy_export_electricity","future"]
    total_exported_energy = abs(sum(exported_energy_ph))                    #make positive for in Excel
    electrolyzer_energy_excess_energy = [max(min(x,0),-electrolyzer_cap) for x in exported_energy_ph]
    total_usable_energy_by_elec_excess_energy = abs(sum(electrolyzer_energy_excess_energy))             #make positive for in Excel
    if total_exported_energy == 0:
        share_energy_used_by_elec_excess_energy = 0
    else:
        share_energy_used_by_elec_excess_energy = total_usable_energy_by_elec_excess_energy / total_exported_energy * 100
    full_load_hours_elec_excess_energy = total_usable_energy_by_elec_excess_energy / electrolyzer_cap
    #Creating the additional dataframe with the additional data to later on add to OG dataframe
    df2 = pd.DataFrame({"index":["total_exported_energy","total_usable_energy_by_elec_excess_energy","share_energy_used_by_elec_excess_energy","full_load_hours_electrolyzer_excess_energy"],
                        "present":[0,0,0,0],
                        "future":[total_exported_energy,total_usable_energy_by_elec_excess_energy,share_energy_used_by_elec_excess_energy,full_load_hours_elec_excess_energy],
                        "unit":["MWh","MWh","%","hours"]})
    df2.set_index("index",inplace=True)
    #Add the additional dataframe to the OG dataframe
    df = df.append(df2)
    df = df.drop("energy_export_electricity", axis=0)
    
    #-----------#
    #Scenario 2: Calculating the used energy by the electrolyzer from the renewable electricity
    av_energy_from_solar_hs = df.loc['households_solar_pv_solar_radiation',"future"]
    av_energy_from_solar_bd = df.loc['buildings_solar_pv_solar_radiation',"future"]
    av_energy_from_solar_pv = df.loc['energy_power_solar_pv_solar_radiation',"future"]
    av_energy_from_wind_inland = df.loc['energy_power_wind_turbine_inland',"future"]
    
    zipped_lists = zip(av_energy_from_solar_hs, av_energy_from_solar_bd, av_energy_from_solar_pv, av_energy_from_wind_inland)
    av_energy_total_list = [a+b+c+d for (a,b,c,d) in zipped_lists]
    av_total_energy = sum(av_energy_total_list)                                          #included in excel

    electrolyzer_energy_RES_energy = [min(max(x,0),electrolyzer_cap) for x in av_energy_total_list]
    total_usable_energy_by_elec_RES_energy = abs(sum(electrolyzer_energy_RES_energy))              #included in excel
    if av_total_energy == 0:
        share_energy_used_by_elec_RES_energy = 0
    else:
        share_energy_used_by_elec_RES_energy = total_usable_energy_by_elec_RES_energy / av_total_energy * 100
    full_load_hours_elec_RES_energy = total_usable_energy_by_elec_RES_energy / electrolyzer_cap    #included in excel
    #Creating the additional dataframe with the additional data to later on add to OG dataframe
    df3 = pd.DataFrame({"index":["av_total_energy","total_usable_energy_by_elec_RES_energy","share_energy_used_by_elec_RES_energy","full_load_hours_electrolyzer_RES_energy"],
                        "present":[0,0,0,0],
                        "future":[av_total_energy,total_usable_energy_by_elec_RES_energy,share_energy_used_by_elec_RES_energy,full_load_hours_elec_RES_energy],
                        "unit":["MWh","MWh","%","hours"]})
    df3.set_index("index",inplace=True)
    #Add the additional dataframe to the OG dataframe
    df = df.append(df3)
    df = df.drop('households_solar_pv_solar_radiation', axis=0)
    df = df.drop('buildings_solar_pv_solar_radiation', axis=0)
    df = df.drop('energy_power_solar_pv_solar_radiation', axis=0)
    df = df.drop('energy_power_wind_turbine_inland', axis=0)

    #-----------#
    #Export the results to an Excel-file
    with pd.ExcelWriter(filepath_results, engine= "openpyxl", mode='a') as writer:
        writer.book = openpyxl.load_workbook(filename = filepath_results)
        df.to_excel(writer, sheet_name = f'{key}', index=True)

    print(f"The results of scenario {key} are stored.")

#-----------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------#

# %%
