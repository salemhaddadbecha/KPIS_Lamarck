# Librairie
from datetime import datetime

# Modules / Dependances
from tables import Controle_qualite
# Tools
from tools.requests_tools import request, get_list_of_element
from tools.safe_actions import safe_dict_get, safe_date_convert, safe_update_table_row, dprint


def controle_1(key, element, day):
    """
    Point de controle 1: Extraction des personnes qui ont ete modifiees ou creees
    dans la semaine sans action saisie
    :param key:
    :param element:
    :param day:
    :return:
    """

    def _are_there_any_actions_created(endpoint, element, day):
        """
        Permet de savoit si des nouvelles actions ont été créées sur l'élément
        :param element:
        :return: nouvelles actions (boolean)
        """
        new_actions = False

        # Fonctionne pour les candidats et les resources
        actions = request(f"{endpoint}/{safe_dict_get(element, ['id'])}/actions")

        for action in safe_dict_get(actions, ["data"]):
            action_date_str = safe_dict_get(action, ["attributes", "creationDate"])
            if datetime(1900, 1, 1) <= safe_date_convert(action_date_str) <= safe_date_convert(day):
                new_actions = True
                break

        return new_actions

    check = _are_there_any_actions_created(f"/{key}", element, day)

    defaut = f"Defaut KPI1: {key} cree mais aucune action a ete saisie"
    if not check:
        safe_update_table_row(
            table=Controle_qualite,
            filters={"id_correspondant": safe_dict_get(element, ["id"]),
                     "nom_table_correspondante": key,
                     "defaut": defaut},
            defaut=defaut,
            date_releve=day,
            nom_table_correspondante=key,
            est_corrige=False,
            id_correspondant=safe_dict_get(element, ["id"])
        )
        dprint(f"[{safe_dict_get(element, ['id'])}] {defaut}", priority_level=4)
    else:
        safe_update_table_row(
            table=Controle_qualite,
            filters={"id_correspondant": safe_dict_get(element, ["id"]),
                     "nom_table_correspondante": key,
                     "defaut": defaut},
            est_corrige=True,
        )


def controle_2(key, element, day):
    """
    Point de controle 2: Extraire toutes les personnes qui ont ete modifiees
    dans la semaine avec un sourceur qui n’est plus dans le groupe Lamarck
    :param key:
    :param element:
    :param day:
    :return:
    """

    def _is_manager_out(element):
        """
        Permet de récupérer l'état du manager de l'élément, et de savoit s'il est OUT
        :param element:
        :return: out (boolean)
        """
        out = None
        manager_informations = None

        manager_id = safe_dict_get(element, ["relationships", "mainManager", "data", "id"])
        if manager_id is not None:
            manager_informations = request(f"/resources/{manager_id}/information")

        liste_etats = ["out", "en mission", "en interne", "en arrêt", "signe"]

        if safe_dict_get(manager_informations, ["attributes", "state"]) is not None:
            main_manager_etat = safe_dict_get(liste_etats,
                                              [int(safe_dict_get(manager_informations, ["attributes", "state"]))])
            if main_manager_etat is not None:
                out = (main_manager_etat == "out")
        return out

    is_out = _is_manager_out(element)

    defaut = f"Defaut KPI1: {key} modifie mais sourceur 'out' (plus dans le groupe Lamarck)"
    if is_out:
        safe_update_table_row(
            table=Controle_qualite,
            filters={"id_correspondant": safe_dict_get(element, ["id"]),
                     "nom_table_correspondante": key,
                     "defaut": defaut},
            defaut=defaut,
            date_releve=day,
            nom_table_correspondante=key,
            est_corrige=False,
            id_correspondant=safe_dict_get(element, ["id"])
        )
        dprint(f"[{safe_dict_get(element, ['id'])}] {defaut}", priority_level=4)
    else:
        safe_update_table_row(
            table=Controle_qualite,
            filters={"id_correspondant": safe_dict_get(element, ["id"]),
                     "nom_table_correspondante": key,
                     "defaut": defaut},
            est_corrige=True,
        )


def controle_qualite_kpi1(day):
    """
    Controle qualite KPI1
    :param day:
    :return:
    """
    people = {
        "candidates": get_list_of_element("/candidates", period="updated", startDate=day, endDate=day),
        "resources": get_list_of_element("/resources", period="updated", startDate=day, endDate=day)
    }

    for key, value in people.items():

        for element in value:
            # Point de controle 1: Extraction des personnes qui ont ete modifiees ou creees
            # dans la semaine sans action saisie
            dprint(f"KPI1: controle qualite 1", priority_level=3, preprint="\n")
            controle_1(key, element, day)

            # Point de controle 2: Extraire toutes les personnes qui ont ete modifiees
            # dans la semaine avec un sourceur qui n’est plus dans le groupe Lamarck
            dprint(f"KPI1: controle qualite 2", priority_level=3, preprint="\n")
            controle_2(key, element)
