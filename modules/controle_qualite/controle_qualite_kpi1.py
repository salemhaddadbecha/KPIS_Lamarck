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
