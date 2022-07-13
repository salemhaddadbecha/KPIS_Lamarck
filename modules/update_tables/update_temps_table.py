# Modules / Dépendances
from tables import Temps
from modules.requests_tools import get_list_of_element
from modules.safe_actions import safe_dict_get, safe_date_convert, dprint,safe_update_table_row, get_period_dates

def get_temps_all_informations(basic_data):
    # Indexation d'éléments utiles:

    # Infos à trouver
    informations = {
        "boond_id": int(),
        "boond_resource_id": int(),
        "date_de_creation": None,
        "duree": float(),
        "type": str(),
        "boond_id_projet": int()
    }

    informations["boond_id"] = safe_dict_get(basic_data, ["id"])
    informations["boond_resource_id"] = safe_dict_get(basic_data, ["relationships", "dependsOn", "data", "id"])
    informations["date_de_creation"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "startDate"]))
    informations["duree"] = safe_dict_get(basic_data, ["attributes", "value"])
    if safe_dict_get(basic_data, ["attributes", "scorecard", "project"]) is not None:
        informations["type"] = "mission"
        informations["boond_id_projet"] = safe_dict_get(basic_data, ["attributes", "scorecard", "project", "id"])
    else:
        informations["type"] = "interne"
        informations["boond_id_projet"] = None

    return informations

def check_new_and_update_temps():
    dates = get_period_dates()

    # New temps -> type = onePeriod (tous les temps créent sur la période)
    # Il y a un élément par mission dans "data", pour chaque élément on vérifie que sa durée est != de 0 (pas utile d'enregistré un temps vide)
    # Un élément par temps renseigné est créé dans la table
    dprint(f"#- New temps: period({dates[0]})")
    list_of_new_temps = get_list_of_element("/reporting-resources", extractType="inDays", period="onePeriod", maxResources=10, startDate=dates[0], endDate=dates[1])
    for temps in list_of_new_temps:

        if safe_dict_get(temps, ["attributes", "value"]) is not None and \
                float(safe_dict_get(temps, ["attributes", "value"])) != float(0):

            new_temps_all_informations = get_temps_all_informations(temps)

            safe_update_table_row(
                table=Temps,
                filters={"boond_id": new_temps_all_informations["boond_id"]},
                boond_id=new_temps_all_informations["boond_id"],
                date_de_creation=new_temps_all_informations["date_de_creation"],
                duree=new_temps_all_informations["duree"],
                type=new_temps_all_informations["type"],
                boond_id_projet=new_temps_all_informations["boond_id_projet"],
                boond_resource_id=new_temps_all_informations["boond_resource_id"]
            )
            dprint(f"#-- Update candidat: {new_temps_all_informations['boond_id']}")

    dprint("\n")