# Modules / Dependances
from tables import Prestations, Temps
# Tools
from tools.requests_tools import request, get_list_of_element
from tools.safe_actions import safe_dict_get, safe_date_convert, dprint, safe_update_table_row, safe_table_read


def get_prestation_all_informations(basic_data):
    """
    Permet de recuperer toutes les informations utiles
    d'une prestation a partir de ses informations basiques
    :param basic_data:
    :return: informations utiles de la prestation
    """

    def _get_temps_consomme(project_id):
        """
        Permet de recuperer la somme des temps consommes sur le projet
        de tous les consultants travaillant dessus
        :param project_id:
        :return: somme des temps consommes
        """
        temps_consomme = float(0)
        rows = safe_table_read(Temps, {"boond_id_projet": project_id})
        if rows is not None:
            for row in rows:
                temps_consomme += float(row.duree)

        return temps_consomme

    # Indexation d'elements utiles:
    etats = ["signe", "previsionnelle"]
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

    # Pour la suite il faut l'etat de la prestation
    prestation = request(f"/deliveries/{informations['boond_id']}")

    if safe_dict_get(prestation, ["data", "attributes", "state"]) is not None:
        informations["etat"] = etats[int(safe_dict_get(prestation, ["data", "attributes", "state"]))]

        if informations["etat"] == "previsionnelle":
            informations["ca_previsionnel"] = safe_dict_get(prestation,
                                                            ["data", "attributes", "turnoverSimulatedExcludingTax"])

        elif informations["etat"] == "signe":
            informations["ca_ht"] = safe_dict_get(prestation, ["data", "attributes", "turnoverSimulatedExcludingTax"])

    # TODO: gerer pour les forfaits !!
    # Calcul du CA réalisé: nb de jours passés (temps consommés) * prix à la journée
    temps_consomme = _get_temps_consomme(safe_dict_get(prestation, ["data", "relationships", "project", "data", "id"]))
    informations["ca_realise"] = safe_dict_get(prestation,
                                               ["data", "attributes", "averageDailyPriceExcludingTax"]) * temps_consomme

    return informations


def check_new_and_update_prestations(day):
    """
    Met à jour et ajoute toutes les nouvelles prestations à la table Prestations:
    :param day:
    :return:
    """
    dprint(f"Update prestation table", priority_level=3, preprint="\n")
    list_of_prestations_to_update = get_list_of_element("/deliveries-groupments", period="updated",
                                                        startDate=day, endDate=day)

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
        dprint(f"Update candidat: {prestation_to_update_all_informations['boond_id']}", priority_level=4)
