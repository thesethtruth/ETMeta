# etm_caller.py
import pandas as pd
import numpy as np
from fuzzywuzzy import process
from functools import partial

# from etm api package
import etm


# load all posible area options
areas = etm.area_codes(refresh=False)

# # get the settings of 1 area
# area_settings = get_area_settings(areas[22])

# # create a scenario
# response = create_scenario(
#                                     area_code="PV25_gelderland",
#                                     title="Trial",
#                                     end_year=2050
#                                 )

