# Modules / Dependances
import datetime

from tables import Controle_qualite
from tools.database_functions import get_all_contacts_updated_last_ten_days
# Tools
from tools.safe_actions import safe_update_table_row, dprint


def controle_1(contact):
    """
    Recupere les clients sans provenance
    :return:
    """

    def _create_failure(contact):
        """
        Cree ou non (en fonction des consignes de controle) un releve de defaut dans la table Controle qualite
        :param contact:
        :return:
        """

        def _get_contact_provenance(contact):
            """
            Permet de savoir si la provenance et le detail de la provenance d'un contact sont presents
            :param contact:
            :return: provenance et le detail de la provenance (Boolean)
            """
            check = {
                "provenance": True,
                "details_provenance": True
            }

            if contact.provenance == 'non renseigne' or not contact.provenance:
                check['provenance'] = False

            if contact.detail_provenance == 'non renseigne' or not contact.detail_provenance:
                check['details_provenance'] = False

            return check

        check = _get_contact_provenance(contact)

        defaut = "Défaut KPI8: Le contact {} {} est créé mais aucune provenance n'est renseignée.".format(
            contact.nom,
            contact.prenom
        )
        if not check["provenance"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": contact.boond_id,
                         "nom_table_correspondante": "contacts",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=datetime.datetime.now().date().strftime('%Y-%m-%d'),
                nom_table_correspondante="contacts",
                est_corrige=False,
                id_correspondant=contact.boond_id
            )
            dprint("[{}] {}".format(contact.boond_id, defaut), priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": contact.boond_id,
                         "nom_table_correspondante": "contacts",
                         "defaut": defaut},
                est_corrige=True,
            )

        defaut = "Défaut KPI8: Le contact {} {} est créé mais aucun détail sur sa provenance n'est renseignée.".format(
            contact.nom,
            contact.prenom
        )
        if not check["details_provenance"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": contact.boond_id,
                         "nom_table_correspondante": "contacts",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=datetime.datetime.now().date().strftime('%Y-%m-%d'),
                nom_table_correspondante="contacts",
                est_corrige=False,
                id_correspondant=contact.boond_id
            )
            dprint("[{}] {}".format(contact.boond_id, defaut), priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": contact.boond_id,
                         "nom_table_correspondante": "contacts",
                         "defaut": defaut},
                est_corrige=True,
            )

    _create_failure(contact)


def controle_qualite_kpi8():
    """
    Controle qualite KPI8
    :return:
    """
    contacts = get_all_contacts_updated_last_ten_days()

    for contact in contacts:
        # Point de controle 1:
        """
        Reporting hebdo des clients sans provenance
        """
        dprint("KPI8: controle qualite 1", priority_level=3, preprint="\n")
        controle_1(contact)
