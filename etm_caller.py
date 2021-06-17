# etm_caller.py

from etm import ETMapi

ETM = ETMapi(scenario_id=769771)

# ETM.generate_input_worksheet(filepath="empty-etmsheet.xlsx", prettify=True)

file_name = "200511_ETM_inputs_KEA++.xlsx"
start_col = "I"
end_col = "Q"
ref_scenarios = 769771
end_years = 2030
start_row = 3
end_row = 485

# user_values = ETM.extract_excel_etm_values(
#     file_name="200511_ETM_inputs_KEA++.xlsx",
#     start_col="I",
#     end_col="I",
#     start_row=3,
#     end_row=485,
# )

ETM.create_new_scenarios_from_excel(
    file_name="200511_ETM_inputs_KEA++.xlsx",
    start_col="I",
    end_col="I",
    start_row=3,
    end_row=485,
    ref_scenarios=769771,
    end_years=2030,
    sheet_name=None,
)
