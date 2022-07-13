# Modules / Dépendances
from tables import Ressources
from modules.requests_tools import request, get_list_of_agencies, get_list_of_element
from modules.safe_actions import safe_dict_get, safe_date_convert, dprint, safe_update_table_row, get_period_dates

def get_resource_all_informations(basic_data, list_of_agencies):
    # Indexation d'éléments utiles:
    liste_sexe = ["homme", "femme"]
    liste_profil_rm = ["manager", "dg", "directeur"]
    liste_etats = ["out", "en mission", "en interne", "en arrêt", "signé"]
    # Infos à trouver
    informations = {
        "boond_id": int(),
        "boond_rm_id": int(),
        "date_de_creation": None,
        "nom": str(),
        "prenom": str(),
        "sexe": str(),
        "agence": str(),
        "profil": str(),
        "est_rm": bool(),
        "date_de_recrutement": None,
    }

    informations["boond_id"] = safe_dict_get(basic_data, ["id"])
    informations["boond_rm_id"] = safe_dict_get(basic_data, ["relationships", "mainManager", "data", "id"])
    informations["date_de_creation"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "creationDate"]))
    informations["nom"] = safe_dict_get(basic_data, ["attributes", "lastName"])
    informations["prenom"] = safe_dict_get(basic_data, ["attributes", "firstName"])
    informations["sexe"] = safe_dict_get(liste_sexe, [safe_dict_get(basic_data, ["attributes", "civility"])])

    if safe_dict_get(basic_data, ["relationships", "agency", "data", "id"]) is not None:
        informations["agence"] = safe_dict_get(list_of_agencies, [int(safe_dict_get(basic_data, ["relationships", "agency", "data", "id"]))-1])
    else:
        informations["agence"] = None

    if safe_dict_get(basic_data, ["attributes", "state"]):
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

    # Pour avoir la date de recrutement, il faut faire une requête de plus
    administrative_informations = request(f"/resources/{informations['boond_id']}/administrative")
    debut_premier_contrat = None
    if safe_dict_get(administrative_informations, ["data", "relationships", "contracts", "data", -1, "id"]):
        id_premier_contrat = safe_dict_get(administrative_informations, ["data", "relationships", "contracts", "data", -1, "id"])
        premier_contrat = request(f"/contracts/{id_premier_contrat}")
        debut_premier_contrat = safe_dict_get(premier_contrat, ["data", "attributes", "startDate"])

    informations["date_de_recrutement"] = safe_date_convert(debut_premier_contrat)

    return informations


def check_new_and_update_resources():
    list_of_agencies = get_list_of_agencies()
    dates = get_period_dates()

    # Update resource -> type = updated
    dprint(f"#- Update resource: period({dates[0]})")
    list_of_resources_to_update = get_list_of_element("/resources", period="updated", startDate=dates[0], endDate=dates[1])

    for resource_to_update_basic_informations in list_of_resources_to_update:
        resource_to_update_all_informations = get_resource_all_informations(resource_to_update_basic_informations, list_of_agencies)

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
            est_rm=resource_to_update_all_informations["est_rm"],
            date_de_recrutement=resource_to_update_all_informations["date_de_recrutement"]
        )
        dprint(f"#-- Update resource: {resource_to_update_all_informations['nom']} {resource_to_update_all_informations['prenom']}")

    dprint("\n")