# Librairies
import json
from time import sleep

import requests
from requests.auth import HTTPBasicAuth

# Modules / Dépendances
from configuration import APP_CONFIG
# Tools
from tools.safe_actions import safe_dict_get, dprint


def request(endpoint, **query_params):
    """
    Permet de faire une requête à l'API de BoondManager
    tout en y passant autant de paramètre que l'on souhaite
    :param endpoint:
    :param query_params:
    :return: reponse de la requête au format dict()
    """
    param = endpoint

    if bool(query_params):
        param += "?"
        for key, value in query_params.items():
            param += ("&" + key + "=" + str(value))
    dprint(f"Endpoint requested: {param}", priority_level=4)

    response = None
    while True:
        try:
            response = requests.get(APP_CONFIG.BOONDMANAGER_API_URL + param,
                                    auth=HTTPBasicAuth(APP_CONFIG.BOONDMANAGER_API_LOGIN,
                                                       APP_CONFIG.BOONDMANAGER_API_PASSWORD))
            if response.ok:
                response = json.loads(response.text)
                break
            else:
                print(f"ERROR, Code erreur de la requete: {response}")
        except:
            sleep(5)
            response = requests.get(APP_CONFIG.BOONDMANAGER_API_URL + param,
                                    auth=HTTPBasicAuth(APP_CONFIG.BOONDMANAGER_API_LOGIN,
                                                       APP_CONFIG.BOONDMANAGER_API_PASSWORD))
            if response.ok:
                response = json.loads(response.text)
                break

    return response


def get_list_of_agencies():
    """
    Permet de récupérer la liste des agences Lamarck
    :return: liste des agences Lamarack
    """
    # Index retourné par l'api - 1 = index de l'agence dans la list
    response_json = request("/agencies")
    return [agence["attributes"]["name"] for agence in response_json["data"]]


def get_list_of_element(endpoint, **params):
    """
    Permet de faire une requête à l'API de BoondManager
    tout en y passant autant de paramètre que l'on souhaite.
    A utiliser lorsque plusieurs resultats sont attendu, car
    cette fonction va les assembler en une liste
    :param endpoint:
    :param query_params:
    :return: reponse de la requête au format dict()
    """
    page = 1
    list_of_elements = []
    while True:
        params["maxResults"] = 500
        params["page"] = page
        elements = request(endpoint, **params)

        dprint(f"Page number: {page}", priority_level=5)
        if elements and len(safe_dict_get(elements, ["data"])) > 0:
            list_of_elements += safe_dict_get(elements, ["data"])
            page += 1
        else:
            break
    return list_of_elements
