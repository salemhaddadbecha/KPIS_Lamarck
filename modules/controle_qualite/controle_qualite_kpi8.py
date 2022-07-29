# Modules / Dependances
from tables import Controle_qualite
# Tools
from tools.requests_tools import request, get_list_of_element
from tools.safe_actions import safe_dict_get, is_in_the_list, safe_update_table_row, dprint


def controle_1(day):
    """
    Recupere les clients sans provenance
    :param day:
    :return:
    """

    def _create_failure(contact, day):
        """
        Crée ou non (en fonction des consignes de controle) un relevé de défaut dans la table Controle qualite
        :param contact:
        :param day:
        :return:
        """

        def _get_contact_provenance(contact):
            """
            Permet de savoir si la provenance et le détail de la provenance d'un contact sont présents
            :param contact:
            :return: provenance et le détail de la provenance (Boolean)
            """
            informations = request(f"/contacts/{contact['id']}/information")
            check = {
                "provenance": False,
                "details_provenance": False
            }

            if safe_dict_get(informations, ["data", "attributes", "origin", "typeOf"]) is not None and \
                    not is_in_the_list([-1, "-1"],
                                       safe_dict_get(informations, ["data", "attributes", "origin", "typeOf"])):
                check["provenance"] = True

            if safe_dict_get(informations, ["data", "attributes", "origin", "detail"]) is not None and \
                    safe_dict_get(informations, ["data", "attributes", "origin", "detail"]) != "":
                check["details_provenance"] = True

            return check

        check = _get_contact_provenance(contact)

        defaut = "Defaut KPI8: Contact cree mais aucune provenance renseignee"
        if not check["provenance"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(contact, ["id"]),
                         "nom_table_correspondante": "contacts",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=day,
                nom_table_correspondante="contacts",
                est_corrige=False,
                id_correspondant=safe_dict_get(contact, ["id"])
            )
            dprint(f"[{safe_dict_get(contact, ['id'])}] {defaut}", priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(contact, ["id"]),
                         "nom_table_correspondante": "contacts",
                         "defaut": defaut},
                est_corrige=True,
            )

        defaut = "Defaut KPI8: Contact cree mais aucun detail sur sa provenance est renseigne"
        if not check["details_provenance"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(contact, ["id"]),
                         "nom_table_correspondante": "contacts",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=day,
                nom_table_correspondante="contacts",
                est_corrige=False,
                id_correspondant=safe_dict_get(contact, ["id"])
            )
            dprint(f"[{safe_dict_get(contact, ['id'])}] {defaut}", priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(contact, ["id"]),
                         "nom_table_correspondante": "contacts",
                         "defaut": defaut},
                est_corrige=True,
            )

    for contact in get_list_of_element("/contacts", startDate=day, endDate=day, period="updated"):
        _create_failure(contact, day)


def controle_qualite_kpi8(day):
    """
    Controle qualite KPI8
    :param day:
    :return:
    """

    # Point de controle 1:
    """
    Reporting hebdo des clients sans provenance
    """
    dprint(f"KPI8: controle qualite 1", priority_level=3, preprint="\n")
    controle_1(day)
