# Modules / Dependances
from tables import Temps
# Tools
from tools.requests_tools import get_list_of_element
from tools.safe_actions import safe_dict_get, safe_date_convert, dprint, safe_update_table_row


def get_temps_all_informations(basic_data):
    """
    Permet de recuperer toutes les informations utiles
    d'un temps a partir de ses informations basiques
    :param basic_data:
    :return: informations utiles du temps
    """
    # Indexation d'elements utiles:

    # Infos à trouver
    informations = {
        "boond_id": str(),
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
    if safe_dict_get(basic_data, ["attributes", "scorecard", "reference"]) == "durationOfProductionUsedTimePerProjects":
        informations["type"] = "mission"
        informations["boond_id_projet"] = safe_dict_get(basic_data, ["attributes", "scorecard", "project", "id"])

    elif safe_dict_get(basic_data, ["attributes", "scorecard", "reference"]) == "durationOfInternalUsedTime":
        informations["type"] = "interne"
        informations["boond_id_projet"] = None

    elif safe_dict_get(basic_data, ["attributes", "scorecard", "reference"]) == "durationOfAbsencesUsedTime":
        informations["type"] = "absence"
        informations["boond_id_projet"] = None

    return informations


def check_new_and_update_temps(day):
    """
    Met à jour et ajoute tous les nouveaux temps à la table Temps:
    :param day:
    :return:
    """
    dprint(f"Update temps table", priority_level=3, preprint="\n")

    list_of_new_temps = get_list_of_element("/reporting-resources", extractType="inDays", period="onePeriod",
                                            maxResources=10, startDate=day, endDate=day)
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
            dprint(f"Update candidat: {new_temps_all_informations['boond_id']}", priority_level=4)
