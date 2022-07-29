# Librairie
from datetime import timedelta

# Modules / Dependances
from tables import Controle_qualite
# Tools
from tools.requests_tools import get_list_of_element, get_list_of_agencies, request
from tools.safe_actions import dprint, safe_dict_get, is_in_the_list, safe_update_table_row, safe_date_convert


def controle_1(day):
    """
    -	Rapport hebdo sur les consultants en statut Recrute(e) :
        o	Sans provenance
        o	Ou sans commentaire
    :param day:
    :return:
    """

    def _create_failure(candidat):
        """
        Crée ou non (en fonction des consignes de controle) un relevé de défaut dans la table Controle qualite
        :param candidat:
        :return:
        """

        def _get_candidat_provenance(candidat):
            """
            Permet de récupérer la provenance et le détail de la provenance
            du candidat entré en paramètre
            :param candidat:
            :return:
            """
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

        check = _get_candidat_provenance(candidat)

        defaut = "Defaut KPI2: Candidat recrute mais aucune provenance renseignee"
        if not check["provenance"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(candidat, ["id"]),
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=day,
                nom_table_correspondante="candidates",
                est_corrige=False,
                id_correspondant=safe_dict_get(candidat, ["id"])
            )
            dprint(f"[{safe_dict_get(candidat, ['id'])}] {defaut}", priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(candidat, ["id"]),
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                est_corrige=True,
            )

        defaut = "Defaut KPI2: Candidat recrute mais aucun detail sur sa provenance est renseigne"
        if not check["details_provenance"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(candidat, ["id"]),
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=day,
                nom_table_correspondante="candidates",
                est_corrige=False,
                id_correspondant=safe_dict_get(candidat, ["id"])
            )
            dprint(f"[{safe_dict_get(candidat, ['id'])}] {defaut}", priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(candidat, ["id"]),
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                est_corrige=True,
            )

    # candidateStates=3 -> que en statut recruté
    for candidat in get_list_of_element("/candidates", candidateStates=3, startDate=day, endDate=day,
                                        period="updated"):
        _create_failure(candidat)


def controle_2(day):
    """
    Rapport hebdo sur les consultants qui sont dans la partie Ressources
    mais qui n’ont pas le statut recrute ou base d’import (ou cleanage du stock)
    :param day:
    :return:
    """

    def create_failure(candidat):
        """
        Crée ou non (en fonction des consignes de controle) un relevé de défaut dans la table Controle qualite
        :param candidat:
        :return:
        """

        def get_associated_ressource(candidat):
            information = request(f"/candidates/{safe_dict_get(candidat, ['id'])}")
            return safe_dict_get(information, ["relationships", "resource", "data"])

        ressource = get_associated_ressource(candidat)

        defaut = "Defaut KPI2: Candidat recruté (fiche ressource créée) mais son statut n'est pas à jour"
        if ressource is not None:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(candidat, ["id"]),
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=day,
                nom_table_correspondante="candidates",
                est_corrige=False,
                id_correspondant=safe_dict_get(candidat, ["id"])
            )
            dprint(f"[{safe_dict_get(candidat, ['id'])}] {defaut}", priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(candidat, ["id"]),
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                est_corrige=True,
            )

    # On reprend tous les candidats sur les 4 derniers mois: durée moyenne de recrutement
    for candidat in get_list_of_element("/candidates", startDate=safe_date_convert(day) - timedelta(weeks=4 * 4),
                                        endDate=day, period="updated"):
        create_failure(candidat)


def controle_3(day, agencies):
    """
    Rapport hebdo sur les candidats ayant
    comme agence « Lamarck Group » en fonction du type de poste
    :param day:
    :param agencies:
    :return:
    """

    def create_failure(candidat, agencies):
        """
        Crée ou non (en fonction des consignes de controle) un relevé de défaut dans la table Controle qualite
        :param candidat:
        :param agencies:
        :return:
        """

        def get_candidat_agency(candidat, agencies):
            """
            Permet de récupérer l'agence rattachée à un candidat
            :param candidat:
            :param agencies:
            :return:
            """
            candidat_agency = None
            candidat_informations = None

            candidat_id = safe_dict_get(candidat, ["id"])

            if candidat_id is not None:
                candidat_informations = request(f"/candidates/{candidat_id}/information")

            if safe_dict_get(candidat_informations, ["attributes", "state"]) is not None:
                candidat_agency = safe_dict_get(agencies,
                                                [int(safe_dict_get(candidat_informations, ["attributes", "state"]))])

            return candidat_agency

        candidat_agency = get_candidat_agency(candidat, agencies)

        defaut = "Defaut KPI2: Candidat lie à 'Lamarck Group'"
        if candidat_agency == "Lamarck Group":
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(candidat, ["id"]),
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=day,
                nom_table_correspondante="candidates",
                est_corrige=False,
                id_correspondant=safe_dict_get(candidat, ["id"])
            )
            dprint(f"[{safe_dict_get(candidat, ['id'])}] {defaut}", priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(candidat, ["id"]),
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                est_corrige=True,
            )

    for candidat in get_list_of_element("/candidates", startDate=day, endDate=day, period="updated"):
        create_failure(candidat, agencies)


def controle_qualite_kpi2(day):
    """
    Controle qualite KPI2
    :param day:
    :return:
    """

    # Point de controle 1:
    """
    -	Rapport hebdo sur les consultants en statut Recrute(e) :
        o	Sans provenance
        o	Ou sans commentaire
    """
    dprint(f"KPI2: controle qualite 1", priority_level=3, preprint="\n")
    controle_1(day)

    # Point de controle 2:
    """
    Rapport hebdo sur les consultants qui sont dans la partie Ressources 
    mais qui n’ont pas le statut recrute ou base d’import (ou cleanage du stock)
    """
    dprint(f"KPI2: controle qualite 2", priority_level=3, preprint="\n")
    controle_2(day)

    # Point de controle 3
    """
    Rapport hebdo sur les candidats ayant 
    comme agence « Lamarck Group » en fonction du type de poste
    """
    dprint(f"KPI2: controle qualite 3", priority_level=3, preprint="\n")
    agencies = get_list_of_agencies()
    controle_3(day, agencies)
