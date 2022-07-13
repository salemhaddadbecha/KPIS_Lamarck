# Librairies
import json
import requests
from requests.auth import HTTPBasicAuth
from time import sleep

# Modules / Dépendances
from configuration import APP_CONFIG

def request(endpoint, **query_params):
    param = endpoint

    if bool(query_params):
        param += "?"
        for key, value in query_params.items():
            param += ("&" + key + "=" + str(value))
    print(param)
    response = None
    while True:
        try:
            response = requests.get(APP_CONFIG.BOONDMANAGER_API_URL + param, auth=HTTPBasicAuth(APP_CONFIG.BOONDMANAGER_API_LOGIN, APP_CONFIG.BOONDMANAGER_API_PASSWORD))
            if response.ok:
                response = json.loads(response.text)
                break
        except:
            sleep(5)
            response = requests.get(APP_CONFIG.BOONDMANAGER_API_URL + param, auth=HTTPBasicAuth(APP_CONFIG.BOONDMANAGER_API_LOGIN, APP_CONFIG.BOONDMANAGER_API_PASSWORD))
            if response.ok:
                response = json.loads(response.text)
                break

    return response

def get_list_of_agencies():
    # Index retourné par l'api - 1 = index de l'agence dans la list
    response_json = request("/agencies")
    return [agence["attributes"]["name"] for agence in response_json["data"]]

def get_list_of_element(endpoint, **params):
    from modules.safe_actions import safe_dict_get
    page = 1
    list_of_elements = []
    while True:
        params["maxResults"] = 500
        params["page"] = page
        elements = request(endpoint, **params)

        print(page)
        if elements and len(safe_dict_get(elements, ["data"])) > 0:
            list_of_elements += safe_dict_get(elements, ["data"])
            page += 1
        else:
            break
    return list_of_elements