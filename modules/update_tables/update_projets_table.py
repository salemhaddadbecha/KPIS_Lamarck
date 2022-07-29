# Modules / Dependances
from tables import Projets
# Tools
from tools.requests_tools import get_list_of_element
from tools.safe_actions import safe_dict_get, safe_date_convert, dprint, safe_update_table_row


def get_projet_all_informations(basic_data):
    """
    Permet de recuperer toutes les informations utiles
    d'un projet a partir de ses informations basiques
    :param basic_data:
    :return: informations utiles du projet
    """
    # Infos à trouver
    informations = {
        "boond_id": int(),
        "boond_rm_id": int(),
        "boond_besoin_id": int(),
        "date_de_debut": None,
        "date_de_fin": None
    }
    informations["boond_id"] = safe_dict_get(basic_data, ["id"])
    informations["boond_rm_id"] = safe_dict_get(basic_data, ["relationships", "mainManager", "data", "id"])
    informations["boond_besoin_id"] = safe_dict_get(basic_data, ["relationships", "opportunity", "data", "id"])
    informations["date_de_debut"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "startDate"]))
    informations["date_de_fin"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "endDate"]))

    return informations


def check_new_and_update_projets(day):
    """
    Met à jour et ajoute tous les nouveaux projets à la table Projets:
    :param day:
    :return:
    """
    dprint(f"Update project table", priority_level=3, preprint="\n")
    list_of_projets_to_update = get_list_of_element("/projects", period="updated", startDate=day,
                                                    endDate=day)

    for projet_to_update_basic_informations in list_of_projets_to_update:
        projet_to_update_all_informations = get_projet_all_informations(projet_to_update_basic_informations)
        safe_update_table_row(
            table=Projets,
            filters={"boond_id": projet_to_update_all_informations["boond_id"]},
            boond_id=projet_to_update_all_informations["boond_id"],
            boond_rm_id=projet_to_update_all_informations["boond_rm_id"],
            boond_besoin_id=projet_to_update_all_informations["boond_besoin_id"],
            date_de_debut=projet_to_update_all_informations["date_de_debut"],
            date_de_fin=projet_to_update_all_informations["date_de_fin"]
        )
        dprint(f"Update project: {projet_to_update_all_informations['boond_id']}", priority_level=4)
