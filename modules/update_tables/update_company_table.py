# Modules / Dependances
from tables import Company
# Tools
from tools.requests_tools import get_list_of_element
from tools.safe_actions import safe_dict_get, safe_date_convert, dprint, safe_update_table_row


def get_company_all_informations(basic_data):
    """
    Permet de recuperer toutes les informations utiles
    d'une compaby a partir de ses informations basiques
    :param basic_data:
    :return: informations utiles du projet
    """
    # Infos à trouver
    informations = {
        "boond_id": int(),
        "boond_rm_id": int(),
        "company_name": None,
        "country": None,
        "phone": None


    }
    informations["boond_id"] = safe_dict_get(basic_data, ["id"])
    informations["boond_rm_id"] = safe_dict_get(basic_data, ["relationships", "mainManager", "data", "id"])
    informations["company_name"] = safe_dict_get(basic_data, ["attributes", "name"])
    informations["country"] = safe_dict_get(basic_data, ["attributes", "country"])
    informations["phone"] = safe_dict_get(basic_data, ["attributes", "phone1"])

    return informations


def check_new_and_update_company(start_day, end_day):
    """
    Met à jour et ajoute tous les nouveaux comapnies à la table Company:
    :param day:
    :return:
    """
    dprint("Update company table", priority_level=3, preprint="\n")
    list_of_companies_to_update = get_list_of_element(
        "/companies",
        period="updated",
        startDate=start_day,
        endDate=end_day
    )

    for company_to_update_basic_informations in list_of_companies_to_update['data']:
        company_to_update_all_informations = get_company_all_informations(company_to_update_basic_informations)
        safe_update_table_row(
            table=Company,
            filters={"boond_id": company_to_update_all_informations["boond_id"]},
            boond_id=company_to_update_all_informations["boond_id"],
            boond_rm_id=company_to_update_all_informations["boond_rm_id"],
            company_name=company_to_update_all_informations["company_name"],
            country=company_to_update_all_informations["country"],
            phone=company_to_update_all_informations["phone"]
        )
        dprint("Update company: {}".format(company_to_update_all_informations['boond_id']), priority_level=4)