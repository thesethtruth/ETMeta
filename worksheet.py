#%% worksheet.py 
import pandas as pd
import numpy as np
from fuzzywuzzy import process
from functools import partial

# from etm api package
import etm

#%% some text utils
last_equals = lambda x, s, target : x[-s:] == target
first_equals = lambda x, s, target : x[:s] == target
last_present = partial(snip_last, s=7, target='present')
first_number = partial(snip_first, s=6, target='number')
combine = lambda x: "_".join(x)
remove = lambda x: [i.replace(' ','_').lower() for i in x]
remove_combine = lambda x: combine(remove(x))

# %% read inputs as received from etm
dfi = etm.generate_input_worksheet()

# finding the bools of rows on specific conditions
present = dfi.code.apply(last_present)    # ending on _present
number = dfi.code.apply(first_number)     # starting with _number
empty = dfi.default.isna()

drops = dfi[present|number|empty].index

# drop those columns that _seem_ irrelevant
dfi.drop(drops, inplace=True)




dft = pd.read_csv('etm_ref/target.csv')
ta = np.array(dft[dft.columns[0:3]])



# %%
