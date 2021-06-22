# consistency-check.py
from time import sleep
import requests

burl = "https://engine.energytransitionmodel.com/api/v3"
inputs = "/inputs"
test_variable1 = "households_number_of_inhabitants"
test_variable2 = "transport_cars_share"
rest = 60*5 # 5 min pause between calls

results = dict()
for i in range(10):
    r = requests.get(burl + inputs)
    d = r.json()
    tv1 = d[test_variable1]["default"]
    tv2 = d[test_variable2]["default"]

    results.update({f't{i}': {test_variable1: tv1, test_variable2: tv2}})
    sleep(rest)
