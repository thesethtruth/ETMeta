import requests
import json
from datetime import datetime
import pandas as pd
import os.path
from warnings import warn

def area_codes(outputformat='list', filepath=None, refresh=False, save_csv=True):
    """
    Use ETM v3 API to request all areas and from that extract only the area codes, to use in 
    other ETM v3 API reuqests. 

    arguments:
        outputformat:
            list            returns only the area codes as list
            dataframe       returns only the area codes as pandas dataframe
            json            returns response.content 
            response        returns response as request object
        filepath:
            specify location to save to / read from (default: /etm_ref/)
        refresh:
            specify true to force refresh, checks for existing file on path location to prevent
            errors from trying to load non-existing files
        save_cvs:
            caches the api response to a csv to speed up the process if called again.

    returns (defined by outputformat argument)
        list 
        pandas dataframe
        json
        request response object
    """

    if filepath is None:
        filepath = 'etm_ref/areacodes.csv'

    if refresh or not os.path.isfile(filepath):
        request_url = "https://engine.energytransitionmodel.com/api/v3/areas/"
        response = requests.get(request_url)
        response_list = json.loads(response.content)
        areas = list()
        for item in response_list:
            areas.append(item['area'])

        df = pd.DataFrame(areas, columns = ['area_codes'])

        if save_csv:
            df.to_csv(filepath)

    else:
        df = pd.read_csv(filepath, index_col=0)
    
    if outputformat == "list":
        areas = list(df.values.flatten())
    elif outputformat == "dataframe":
        areas = df
    elif outputformat == "json":
        areas = response.content
    elif outputformat == 'response':
        areas = response

    return areas

def get_area_settings(area_code):
    """
    Gets the area settings based on the area code.

    argument:
        area_code (as defined by ETM)

    returns:
        requests response object
    """

    request_url = f"https://engine.energytransitionmodel.com/api/v3/areas/{area_code}"
    response = requests.get(request_url)

    return response



def create_scenario(area_code, title, end_year, source="api-WB", scenario_id=None, verbose=True):
    """
    POST-method to create a scenario in ETM using ETM v3 API. Converts non-strings to strings. 
    Pushes the setup as json in correct format voor ETM v3 API.

    arguments:
        area_code (optional, one of the existing area codes (use etm.area_codes() to obtain))
        title (title of scenario)
        end_year (interger end year)
        source (paper trail, recommended to use)
        scenario_id (refference scenario)
        verbose (false turns off all print and warn)
    
    returns:
        requests response object
    """
    
    headers = {
        'Content-Type': 'application/json',
    }

    scenario_setup = {
        "scenario": 
            {
                "area_code": str(area_code),
                "title": str(title), 
                "end_year": str(end_year),
                "source": str(source),
                "scenario_id": None,
        }}

    post_url = "https://engine.energytransitionmodel.com/api/v3/scenarios"
    response = requests.post(post_url, json=scenario_setup, headers=headers)

    if response.status_code == 200 and verbose:

        api_url = json.loads(response.content)['url']
        scenario_number = api_url.split("/")[-1]
        browse_url = "https://pro.energytransitionmodel.com/scenarios/"

        print()
        print("Browsable URL to scenario:")
        print(browse_url+scenario_number)

    if not response.status_code == 200 and verbose:
        warn(f"Response not succesful: {response.status_code}")

    return response


def get_all_inputs(outputformat='list', scenario_id=None):
    """

    """
    if scenario_id is not None:
        request_url = f"https://engine.energytransitionmodel.com/api/v3/scenarios/{scenario_id}/inputs"
    else:
        request_url = "https://engine.energytransitionmodel.com/api/v3/inputs"
    
    response = requests.get(request_url)
    response_dict = json.loads(response.content)

    if outputformat=='list':
        inputs = list(json.loads(response.content).keys())
    elif outputformat=='dataframe':
        inputs = pd.DataFrame(index=json.loads(response.content).keys())
    elif outputformat=='response':
        inputs = response
    elif outputformat=='csv':
        inputs = None
        print("Not available through this function; use 'etm.generate_input_worksheet' instead.")
    
    if not response.status_code == 200:
        warn(f"Response not succesful: {response.status_code}")

    return inputs


def get_single_input(input_code):

    request_url = f"https://engine.energytransitionmodel.com/api/v3/inputs/{input_code}"
    response = requests.get(request_url)
    response_dict = json.loads(response.content)

    if not response.status_code == 200:
        raise ValueError(f"Response not succesful: {response.status_code}")
        # here we raise error to prevent running generate_input_worksheet with silent errors

    return response_dict    


def generate_input_worksheet(overwrite=False, filepath='etm_ref/api_raw_inputs.csv',scenario_id=None):
    
    if overwrite or not os.path.isfile(filepath):

        print()
        print("Filepath does not exist or overwriting is forced; Warning; this takes time.")

        inputs = get_all_inputs(scenario_id=scenario_id)
        input_keys = list(get_single_input(inputs[0]).keys())
        df = pd.DataFrame(columns=input_keys)


        for item in inputs:
            _df = pd.DataFrame.from_dict(data= {item: get_single_input(item)}, orient="index")
            df = pd.concat([df, _df])

        df.to_csv(filepath)
    else:
        df = pd.read_csv(filepath, index_col=0)    
    
    return df