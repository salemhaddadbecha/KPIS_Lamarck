# Modules / Dépendances
from tables import Controle_qualite
from modules.requests_tools import get_list_of_element
from modules.safe_actions import safe_dict_get, is_in_the_list, safe_update_table_row, get_period_dates, get_current_date, dprint

def controle_1(start_date, end_date):
    def create_failure(candidat):
        def get_candidat_provenance(candidat):
            check = {
                "provenance": False,
                "details_provenance": False
            }

            if safe_dict_get(candidat, ["attributes", "source", "typeOf"]) is not None and \
                    not is_in_the_list([-1, "-1"], safe_dict_get(candidat, ["attributes", "source", "typeOf"])):
                check["provenance"] = True

            if safe_dict_get(candidat, ["attributes", "source", "detail"]) is not None and \
                    safe_dict_get(candidat, ["attributes", "source", "detail"]) != "":
                check["details_provenance"] = True

            return check

        check = get_candidat_provenance(candidat)

        if not check["provenance"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(candidat, ["id"]),
                         "nom_table_correspondante": "candidates",
                         "defaut": "Défaut KPI2: Candidat recruté mais aucune provenance renseignée"},
                defaut=f"Défaut KPI2: Candidat recruté mais aucune provenance renseignée",
                date_releve=get_current_date(),
                nom_table_correspondante="candidates",
                id_correspondant=safe_dict_get(candidat, ["id"])
            )
            dprint(f"#-- [{safe_dict_get(candidat, ['id'])}] Défaut KPI2: Candidat recruté mais aucune provenance renseignée")

        if not check["details_provenance"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(candidat, ["id"]),
                         "nom_table_correspondante": "candidates",
                         "defaut": "Défaut KPI2: Candidat recruté mais aucun détail sur sa provenance est renseigné"},
                defaut=f"Défaut KPI2: Candidat recruté mais aucun détail sur sa provenance est renseigné",
                date_releve=get_current_date(),
                nom_table_correspondante="candidates",
                id_correspondant=safe_dict_get(candidat, ["id"])
            )
            dprint(f"#-- [{safe_dict_get(candidat, ['id'])}] Défaut KPI2: Candidat recruté mais aucun détail sur sa provenance est renseigné")

    for candidat in get_list_of_element("/candidates", candidateStates=3, startDate=start_date, endDate=end_date, period="updated"):
        create_failure(candidat)

def controle_2():
    for candidate in get_list_of_element("/candidates"):
        print(candidate)
        print()


def controle_qualite_kpi2():
    dates = get_period_dates()

    # Point de contrôle 1:
    """
    -	Rapport hebdo sur les consultants en statut Recruté(e) :
        o	Sans provenance
        o	Ou sans commentaire
    """
    dprint(f"#- KPI2: contrôle qualité 1")
    controle_1(dates[0], dates[1])

    # Point de contrôle 2:
    """
    Rapport hebdo sur les consultants qui sont dans la partie Ressources 
    mais qui n’ont pas le statut recruté ou base d’import (ou cleanage du stock)
    """
    #controle_2()
    # TODO: solution à trouver car hypo: lister les candidats pour chaque
    #  candidat rechercher /information et trouver si resource associé,
    #  si oui regarder le statut et si il est pas à recrtué alors erreur

    """
    Rapport hebdo sur les candidats ayant 
    comme agence « Lamarck Group » en fonction du type de poste
    """
    # TODO: ça veut dire quoi ? qui estce qu'il faut faire ?
