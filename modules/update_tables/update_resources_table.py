# Modules / Dependances
from tables import Ressources
# Tools
from tools.requests_tools import request, get_list_of_agencies, get_list_of_element
from tools.safe_actions import safe_dict_get, safe_date_convert, dprint, safe_update_table_row


def get_resource_all_informations(basic_data, list_of_agencies):
    """
    Permet de recuperer toutes les informations utiles
    d'une ressource a partir de ses informations basiques
    :param basic_data:
    :return: informations utiles de la ressource
    """
    # Indexation d'elements utiles:
    liste_sexe = ["homme", "femme"]
    liste_profil_rm = [
        "business",
        "dg",
        "directeur",
        "drh",
        "responsable",
        "gerant",
        "gerant",
        "ressources humaines",
        "recrutement"
    ]
    list_type = ["Consultant Interne", "Consultant Externe", "Comptabilite", "Business Manager", "Associe",
                 "Recrutement / RH", "DRH", "DAF", "0", "non renseigne"]
    liste_etats = ["out", "en mission", "en interne", "en arrêt", "signe", "non renseigne"]
    # Infos à trouver
    informations = {
        "boond_id": int(),
        "boond_rm_id": int(),
        "date_de_creation": None,
        "nom": str(),
        "prenom": str(),
        "sexe": str(),
        "agence": str(),
        "etat": str(),
        "profil": str(),
        "type": str(),
        "est_rm": bool(),
        "date_de_recrutement": None,
        "debut_derniere_prestation": None,
        "fin_derniere_prestation": None,
    }

    informations["boond_id"] = safe_dict_get(basic_data, ["id"])
    informations["boond_rm_id"] = safe_dict_get(basic_data, ["relationships", "mainManager", "data", "id"])
    informations["date_de_creation"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "creationDate"]))
    informations["nom"] = safe_dict_get(basic_data, ["attributes", "lastName"])
    informations["prenom"] = safe_dict_get(basic_data, ["attributes", "firstName"])
    informations["sexe"] = safe_dict_get(liste_sexe, [safe_dict_get(basic_data, ["attributes", "civility"])])

    if safe_dict_get(basic_data, ["relationships", "agency", "data", "id"]) is not None:
        informations["agence"] = safe_dict_get(list_of_agencies, [
            int(safe_dict_get(basic_data, ["relationships", "agency", "data", "id"])) - 1])
    else:
        informations["agence"] = None

    if safe_dict_get(basic_data, ["attributes", "state"]) is not None:
        informations["etat"] = safe_dict_get(liste_etats, [int(safe_dict_get(basic_data, ["attributes", "state"]))])
    else:
        informations["etat"] = None

    informations["profil"] = safe_dict_get(basic_data, ["attributes", "title"])
    if informations["profil"] is not None:
        informations["est_rm"] = False
        profil = informations["profil"].lower()
        for profil_rm in liste_profil_rm:
            if profil_rm in profil:
                informations["est_rm"] = True
                break
    else:
        informations["est_rm"] = None

    informations["type"] = safe_dict_get(list_type, [safe_dict_get(basic_data, ["attributes", "typeOf"])])

    # Pour avoir la date de recrutement, il faut faire une requête de plus
    administrative_informations = request("/resources/{}/administrative".format(informations['boond_id']))
    resource_prestations = request("/resources/{}/deliveries-inactivities".format(informations['boond_id']))
    if safe_dict_get(resource_prestations, ['data']) and len(safe_dict_get(resource_prestations, ['data'])) > 0:
        last_prestation = safe_dict_get(resource_prestations, ['data'])[0]
        informations["debut_derniere_prestation"] = safe_dict_get(last_prestation, ['attributes', 'startDate'])
        informations["fin_derniere_prestation"] = safe_dict_get(last_prestation, ['attributes', 'endDate'])
    debut_premier_contrat = None
    if safe_dict_get(administrative_informations, ["data", "relationships", "contracts", "data", -1, "id"]):
        id_premier_contrat = safe_dict_get(administrative_informations,
                                           ["data", "relationships", "contracts", "data", -1, "id"])
        premier_contrat = request("/contracts/{}".format(id_premier_contrat))
        debut_premier_contrat = safe_dict_get(premier_contrat, ["data", "attributes", "startDate"])

    informations["date_de_recrutement"] = safe_date_convert(debut_premier_contrat)

    return informations


def check_new_and_update_resources(start_day, end_day):
    """
    Met à jour et ajoute toutes les nouvelles ressources à la table Ressources:
    :param day:
    :return:
    """
    list_of_agencies = get_list_of_agencies()

    dprint("Update resource table", priority_level=3, preprint="\n")
    list_of_resources_to_update = get_list_of_element(
        "/resources",
        period="updated",
        startDate=start_day,
        endDate=end_day
    )
    if 'data' in list_of_resources_to_update and list_of_resources_to_update['data']:
        for resource_to_update_basic_informations in list_of_resources_to_update['data']:
            resource_to_update_all_informations = get_resource_all_informations(resource_to_update_basic_informations,
                                                                                list_of_agencies)

            safe_update_table_row(
                table=Ressources,
                filters={"boond_id": resource_to_update_all_informations["boond_id"]},
                boond_id=resource_to_update_all_informations["boond_id"],
                boond_rm_id=resource_to_update_all_informations["boond_rm_id"],
                date_de_creation=resource_to_update_all_informations["date_de_creation"],
                nom=resource_to_update_all_informations["nom"],
                prenom=resource_to_update_all_informations["prenom"],
                sexe=resource_to_update_all_informations["sexe"],
                agence=resource_to_update_all_informations["agence"],
                etat=resource_to_update_all_informations["etat"],
                profil=resource_to_update_all_informations["profil"],
                type=resource_to_update_all_informations["type"],
                est_rm=resource_to_update_all_informations["est_rm"],
                date_de_recrutement=resource_to_update_all_informations["date_de_recrutement"],
                debut_derniere_prestation=resource_to_update_all_informations["debut_derniere_prestation"],
                fin_derniere_prestation=resource_to_update_all_informations["fin_derniere_prestation"],
            )
            dprint(
                "Update resource: {} {}".format(
                    resource_to_update_all_informations['nom'],
                    resource_to_update_all_informations['prenom']
                ),
                priority_level=4)
    else:
            dprint(f"No data found for the period {start_day} to {end_day}", priority_level=3)
