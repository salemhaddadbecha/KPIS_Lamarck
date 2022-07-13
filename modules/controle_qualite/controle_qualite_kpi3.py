# Modules / Dépendances
from tables import Controle_qualite
from modules.requests_tools import request, get_list_of_element
from modules.safe_actions import safe_dict_get, safe_update_table_row, get_period_dates, dprint, get_current_date


def controle_1(start_date, end_date):
    def create_failure(resource):
        def get_hr_contract(resource):
            check = False
            administrative = request(f"/resources/{safe_dict_get(resource, ['id'])}/administrative")

            if safe_dict_get(administrative, ["data", "relationships", "contracts", "data"]) is not None and \
                len(safe_dict_get(administrative, ["data", "relationships", "contracts", "data"])) > 0:
                check = True

            return check

        if not get_hr_contract(resource):
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": "Défaut KPI3: aucun contract RH renseigné sur la resource"},
                defaut=f"Défaut KPI3: aucun contract RH renseigné sur la resource",
                date_releve=get_current_date(),
                nom_table_correspondante="ressources",
                id_correspondant=safe_dict_get(resource, ["id"])
            )
            dprint(f"#-- [{safe_dict_get(resource, ['id'])}] Défaut KPI3: aucun contract RH renseigné sur la resource")

    for resource in get_list_of_element("/resources", startDate=start_date, endDate=end_date, period="updated"):
        create_failure(resource)


def controle_2():
    pass


def controle_qualite_kpi3():
    dates = get_period_dates()

    # Point de contrôle 1:
    """
    Existence pour tous les consultants d’au
    moins une ligne dans le bloc Ressources > Administratif > Contrat RH
    """
    dprint(f"#- KPI3: contrôle qualité 1")
    controle_1(dates[0], dates[1])

    # Point de contrôle 2:
    """
    Mettre à jour l’ensemble des titres de profils Ressources pour standardiser 
    les titres avec le profil du consultant
    """
    #controle_2()
    # TODO: signification ?