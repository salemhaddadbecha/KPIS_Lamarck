# Librairie
from datetime import datetime

# Modules / Dependances
from tables import Controle_qualite
from tools.database_functions import get_last_week_updated_candidates, get_all_resource_as_dict, \
    get_candidates_actions_as_dict
# Tools
from tools.safe_actions import safe_update_table_row, dprint


def controle_1(element, actions_dict):
    """
    Point de controle 1: Extraction des personnes qui ont ete modifiees ou creees
    dans la semaine sans action saisie
    :param element:
    :return:
    """

    def _are_there_any_actions_created(element, actions_dict):
        """
        Permet de savoit si des nouvelles actions ont ete creees sur l'element
        :param element:
        :return: nouvelles actions (boolean)
        """

        # Fonctionne pour les candidats et les resources
        return True if actions_dict.get(element.boond_id) else False


    check = _are_there_any_actions_created(element, actions_dict)

    defaut = "Défaut KPI1: Le candidat {} {} a été créé sans aucune action saisie.".format(
        element.nom,
        element.prenom
    )
    if not check:
        safe_update_table_row(
            table=Controle_qualite,
            filters={"id_correspondant": element.boond_id,
                     "nom_table_correspondante": 'candidates',
                     "defaut": defaut},
            defaut=defaut,
            date_releve=datetime.now().date().strftime('%Y-%m-%d'),
            nom_table_correspondante='candidates',
            est_corrige=False,
            id_correspondant=element.boond_id
        )
        dprint("[{}] {}".format(element.boond_id, defaut), priority_level=4)
    else:
        safe_update_table_row(
            table=Controle_qualite,
            filters={"id_correspondant": element.boond_id,
                     "nom_table_correspondante": 'candidates',
                     "defaut": defaut},
            est_corrige=True,
        )


def controle_2(element, resources_dict):
    """
    Point de controle 2: Extraire toutes les personnes qui ont ete modifiees
    dans la semaine avec un sourceur qui n’est plus dans le groupe Lamarck
    :param element:
    :return:
    """

    def _is_manager_out(element, resources_dict):
        """
        Permet de recuperer l'etat du manager de l'element, et de savoit s'il est OUT
        :param element:
        :return: (boolean) true si manager  est out ou equivalent
        """
        manager_data = resources_dict.get(element.boond_rm_id)

        liste_etats = ["out", "en arrêt"]
        if not manager_data or manager_data.etat in liste_etats:
            return True


    is_out = _is_manager_out(element, resources_dict)

    defaut = "Défaut KPI1: Le candidat {} {} est modifié dans la semaine mais son sourceur n'est " \
             "plus dans le groupe Lamarck.".format(
        element.nom,
        element.prenom
    )
    if is_out:
        safe_update_table_row(
            table=Controle_qualite,
            filters={"id_correspondant": element.boond_id,
                     "nom_table_correspondante": 'candidates',
                     "defaut": defaut},
            defaut=defaut,
            date_releve=datetime.now().date().strftime('%Y-%m-%d'),
            nom_table_correspondante='candidates',
            est_corrige=False,
            id_correspondant=element.boond_id
        )
        dprint("[{}] {}".format(element.boond_id, defaut), priority_level=4)
    else:
        safe_update_table_row(
            table=Controle_qualite,
            filters={"id_correspondant": element.boond_id,
                     "nom_table_correspondante": 'candidates',
                     "defaut": defaut},
            est_corrige=True,
        )
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
        "Site Societe",
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
    agency = ''
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
        details_candidat = request("/candidates/{}/information".format(informations['boond_id']))

        for item in safe_dict_get(details_candidat, ['included']) or []:
            if safe_dict_get(item, ["type"]) == "agency":
                agency = safe_dict_get(item, ["attributes", "name"])
                break

        informations["boond_ressource_id"] = safe_dict_get(details_candidat,
                                                           ["data", "relationships", "resource", "data", "id"])
    else:
        informations["boond_ressource_id"] = safe_dict_get(basic_data, ["relationships", "resource", "data", "id"])

    # Pour les infos prise_de_contact & recontacte il faut aller voir les actions
    actions = request("/candidates/{}/actions".format(informations['boond_id']))
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

    informations['agence'] = agency

    return informations


def check_new_and_update_candidates(start_day, end_day):
    """
    Met à jour et ajoute tous les nouveaux candidats à la table Candidats:
    :param day:
    :return:
    """
    dprint("Update candidates table", priority_level=3, preprint="\n")
    list_of_candidates_to_update = get_list_of_element(
        "/candidates",
        period="updated",
        startDate=start_day,
        endDate=end_day
    )

    for candidate_to_update_basic_informations in list_of_candidates_to_update['data']:
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
            signature=candidate_to_update_all_informations["signature"],
            agence=candidate_to_update_all_informations["agence"]
        )

        dprint(
            "Update candidat: {} {}".format(
                candidate_to_update_all_informations['nom'],
                candidate_to_update_all_informations['prenom']
            ),
            priority_level=4)


def controle_qualite_kpi1():
    """
    Controle qualite KPI1
    :return:
    """

    candidates = get_last_week_updated_candidates()
    resources_dict = get_all_resource_as_dict()
    actions_dict = get_candidates_actions_as_dict()

    for element in candidates:
        # Point de controle 1: Extraction des personnes qui ont ete modifiees ou creees
        # dans la semaine sans action saisie
        dprint("KPI1: controle qualite 1", priority_level=3, preprint="\n")
        controle_1(element, actions_dict)

        # Point de controle 2: Extraire toutes les personnes qui ont ete modifiees
        # dans la semaine avec un sourceur qui n’est plus dans le groupe Lamarck
        dprint("KPI1: controle qualite 2", priority_level=3, preprint="\n")
        controle_2(element, resources_dict)
