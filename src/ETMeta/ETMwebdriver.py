# webdriver.py
#%% packages
import requests
from bs4 import BeautifulSoup
from time import sleep
import json
import pandas as pd
import pickle

# webdriver start-up
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

driver = webdriver.Chrome()


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
    sleep(2)

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

# push all information to a frame
df = pd.DataFrame(sliders_list)

#%% remove some HTML formatting from translated name
strip_subs = lambda x: str(x).replace("<sub>2</sub>", "2")
df.translated_name = df.translated_name.apply(strip_subs)

# reformat dupes to unique description for easier API input integration
from ETMapi import _construct_ids

dupes = pd.DataFrame(_construct_ids(df)).duplicated()
df.translated_name.mask(
    dupes, df.translated_name.apply(lambda x: str(x) + " 2"), inplace=True
)

# insert missing values in subgroup based on group
nans = df.subgroup.isna()
df.subgroup.mask(nans, df.group, inplace=True)

# write to csv file
df.to_csv("data/clean_scraped_inputs.csv")

#%% store slider_list for future reference
picklefile = open("data/raw_sliders_list.pkl", "wb")
pickle.dump(sliders_list, picklefile)
picklefile.close()
