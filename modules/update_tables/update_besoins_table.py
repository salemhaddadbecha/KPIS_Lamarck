# Modules / Dependances
from tables import Besoins
# Tools
from tools.requests_tools import request, get_list_of_element, get_list_of_agencies
from tools.safe_actions import safe_dict_get, safe_date_convert, dprint, safe_update_table_row


def get_besoin_all_informations(basic_data):
    """
    Permet de recuperer toutes les informations utiles
    d'un besoin a partir de ses informations basiques
    :param basic_data:
    :return: informations utiles du besoin
    """
    # Indexation d'elements utiles:
    list_etats = ["Piste", "Draaae", "Perdu", "Abandonnee", "En cours", "5", "Soutenance", "ADR", "8", "Reporte",
                  "non renseigné"]

    # Infos à trouver
    informations = {
        "boond_id": int(),
        "boond_rm_id": int(),
        "boond_contact_id": int(),
        "date_de_creation": None,
        "etat": str(),
        "date_maj_drae": None,
        "est_interne": bool()
    }

    informations["boond_id"] = safe_dict_get(basic_data, ["id"])
    informations["boond_rm_id"] = safe_dict_get(basic_data, ["relationships", "mainManager", "data", "id"])
    informations["boond_contact_id"] = safe_dict_get(basic_data, ["relationships", "contact", "data", "id"])
    informations["date_de_creation"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "creationDate"]))
    if safe_dict_get(basic_data, ["attributes", "state"]) is not None:
        informations["etat"] = safe_dict_get(list_etats, [int(safe_dict_get(basic_data, ["attributes", "state"]))])
        # date_maj_drae
        if informations["etat"] == "Draaae":
            # date de la maj à drae est la date de creation du projet associe
            besoin_projet = request(f"/opportunities/{informations['boond_id']}/projects")
            besoin_projet_debut = safe_dict_get(besoin_projet, ["data", -1, "attributes", "startDate"])
            informations["date_maj_drae"] = safe_date_convert(besoin_projet_debut)
    else:
        informations["etat"] = None
        informations["date_maj_drae"] = None

    # Vérification des refacturations: si contient refacturation ET un noms de l'une des agences
    titre = safe_date_convert(safe_dict_get(basic_data, ["attributes", "title"]))
    informations["est_interne"] = False
    if "refacturation" in titre.lower():
        for agence in get_list_of_agencies():
            if agence.lower() in titre.lower():
                informations["est_interne"] = True

    return informations


def check_new_and_update_besoins(start_date, end_date):
    """
    Met à jour et ajoute tous les nouveaux besoins à la table Besoins:
    :param start_date:
    :param end_date:
    :return:
    """
    dprint(f"Update besoin table", priority_level=3, preprint="\n")
    list_of_besoins_to_update = get_list_of_element("/opportunities", period="updated", startDate=start_date,
                                                    endDate=end_date)

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
            date_maj_drae=besoin_to_update_all_informations["date_maj_drae"],
            est_interne=besoin_to_update_all_informations["est_interne"]
        )
        dprint(f"Update besoin: {besoin_to_update_all_informations['boond_id']}", priority_level=4)
