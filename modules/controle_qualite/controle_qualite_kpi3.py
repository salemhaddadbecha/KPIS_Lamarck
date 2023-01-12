# Modules / Dependances
import datetime

from tables import Controle_qualite
from tools.database_functions import get_all_resources
from tools.safe_actions import safe_update_table_row, dprint


def controle_1(resource):
    """
    Existence pour tous les consultants d’au
    moins une ligne dans le bloc Ressources > Administratif > Contrat RH
    :return:
    """

    def _create_failure(resource):
        """
        Cree ou non (en fonction des consignes de controle) un releve de defaut dans la table Controle qualite
        :param resource:
        :return:
        """

        def _get_hr_contract(resource):
            """
            Permet de recuperer tous les contrats RH d'une ressource
            :param resource:
            :return:
            """
            return True if resource.date_de_recrutement else False

        defaut = "Défaut KPI3: Aucun contrat RH n'est renseigné sur la ressource {} {}.".format(
            resource.nom,
            resource.prenom,
        )
        if not _get_hr_contract(resource):
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

    _create_failure(resource)


def controle_2(resource):
    """
    Mettre à jour l’ensemble des titres de profils Ressources pour standardiser
    les titres avec le profil du consultant
    :return:
    """

    def _create_failure(resource):
        """
        Cree ou non (en fonction des consignes de controle) un releve de defaut dans la table Controle qualite
        :param resource:
        :return:
        """
        liste_titre_autorise = [
            'Consultant',
            'Consultante',
            'Consultant Confirmé',
            'Consultante Confirmée',
            'Consultant Senior',
            'Consultante Senior',
            'Consultant Manager',
            'Consultante Manager',
            'Consultant Directeur',
            'Consultante Directeur',
            'Alternant',
            'Alternante',
            'Business Partner',
            'Business Manager',
            'Chargée de communication',
            'Chargée des Ressources Humaines',
            'Chercheur',
            'Chercheuse',
            'Freelance',
            'Gérant',
            'Gérante',
            'Stagiaire',
            'Lamarck Institute',
            'Responsable des ressources humaines',
        ]


        defaut = "Défaut KPI3: Le titre de la ressource {} {} est non conforme : '{}'.".format(
            resource.nom,
            resource.prenom,
            resource.profil)
        if resource.profil not in liste_titre_autorise:
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

    _create_failure(resource)


def controle_qualite_kpi3():
    """
    Controle qualite KPI3
    :return:
    """
    resources = get_all_resources()
    for resource in resources:
        # Point de controle 1:
        """
        Existence pour tous les consultants d’au
        moins une ligne dans le bloc Ressources > Administratif > Contrat RH
        """
        dprint("KPI3: controle qualite 1", priority_level=3, preprint="\n")
        controle_1(resource)

        # Point de controle 2:
        """
        Mettre à jour l’ensemble des titres de profils Ressources pour standardiser 
        les titres avec le profil du consultant
        """
        dprint("KPI3: controle qualite 2", priority_level=3, preprint="\n")
        controle_2(resource)
