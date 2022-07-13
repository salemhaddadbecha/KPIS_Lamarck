# Modules / Dépendances
from tables import Controle_qualite
from modules.requests_tools import request, get_list_of_element
from modules.safe_actions import safe_dict_get, safe_date_convert, safe_update_table_row, get_period_dates, dprint, get_current_date

def controle_1(key, element, dates):
    def are_there_any_actions_created(endpoint, element, dates):
        new_actions = False

        # Fonctionne pour les candidats et les resources
        actions = request(f"{endpoint}/{safe_dict_get(element, ['id'])}/actions")

        for action in safe_dict_get(actions, ["data"]):
            action_date_str = safe_dict_get(action, ["attributes", "creationDate"])
            if safe_date_convert(dates[0]) <= safe_date_convert(action_date_str) <= safe_date_convert(dates[1]):
                new_actions = True
                break

        return new_actions

    check = are_there_any_actions_created(f"/{key}", element, dates)

    if not check:
        safe_update_table_row(
            table=Controle_qualite,
            filters={"id_correspondant": safe_dict_get(element, ["id"]),
                     "nom_table_correspondante": key,
                     "defaut": f"Défaut KPI1: {key} créé mais aucune action a été saisie"},
            defaut=f"Défaut KPI1: {key} créé mais aucune action a été saisie",
            date_releve=get_current_date(),
            nom_table_correspondante=key,
            id_correspondant=safe_dict_get(element, ["id"])
        )
        dprint(f"#-- [{safe_dict_get(element, ['id'])}] Défaut KPI1: {key} créé mais aucune action a été saisie")

def controle_2(key, element):
    pass

def controle_qualite_kpi1():
    dates = get_period_dates()

    people = {
        "candidates": get_list_of_element("/candidates", period="updated", startDate=dates[0], endDate=dates[1]),
        "resources": get_list_of_element("/resources", period="updated", startDate=dates[0], endDate=dates[1])
    }

    for key, value in people.items():

        for element in value:

            # Point de contrôle 1: Extraction des personnes qui ont été modifiées ou créées
            # dans la semaine sans action saisie
            dprint(f"#- KPI1: contrôle qualité 1")
            controle_1(key, element, dates)

            # Point de contrôle 2: Extraire toutes les personnes qui ont été modifiées
            # dans la semaine avec un sourceur qui n’est plus dans le groupe Lamarck
            # TODO: comment trouver si le sourceur est dans le groupe lamarack ou non, c'est le sourceur qui modifie ?
            controle_2(key, element)


