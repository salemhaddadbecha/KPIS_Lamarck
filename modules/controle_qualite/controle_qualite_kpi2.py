# Librairie
import datetime
from datetime import timedelta

# Modules / Dependances
from tables import Controle_qualite
from tools.database_functions import get_all_candidates
# Tools
from tools.requests_tools import request
from tools.safe_actions import dprint, safe_dict_get, safe_update_table_row


def controle_1(candidat):
    """
    -	Rapport hebdo sur les consultants en statut Recrute(e) :
        o	Sans provenance
        o	Ou sans commentaire
    :return:
    """

    def _create_failure(candidat):
        """
        Cree ou non (en fonction des consignes de controle) un releve de defaut dans la table Controle qualite
        :param candidat:
        :return:
        """

        def _get_candidat_provenance(candidat):
            """
            Permet de recuperer la provenance et le detail de la provenance
            du candidat entre en parametre
            :param candidat:
            :return:
            """
            result = {'provenance': True, 'details_provenance': True}
            if str(candidat.provenance_cv) == 'non renseigne' or not candidat.provenance_cv:
                result['provenance'] = False

            if not candidat.commentaire_provenance_cv:
                result['details_provenance'] = False

            return result

        check = _get_candidat_provenance(candidat)

        defaut = "Défaut KPI2: Le candidat {} {} est recruté mais aucune provenance du CV n'est renseignée.".format(
            candidat.nom,
            candidat.prenom
        )
        if not check["provenance"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": candidat.boond_id,
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=datetime.datetime.now().date().strftime('%Y-%m-%d'),
                nom_table_correspondante="candidates",
                est_corrige=False,
                id_correspondant=candidat.boond_id
            )
            dprint("[{}] {}".format(candidat.boond_id, defaut), priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": candidat.boond_id,
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                est_corrige=True,
            )

        defaut = "Défaut KPI2: Le candidat {} {} est recruté mais aucun détail (champ commentaire) sur sa " \
                 "provenance n'est renseignée.".format(
            candidat.nom,
            candidat.prenom
        )
        if not check["details_provenance"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": candidat.boond_id,
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=datetime.datetime.now().date().strftime('%Y-%m-%d'),
                nom_table_correspondante="candidates",
                est_corrige=False,
                id_correspondant=candidat.boond_id
            )
            dprint("[{}] {}".format(candidat.boond_id, defaut), priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": candidat.boond_id,
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                est_corrige=True,
            )

    # candidateStates=3 -> que en statut recrute
    _create_failure(candidat)


def controle_2(candidat):
    """
    Rapport hebdo sur les consultants qui sont dans la partie Ressources
    mais qui n’ont pas le statut recrute ou base d’import (ou cleanage du stock)
    :return:
    """

    def create_failure(candidat):
        """
        Cree ou non (en fonction des consignes de controle) un releve de defaut dans la table Controle qualite
        :param candidat:
        :return:
        """

        def get_associated_ressource(candidat):
            information = request("/candidates/{}".format(safe_dict_get(candidat, ['id'])))
            return safe_dict_get(information, ["relationships", "resource", "data"])

        ressource = get_associated_ressource(candidat)

        defaut = "Défaut KPI2: Le candidat {} {} est recruté (fiche ressource créée) mais son statut n'est pas à jour.".format(
            safe_dict_get(candidat, ["attributes", 'lastName']),
            safe_dict_get(candidat, ["attributes", 'firstName'])
        )
        if ressource is not None:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(candidat, ["id"]),
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=datetime.datetime.now().date().strftime('%Y-%m-%d'),
                nom_table_correspondante="candidates",
                est_corrige=False,
                id_correspondant=safe_dict_get(candidat, ["id"])
            )
            dprint("[{}] {}".format(
                safe_dict_get(candidat, ['id']),defaut
            ), priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(candidat, ["id"]),
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                est_corrige=True,
            )

    # On reprend tous les candidats sur les 4 derniers mois: duree moyenne de recrutement
    create_failure(candidat)


def controle_3(candidat):
    """
    Rapport hebdo sur les candidats ayant
    comme agence « Lamarck Group » en fonction du type de poste
    :param agencies:
    :return:
    """

    def create_failure(candidat):
        """
        Cree ou non (en fonction des consignes de controle) un releve de defaut dans la table Controle qualite
        :param candidat:
        :param agencies:
        :return:
        """

        def get_candidat_agency(candidat):
            """
            Permet de recuperer l'agence rattachee à un candidat
            :param candidat:
            :return:
            """

            return candidat.agence

        candidat_agency = get_candidat_agency(candidat)

        defaut = "Défaut KPI2: Le candidat {} {} est lié à 'Lamarck Group'.".format(
            candidat.nom,
            candidat.prenom
        )
        if str(candidat_agency) == "Lamarck Group":
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": candidat.boond_id,
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=datetime.datetime.now().date().strftime('%Y-%m-%d'),
                nom_table_correspondante="candidates",
                est_corrige=False,
                id_correspondant=candidat.boond_id
            )
            dprint("[{}] {}".format(candidat.boond_id, defaut), priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": candidat.boond_id,
                         "nom_table_correspondante": "candidates",
                         "defaut": defaut},
                est_corrige=True,
            )

    create_failure(candidat)


def controle_qualite_kpi2():
    """
    Controle qualite KPI2
    :return:
    """
    candidates = get_all_candidates()
    # Point de controle 1:
    """
    -	Rapport hebdo sur les consultants en statut Recrute(e) :
        o	Sans provenance
        o	Ou sans commentaire
    """
    for candidate in candidates:
        if not candidate.recrute:
            continue

        dprint("KPI2: controle qualite 1", priority_level=3, preprint="\n")
        controle_1(candidate)

        # Point de controle 2:
        """
        Rapport hebdo sur les consultants qui sont dans la partie Ressources 
        mais qui n’ont pas le statut recrute ou base d’import (ou cleanage du stock)
        """
        # dprint("KPI2: controle qualite 2", priority_level=3, preprint="\n")
        # controle_2(candidates)
        # ToDo:find a way to make this kpi possible

        # Point de controle 3
        """
        Rapport hebdo sur les candidats ayant 
        comme agence « Lamarck Group » en fonction du type de poste
        """
        dprint("KPI2: controle qualite 3", priority_level=3, preprint="\n")
        controle_3(candidate)
