# Modules / Dépendances
from tables import Prestations
from modules.requests_tools import request, get_list_of_element
from modules.safe_actions import safe_dict_get, safe_date_convert, dprint, safe_update_table_row, get_period_dates

def get_prestation_all_informations(basic_data):
    # Indexation d'éléments utiles:
    etats = ["signé", "prévisionnelle"]
    informations = {
        "boond_id": int(),
        "boond_resource_id": int(),
        "date_de_debut": None,
        "date_de_fin": None,
        "etat": str(),
        "ca_ht": float(),
        "ca_realise": float(),
        "ca_previsionnel": float()
    }
    informations["boond_id"] = safe_dict_get(basic_data, ["id"])
    informations["boond_resource_id"] = safe_dict_get(basic_data, ["relationships", "dependsOn", "data", "id"])
    informations["date_de_debut"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "startDate"]))
    informations["date_de_fin"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "endDate"]))

    # Pour la suite il faut l'état de la prestation
    prestation = request(f"/deliveries/{informations['boond_id']}")

    if safe_dict_get(prestation, ["data", "attributes", "state"]) is not None:
        informations["etat"] = etats[ int(safe_dict_get(prestation, ["data", "attributes", "state"])) ]

        if informations["etat"] == "prévisionnelle":
            informations["ca_previsionnel"] = safe_dict_get(prestation, ["data", "attributes", "turnoverSimulatedExcludingTax"])

        elif informations["etat"] == "signé":
            informations["ca_ht"] = safe_dict_get(prestation, ["data", "attributes", "turnoverSimulatedExcludingTax"])

    # TODO: Calcul CA prévisionnel : nb jour * TJM (nb jour où trouver ? pour le moment: % d'occupation * nb jours commandés)
    # TODO: gérer pour les forfaits !!
    nb_jours_consommes = 1 # à changer
    informations["ca_realise"] = safe_dict_get(prestation, ["data", "attributes", "averageDailyPriceExcludingTax"]) * nb_jours_consommes

    return informations


def check_new_and_update_prestations():
    dates = get_period_dates()


    # Update prestation -> type = updated
    dprint(f"#- Update prestation: period({dates[0]})")
    list_of_prestations_to_update = get_list_of_element("/deliveries-groupments", period="updated", startDate=dates[0], endDate=dates[1])

    for prestation_to_update_basic_informations in list_of_prestations_to_update:
        prestation_to_update_all_informations = get_prestation_all_informations(prestation_to_update_basic_informations)

        safe_update_table_row(
            table=Prestations,
            filters={"boond_id": prestation_to_update_all_informations["boond_id"]},
            boond_id=prestation_to_update_all_informations["boond_id"],
            boond_resource_id=prestation_to_update_all_informations["boond_resource_id"],
            date_de_debut=prestation_to_update_all_informations["date_de_debut"],
            date_de_fin=prestation_to_update_all_informations["date_de_fin"],
            etat=prestation_to_update_all_informations["etat"]
        )
        dprint(f"#-- Update candidat: {prestation_to_update_all_informations['boond_id']}")

    dprint("\n")