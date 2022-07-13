# TODO: Execution quotidienne

# Librairies
from datetime import datetime

# Modules / Dépendances
from tables import Controle_qualite
from modules.requests_tools import get_list_of_element
from modules.safe_actions import safe_dict_get, safe_date_convert, safe_update_table_row, get_current_date, get_period_dates, dprint


def controle_1(start_date, end_date):
    def create_failure(resource):
        pass

    for resource in get_list_of_element("/resources"):
        create_failure(resource)

def controle_qualite_kpi16():
    # Point de contrôle 1:
    """
    -   Tous les projets qui n’ont pas d’action d’un des 3 types
    -   Tous les projets qui ont plusieurs actions d’un des 3 types
    """
    # TODO: controle qualite sur les Roll mais aucun exemple ...


    #controle_1()

