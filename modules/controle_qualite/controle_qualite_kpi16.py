# Modules / Dependances
from tables import Controle_qualite
# Tools
from tools.requests_tools import get_list_of_element
from tools.safe_actions import safe_dict_get, safe_update_table_row, get_current_date, \
    dprint, is_in_the_list


def controle_1(start_date, end_date):
    def _create_failure(projet):
        """
        Crée ou non (en fonction des consignes de controle) un relevé de défaut dans la table Controle qualite
        :param projet:
        :return:
        """

        def _get_projet_actions(projet):
            """
            Permet de récupérer les actions liees a un projet, et de verifier
            que les actions: roll probable | garanti | indetermine sont present ou non
            :param projet:
            :return: liste des presnces des actions
            """
            actions = get_list_of_element(f"/projects/{projet['id']}/actions")
            actions_lite = {
                "roll probable": False,
                "roll garanti": False,
                "roll indetermine": False
            }

            for action in actions:

                # Roll probable
                if is_in_the_list([35, "35"], safe_dict_get(action, ["attributes", "typeOf"])):
                    actions_lite["roll probable"] = True

                # Roll garanti
                elif is_in_the_list([36, "36"], safe_dict_get(action, ["attributes", "typeOf"])):
                    actions_lite["roll garanti"] = True

                # Roll indetermine
                elif is_in_the_list([37, "37"], safe_dict_get(action, ["attributes", "typeOf"])):
                    actions_lite["roll indetermine"] = True

            return actions_lite

        actions = _get_projet_actions(projet)

        roll_count = sum(
            [1 if value else 0 for value in actions.values()]
        )

        defaut = f"Defaut KPI16: le projet {safe_dict_get(projet, ['attributes', 'reference'])} comporte plusieurs action de type 'Roll'"
        if roll_count >= 2:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(projet, ["id"]),
                         "nom_table_correspondante": "projets",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=get_current_date(),
                nom_table_correspondante="projets",
                est_corrige=False,
                id_correspondant=safe_dict_get(projet, ["id"])
            )
            dprint(f"[{safe_dict_get(projet, ['id'])}] {defaut}", priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(projet, ["id"]),
                         "nom_table_correspondante": "projets",
                         "defaut": defaut},
                est_corrige=True,
            )

        defaut = f"Defaut KPI16: le projet {safe_dict_get(projet, ['attributes', 'reference'])} ne comporte aucune action de type 'Roll'"
        if roll_count == 0:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(projet, ["id"]),
                         "nom_table_correspondante": "projets",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=get_current_date(),
                nom_table_correspondante="projets",
                est_corrige=False,
                id_correspondant=safe_dict_get(projet, ["id"])
            )
            dprint(f"#[{safe_dict_get(projet, ['id'])}] {defaut}", priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(projet, ["id"]),
                         "nom_table_correspondante": "projets",
                         "defaut": defaut},
                est_corrige=True,
            )

    for projet in get_list_of_element("/projects", startDate=start_date, endDate=end_date):
        _create_failure(projet)


def controle_qualite_kpi16(start_date, end_date):
    """
    Controle qualite KPI16
    :param start_date:
    :param end_date:
    :return:
    """
    dates = [start_date, end_date]

    # Point de controle 1:
    """
    -   Tous les projets qui n’ont pas d’action d’un des 3 types
    -   Tous les projets qui ont plusieurs actions d’un des 3 types
    """
    dprint(f"KPI16: controle qualite 1", priority_level=3, preprint="\n")
    controle_1(dates[0], dates[1])
