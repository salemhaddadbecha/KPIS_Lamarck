# Modules / Dependances
from tables import Controle_qualite
# Tools
from tools.requests_tools import get_list_of_element
from tools.safe_actions import safe_dict_get, dprint, get_period_dates


def controle_1(start_date, end_date):

    def create_failure(resource):
        pass

    for resource in get_list_of_element("/resources"):
        create_failure(resource)


def controle_qualite_kpi6(start_date, end_date):
    dates = [start_date, end_date]

    # Point de controle 1:
    """
    S’assurer que les soutenances soient bien renseignees
    """
    # Comment trouver la soutenance ? idee: on regarder tous les
    # positionnemnts puis toutes les actions de la resources et on compare -> jamais de soutenance dans actions pq ?
    dprint(f"#- KPI6: controle qualite 1")
    controle_1(dates[0], dates[1])

