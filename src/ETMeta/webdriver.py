# webdriver.py

#%% packages
import requests
from bs4 import BeautifulSoup
from time import sleep
import json
import pandas as pd
import pickle
from pathlib import Path

# webdriver start-up
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def _construct_ids(serie_or_df):
    """
    Used to combine groups, subgroups and translated name to form an ID from a workbook.
    Takes either a (sliced) df or a series (single row) to form the ID(s).

    Returns:
        list of IDs if input is pd.DataFrame
        single ID if input is pd.Series
    """
    if isinstance(serie_or_df, pd.DataFrame):
        df = serie_or_df
        ids = [
            f"{row.group}{row.subgroup}{row.translated_name}"
            for _, row in df.iterrows()
        ]

    elif isinstance(serie_or_df, pd.Series):
        row = serie_or_df
        ids = f"{row.group}{row.subgroup}{row.translated_name}"

    return ids

#%% Definition of the update_etm_inputs

def update_etm_inputs():
    driver = webdriver.Chrome()
    FOLDER = Path(__file__).parent

    #%% obtain links to all slider pages

    # request main page as static
    url = "https://pro.energytransitionmodel.com/scenario/overview/introduction/how-does-the-energy-transition-model-work"
    mainpage = requests.get(url)
    mainsoup = BeautifulSoup(mainpage.content, "html.parser")

    # create a list of all the needed slider links
    links = list()

    for div in mainsoup.find_all("div", attrs={"id": "sidebar"}):
        for link in div.find_all("a"):
            links.append(link.get("href"))

    # remove overview and data tabs
    del links[0]
    del links[-3:]

    #%% extracting slider information of the before collected links of sections

    # using driver due to dynamic nature of ETM (headless not allowed due to FLoC)
    base_url = "https://pro.energytransitionmodel.com"
    sliders_list = list()

    for link in links:

        print()
        print("navigating to: ", link)
        url = base_url + link

        # navigate to url and wait for page to load
        driver.get(url)
        sleep(3)

        # extract sidebar group name
        sidebar = driver.find_element_by_id("sidebar")
        active = sidebar.find_elements_by_class_name("active")
        group = active[-1].find_element_by_class_name("title").text

        # find accordion
        accordion = driver.find_element_by_id("accordion_wrapper")

        # extract the sections
        sections = accordion.find_elements_by_class_name("accordion_element")

        # for each section; extract subgroup name and all meta-data (includes key to be use as input)
        for subsection in sections:

            subgroup = subsection.find_element_by_tag_name("a").text

            sliders = subsection.find_elements_by_class_name("slider")

            for slider in sliders:

                sliderdict = json.loads(slider.get_attribute("data-attrs"))
                sliderdict.update({"group": group, "subgroup": subgroup})

                sliders_list.append(sliderdict)

        print("extracted!")

    # push all information to a dataframe
    df = pd.DataFrame(sliders_list)


    #%% remove some HTML formatting from translated name
    strip_subs = lambda x: str(x).replace("<sub>2</sub>", "2")
    df.translated_name = df.translated_name.apply(strip_subs)

    #%% reformat dupes to unique description for easier API input integration
    dupes = pd.DataFrame(_construct_ids(df)).duplicated()
    df.translated_name.mask(
        dupes, df.translated_name.apply(lambda x: str(x) + " 2"), inplace=True
        )
    df["trans_name"] = _construct_ids(df)

    #%% insert missing values in subgroup based on group
    '''
    This does not show any use as there are no NaNs in the subgroup (or group or translated name)
    There are empty cells in the dataframe.
    If that is a problem, it can be solved differently
    '''
    # nans = df.subgroup.isna()
    # df.subgroup.mask(nans, df.group, inplace=True)

    #%% write to csv and pkl file

    '''
    Changed file names to etm_inputs for a more logical feel
    old name: clean_scraped_inputs.csv (these are just the inputs)
    old name: raw_sliders_list.pkl (is no list)
    '''
    filename = "data/etm_inputs.csv"
    df.to_csv(FOLDER / filename)
    filename = "data/etm_inputs.pkl"
    df.to_pickle(FOLDER / filename)    

# %%
