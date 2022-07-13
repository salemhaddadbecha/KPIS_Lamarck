# Modules / Dépendances
from tables import Besoins
from modules.requests_tools import request, get_list_of_element
from modules.safe_actions import safe_dict_get, safe_date_convert, dprint, safe_update_table_row, get_period_dates

def get_besoin_all_informations(basic_data):
    # Indexation d'éléments utiles:
    # TODO: Trouver les index manquant (il est sensé en manquer que 1)
    list_etats = ["Piste", "Draaaé", "Perdu", "Abandonnée", "En cours", "5", "Soutenance", "7", "8", "Reporté"]

    # Infos à trouver
    informations = {
        "boond_id": int(),
        "boond_rm_id": int(),
        "boond_contact_id": int(),
        "date_de_creation": None,
        "etat": str(),
        "date_maj_drae": None
    }

    informations["boond_id"] = safe_dict_get(basic_data, ["id"])
    informations["boond_rm_id"] = safe_dict_get(basic_data, ["relationships", "mainManager", "data", "id"])
    informations["boond_contact_id"] = safe_dict_get(basic_data, ["relationships", "contact", "data", "id"])
    informations["date_de_creation"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "creationDate"]))
    if safe_dict_get(basic_data, ["attributes", "state"]) is not None:
        informations["etat"] = safe_dict_get(list_etats, [int(safe_dict_get(basic_data, ["attributes", "state"]))])
        # date_maj_drae
        if informations["etat"] == "Draaaé":
            # date de la maj à draé est la date de création du projet associé
            besoin_projet = request(f"/opportunities/{informations['boond_id']}/projects")
            besoin_projet_debut = safe_dict_get(besoin_projet, ["data", -1, "attributes", "startDate"])
            informations["date_maj_drae"] = safe_date_convert(besoin_projet_debut)
    else:
        informations["etat"] = None
        informations["date_maj_drae"] = None

    return informations


def check_new_and_update_besoins():
    dates = get_period_dates()

    # Update besoin -> type = updated
    dprint(f"#- Update besoin: period({dates[0]})")
    list_of_besoins_to_update = get_list_of_element("/opportunities", period="updated", startDate=dates[0], endDate=dates[1])

    for besoin_to_update_basic_informations in list_of_besoins_to_update:
        besoin_to_update_all_informations = get_besoin_all_informations(besoin_to_update_basic_informations)

        safe_update_table_row(
            table=Besoins,
            filters={"boond_id": besoin_to_update_all_informations["boond_id"]},
            boond_id=besoin_to_update_all_informations["boond_id"],
            boond_rm_id=besoin_to_update_all_informations["boond_rm_id"],
            boond_contact_id=besoin_to_update_all_informations["boond_contact_id"],
            date_de_creation=besoin_to_update_all_informations["date_de_creation"],
            etat=besoin_to_update_all_informations["etat"],
            date_maj_drae=besoin_to_update_all_informations["date_maj_drae"]
        )
        dprint(f"#-- Update besoin: {besoin_to_update_all_informations['boond_id']}")

    dprint("\n")