# Modules / Dépendances
from tables import Controle_qualite
from modules.requests_tools import request, get_list_of_element
from modules.safe_actions import safe_dict_get, is_in_the_list, safe_update_table_row, get_current_date, dprint, get_period_dates


def controle_1(start_date, end_date):
    def create_failure(contact):
        def get_contact_provenance(contact):
            informations = request(f"/contacts/{contact['id']}/information")
            check = {
                "provenance": False,
                "details_provenance": False
            }

            if safe_dict_get(informations, ["data", "attributes", "origin", "typeOf"]) is not None and \
                    not is_in_the_list([-1, "-1"], safe_dict_get(informations, ["data", "attributes", "origin", "typeOf"])):
                check["provenance"] = True

            if safe_dict_get(informations, ["data", "attributes", "origin", "detail"]) is not None and \
                    safe_dict_get(informations, ["data", "attributes", "origin", "detail"]) != "":
                check["details_provenance"] = True

            return check

        check = get_contact_provenance(contact)

        if not check["provenance"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(contact, ["id"]),
                         "nom_table_correspondante": "candidates",
                         "defaut": "Défaut KPI8: Contact créé mais aucune provenance renseignée"},
                defaut=f"Défaut KPI8: Contact créé mais aucune provenance renseignée",
                date_releve=get_current_date(),
                nom_table_correspondante="contacts",
                id_correspondant=safe_dict_get(contact, ["id"])
            )
            dprint(f"#-- [{safe_dict_get(contact, ['id'])}] Défaut KPI8: Contact créé mais aucune provenance renseignée")


        if not check["details_provenance"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(contact, ["id"]),
                         "nom_table_correspondante": "candidates",
                         "defaut": "Défaut KPI8: Contact créé mais aucun détail sur sa provenance est renseigné"},
                defaut=f"Défaut KPI8: Contact créé mais aucun détail sur sa provenance est renseigné",
                date_releve=get_current_date(),
                nom_table_correspondante="contacts",
                id_correspondant=safe_dict_get(contact, ["id"])
            )
            dprint(f"#-- [{safe_dict_get(contact, ['id'])}] Défaut KPI8: Contact créé mais aucun détail sur sa provenance est renseigné")


    for contact in get_list_of_element("/contacts", startDate=start_date, endDate=end_date, period="updated"):
        create_failure(contact)

def controle_qualite_kpi8():
    dates = get_period_dates()

    # Point de contrôle 1:
    """
    Reporting hebdo des clients sans provenance
    """
    dprint(f"#- KPI8: contrôle qualité 1")
    controle_1(dates[0], dates[1])

