# Modules / Dependances
from tables import Candidats
# Tools
from tools.requests_tools import request, get_list_of_element
from tools.safe_actions import safe_dict_get, safe_count_type_of_dict_in_list, safe_date_convert, dprint, \
    safe_update_table_row


def get_candidate_all_informations(basic_data):
    """
    Permet de recuperer toutes les informations utiles
    d'un candidat a partir de ses informations basiques
    :param basic_data:
    :return: informations utiles du candidat
    """
    # Indexation d'elements utiles:
    etape_recrute = 3
    provenance_cv = [
        "jobboard",
        "Site Société",
        "Cooptation Consultant",
        "Cooptation Client",
        "Cooptation Candidat",
        "Reseau Social",
        "Autres",
        "Annonce",
        "Salon",
        "Import",
        "Cooptation Staff",
        "non renseigne"
    ]  # index pour avoir la valeur correspondante / dernier index reserve au non renseigne auquel l'index est de -1

    action_entretien = [12, 133, 134]  # Respectivement, E1, E2, E3
    action_prise_de_contact = 42
    action_prequalification_telephonique = 41
    action_signature = 44

    # Infos à trouver
    informations = {
        "boond_id": int(),
        "boond_rm_id": int(),
        "nom": str(),
        "prenom": str(),
        "date_de_creation": None,
        "date_derniere_maj": None,
        "provenance_cv": str(),
        "commentaire_provenance_cv": str(),
        "recrute": bool(),
        "boond_ressource_id": int(),
        "prise_de_contact": bool(),
        "entretien_1": bool(),
        "entretien_2": bool(),
        "entretien_3": bool(),
        "signature": bool()
    }

    informations["boond_id"] = safe_dict_get(basic_data, ["id"])
    informations["boond_rm_id"] = safe_dict_get(basic_data, ["relationships", "mainManager", "data", "id"])
    informations["nom"] = safe_dict_get(basic_data, ["attributes", "lastName"])
    informations["prenom"] = safe_dict_get(basic_data, ["attributes", "firstName"])
    informations["date_de_creation"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "creationDate"]))
    informations["date_derniere_maj"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "updateDate"]))
    if safe_dict_get(basic_data, ["attributes", "source", "typeOf"]) is not None:
        informations["provenance_cv"] = safe_dict_get(provenance_cv, [
            safe_dict_get(basic_data, ["attributes", "source", "typeOf"])])
    else:
        informations["provenance_cv"] = safe_dict_get(basic_data, ["attributes", "source", "typeOf"])
    informations["commentaire_provenance_cv"] = safe_dict_get(basic_data, ["attributes", "source", "detail"])
    informations["recrute"] = (safe_dict_get(basic_data, ["attributes", "state"]) == etape_recrute)
    if informations["recrute"] is not None:
        details_candidat = request(f"/candidates/{informations['boond_id']}/information")
        informations["boond_ressource_id"] = safe_dict_get(details_candidat,
                                                           ["data", "relationships", "resource", "data", "id"])
    else:
        informations["boond_ressource_id"] = safe_dict_get(basic_data, ["relationships", "resource", "data", "id"])

    # Pour les infos prise_de_contact & recontacte il faut aller voir les actions
    actions = request(f"/candidates/{informations['boond_id']}/actions")
    liste_des_actions = safe_dict_get(actions, ["data"])

    # Si il a eu un entretien, alors il a dejà eu prise de contact et recontacte
    # Entretien 1 (E1)
    if safe_count_type_of_dict_in_list(liste_des_actions, ["attributes", "typeOf"], action_entretien[0]) > 0:
        informations["prise_de_contact"] = True
        informations["entretien_1"] = True

        # Entretien 2 (E2)
        if safe_count_type_of_dict_in_list(liste_des_actions, ["attributes", "typeOf"], action_entretien[1]) > 0:
            informations["entretien_2"] = True

            # Entretien 3 (E3)
            if safe_count_type_of_dict_in_list(liste_des_actions, ["attributes", "typeOf"], action_entretien[2]) > 0:
                informations["entretien_3"] = True

    elif safe_count_type_of_dict_in_list(liste_des_actions, ["attributes", "typeOf"],
                                         [action_prise_de_contact, action_prequalification_telephonique]) > 0:
        informations["prise_de_contact"] = True
        informations["entretien_1"] = False
        informations["entretien_2"] = False
        informations["entretien_3"] = False

    else:
        informations["prise_de_contact"] = False
        informations["entretien_1"] = False
        informations["entretien_2"] = False
        informations["entretien_3"] = False

    informations["signature"] = False
    if safe_count_type_of_dict_in_list(liste_des_actions, ["attributes", "typeOf"], action_signature) > 0:
        informations["signature"] = True

    return informations


def check_new_and_update_candidates(start_date, end_date):
    """
    Met à jour et ajoute tous les nouveaux candidats à la table Candidats:
    :param start_date:
    :param end_date:
    :return:
    """
    dprint(f"Update candidates table", priority_level=3, preprint="\n")
    list_of_candidates_to_update = get_list_of_element("/candidates", period="updated", startDate=start_date,
                                                       endDate=end_date)

    for candidate_to_update_basic_informations in list_of_candidates_to_update:
        candidate_to_update_all_informations = get_candidate_all_informations(candidate_to_update_basic_informations)

        safe_update_table_row(
            table=Candidats,
            filters={"boond_id": candidate_to_update_all_informations["boond_id"]},
            boond_id=candidate_to_update_all_informations["boond_id"],
            boond_rm_id=candidate_to_update_all_informations["boond_rm_id"],
            nom=candidate_to_update_all_informations["nom"],
            prenom=candidate_to_update_all_informations["prenom"],
            date_de_creation=candidate_to_update_all_informations["date_de_creation"],
            date_derniere_maj=candidate_to_update_all_informations["date_derniere_maj"],
            provenance_cv=candidate_to_update_all_informations["provenance_cv"],
            commentaire_provenance_cv=candidate_to_update_all_informations["commentaire_provenance_cv"],
            recrute=candidate_to_update_all_informations["recrute"],
            boond_ressource_id=candidate_to_update_all_informations["boond_ressource_id"],
            prise_de_contact=candidate_to_update_all_informations["prise_de_contact"],
            entretien_1=candidate_to_update_all_informations["entretien_1"],
            entretien_2=candidate_to_update_all_informations["entretien_2"],
            entretien_3=candidate_to_update_all_informations["entretien_3"],
            signature=candidate_to_update_all_informations["signature"]
        )

        dprint(
            f"Update candidat: {candidate_to_update_all_informations['nom']} {candidate_to_update_all_informations['prenom']}",
            priority_level=4)
