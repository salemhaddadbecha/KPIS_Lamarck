# Modules / Dependances
import datetime

from tables import Controle_qualite
from tools.database_functions import get_all_resources_consultant_interne_in_mission_or_intern
# Tools
from tools.safe_actions import safe_update_table_row, dprint


def controle_1():
    """
    Verifie que l etat des ressources est bien a jour
    :return:
    """

    def _create_failure(resource):
        """
        Cree ou non (en fonction des consignes de controle) un releve de defaut dans la table Controle qualite
        :param resource:
        :return:
        """

        def _get_last_prestation(resource):
            """
            Permet de recuperer la derniere prestation d une ressource
            :param resource:
            :return: informations sur la derniere prestation d une ressource
            """
            return {
                "etat": resource.etat,
                "en_cours": resource.debut_derniere_prestation is not None and
                            resource.fin_derniere_prestation is not None and
                            resource.debut_derniere_prestation <=
                            datetime.datetime.now().date() <=
                            resource.fin_derniere_prestation,
                "debut": resource.debut_derniere_prestation,
                "fin": resource.fin_derniere_prestation
            }

        last_prestation = _get_last_prestation(resource)

        defaut = "Défaut KPI12: La dernière prestation de la ressource {} {} n'a pas de date de debut.".format(
            resource.nom,
            resource.prenom
        )

        if not last_prestation["debut"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": resource.boond_id,
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=datetime.datetime.now().date().strftime('%Y-%m-%d'),
                nom_table_correspondante="ressources",
                est_corrige=False,
                id_correspondant=resource.boond_id
            )
            dprint("[{}] {}".format(resource.boond_id, defaut), priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": resource.boond_id,
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                est_corrige=True,
            )

        defaut = "Défaut KPI12: La dernière prestation de la ressource {} {} n'a pas de date de fin".format(
            resource.nom,
            resource.prenom
        )

        if not last_prestation["fin"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": resource.boond_id,
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=datetime.datetime.now().date().strftime('%Y-%m-%d'),
                nom_table_correspondante="ressources",
                est_corrige=False,
                id_correspondant=resource.boond_id
            )
            dprint("[{}] {}".format(resource.boond_id, defaut), priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": resource.boond_id,
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                est_corrige=True,
            )
        defaut = "Défaut KPI12: La ressource {} {} est à l'état 'en mission' " \
                 "alors qu'aucune prestation n'est en cours.".format(
            resource.nom,
            resource.prenom
        )
        if last_prestation["etat"] == "en mission" and not last_prestation["en_cours"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": resource.boond_id,
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=datetime.datetime.now().date().strftime('%Y-%m-%d'),
                nom_table_correspondante="ressources",
                est_corrige=False,
                id_correspondant=resource.boond_id
            )
            dprint("[{}] {}".format(resource.boond_id, defaut), priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": resource.boond_id,
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                est_corrige=True,
            )

        defaut = "Défaut KPI12: La ressource {} {} est à l'état 'en interne' alors" \
                 " qu'une prestation est en cours.".format(
            resource.nom,
            resource.prenom
        )
        if last_prestation["etat"] == "en interne" and last_prestation["en_cours"] == True:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": resource.boond_id,
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=datetime.datetime.now().date().strftime('%Y-%m-%d'),
                nom_table_correspondante="ressources",
                est_corrige=False,
                id_correspondant=resource.boond_id
            )
            dprint("[{}] {}".format(resource.boond_id, defaut), priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": resource.boond_id,
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                est_corrige=True,
            )

    for resource in get_all_resources_consultant_interne_in_mission_or_intern():
        _create_failure(resource)


def controle_qualite_kpi12():
    """
    Controle qualite KPI12
    :return:
    """
    # Point de controle 1:
    """
    Mise à jour de l’etat de la Ressource sur Boond
    """
    dprint("KPI12: controle qualite 1", priority_level=3, preprint="\n")
    controle_1()
