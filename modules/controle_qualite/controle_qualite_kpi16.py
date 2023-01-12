# Modules / Dependances
from datetime import datetime

from tables import Controle_qualite
from tools.database_functions import get_all_projects, get_projects_actions_as_dict
# Tools
from tools.safe_actions import safe_update_table_row, dprint


def controle_1(projects, projects_actions):
    """
    -   Tous les projets qui n’ont pas d’action d’un des 3 types
    -   Tous les projets qui ont plusieurs actions d’un des 3 types
    :param day:
    :return:
    """

    def _create_failure(projet, project_actions):
        """
        Cree ou non (en fonction des consignes de controle) un releve de defaut dans la table Controle qualite
        :param projet:
        :param day:
        :return:
        """

        def _get_projet_actions(project_actions):
            """
            Permet de recuperer les actions liees a un projet, et de verifier
            que les actions: roll probable | garanti | indetermine sont present ou non
            :param projet:
            :return: liste des presnces des actions
            """
            actions_lite = {
                "roll probable": False,
                "roll garanti": False,
                "roll indetermine": False
            }

            if '35' in project_actions or 35 in project_actions:
                actions_lite["roll probable"] = True

            if '36' in project_actions or 36 in project_actions:
                actions_lite["roll garanti"] = True

            if '37' in project_actions or 37 in project_actions:
                actions_lite["roll indetermine"] = True

            return actions_lite

        actions = _get_projet_actions(project_actions)

        roll_count = sum(
            [1 if value else 0 for value in actions.values()]
        )

        defaut = "Défaut KPI16: le projet {} comporte plusieurs action de type 'Roll'.".format(
            projet.boond_id
        )
        if roll_count >= 2:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": projet.boond_id,
                         "nom_table_correspondante": "projets",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=datetime.now().date().strftime('%Y-%m-%d'),
                nom_table_correspondante="projets",
                est_corrige=False,
                id_correspondant=projet.boond_id
            )
            dprint("[{}] {}".format(projet.boond_id, defaut), priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": projet.boond_id,
                         "nom_table_correspondante": "projets",
                         "defaut": defaut},
                est_corrige=True,
            )

        defaut = "Défaut KPI16: le projet {} ne comporte aucune action de type 'Roll'.".format(
            projet.boond_id
        )
        if roll_count == 0:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": projet.boond_id,
                         "nom_table_correspondante": "projets",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=datetime.now().date().strftime('%Y-%m-%d'),
                nom_table_correspondante="projets",
                est_corrige=False,
                id_correspondant=projet.boond_id
            )
            dprint("#[{}] {}".format(projet.boond_id, defaut), priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": projet.boond_id,
                         "nom_table_correspondante": "projets",
                         "defaut": defaut},
                est_corrige=True,
            )

    for projet in projects:
        _create_failure(projet, projects_actions.get(projet.boond_id, []))


def controle_qualite_kpi16():
    """
    Controle qualite KPI16
    :param day:
    :return:
    """
    projects = get_all_projects()
    if not projects:
        return
    projects_actions = get_projects_actions_as_dict()
    # Point de controle 1:
    """
    -   Tous les projets qui n’ont pas d’action d’un des 3 types
    -   Tous les projets qui ont plusieurs actions d’un des 3 types
    """
    dprint("KPI16: controle qualite 1", priority_level=3, preprint="\n")
    controle_1(projects, projects_actions)
