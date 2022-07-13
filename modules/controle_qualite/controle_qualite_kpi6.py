# Modules / Dépendances
from tables import Controle_qualite
from modules.requests_tools import get_list_of_element
from modules.safe_actions import safe_dict_get, dprint, get_period_dates, get_current_date


def controle_1(start_date, end_date):

    def create_failure(resource):
        pass

    for resource in get_list_of_element("/resources"):
        create_failure(resource)


def controle_2():
    pass


def controle_qualite_kpi6():
    dates = get_period_dates()

    # Point de contrôle 1:
    """
    S’assurer que les soutenances soient bien renseignées
    """
    # TODO: Comment trouver la soutenance ? idée: on regarder tous les
    #  positionnemnts puis toutes les actions de la resources et on compare -> jamais de soutenance dans actions pq ?
    dprint(f"#- KPI6: contrôle qualité 1")
    controle_1(dates[0], dates[1])

