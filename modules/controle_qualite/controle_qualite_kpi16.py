# Modules / Dépendances
from tables import Controle_qualite
from modules.requests_tools import get_list_of_element
from modules.safe_actions import safe_dict_get, safe_date_convert, safe_update_table_row, get_current_date, \
    get_period_dates, dprint, is_in_the_list


def controle_1(start_date, end_date):
    def create_failure(projet):
        def get_projet_actions(projet):
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

        actions = get_projet_actions(projet)

        roll_count = sum(
            [1 if value else 0 for value in actions.values()]
        )

        if roll_count >= 2:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(projet, ["id"]),
                         "nom_table_correspondante": "projets",
                         "defaut": f"Défaut KPI16: le projet {safe_dict_get(projet, ['attributes', 'reference'])} comporte plusieurs action de type 'Roll'"},
                defaut=f"Défaut KPI16: le projet {safe_dict_get(projet, ['attributes', 'reference'])} comporte plusieurs action de type 'Roll'",
                date_releve=get_current_date(),
                nom_table_correspondante="projets",
                id_correspondant=safe_dict_get(projet, ["id"])
            )
            dprint(f"#-- [{safe_dict_get(projet, ['id'])}] Défaut KPI16: le projet {safe_dict_get(projet, ['attributes', 'reference'])} comporte plusieurs action de type 'Roll'")

        elif roll_count == 0:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(projet, ["id"]),
                         "nom_table_correspondante": "projets",
                         "defaut": f"Défaut KPI16: le projet {safe_dict_get(projet, ['attributes', 'reference'])} ne comporte aucune action de type 'Roll'"},
                defaut=f"Défaut KPI16: le projet {safe_dict_get(projet, ['attributes', 'reference'])} ne comporte aucune action de type 'Roll'",
                date_releve=get_current_date(),
                nom_table_correspondante="projets",
                id_correspondant=safe_dict_get(projet, ["id"])
            )
            dprint(f"#-- [{safe_dict_get(projet, ['id'])}] Défaut KPI16: le projet {safe_dict_get(projet, ['attributes', 'reference'])} ne comporte aucune action de type 'Roll'")


    for projet in get_list_of_element("/projects"):
        create_failure(projet)


def controle_qualite_kpi16():
    dates = get_period_dates()

    # Point de contrôle 1:
    """
    -   Tous les projets qui n’ont pas d’action d’un des 3 types
    -   Tous les projets qui ont plusieurs actions d’un des 3 types
    """
    controle_1(dates[0], dates[1])
