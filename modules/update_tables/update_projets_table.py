# Modules / Dependances
from tables import Projets
# Tools
from tools.requests_tools import get_list_of_element
from tools.safe_actions import safe_dict_get, safe_date_convert, dprint, safe_update_table_row


def get_projet_all_informations(basic_data, included_data):
    """
    Retrieves all relevant information about a project, including company name.
    :param basic_data: Basic project data
    :param included_data: Included data from the API response
    :return: Useful project information
    """
    # Infos à trouver
    informations = {
        "boond_id": int(),
        "boond_rm_id": int(),
        "boond_besoin_id": int(),
        "date_de_debut": None,
        "date_de_fin": None,
        "company_name": None  # Add company name to be fetched
    }
    informations["boond_id"] = safe_dict_get(basic_data, ["id"])
    informations["boond_rm_id"] = safe_dict_get(basic_data, ["relationships", "mainManager", "data", "id"])
    informations["boond_besoin_id"] = safe_dict_get(basic_data, ["relationships", "opportunity", "data", "id"])
    informations["date_de_debut"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "startDate"]))
    informations["date_de_fin"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "endDate"]))

    # Retrieve the company ID from basic_data
    company_id = safe_dict_get(basic_data, ["relationships", "company", "data", "id"])

    # Look for the company in the included data
    for included in included_data:
        if included["type"] == "company" and included["id"] == company_id:
            informations["company_name"] = safe_dict_get(included, ["attributes", "name"])
            break

    return informations


def check_new_and_update_projets(start_day, end_day):
    """
    Updates and adds new projects to the Projets table.
    :param start_day: Start date for the update range
    :param end_day: End date for the update range
    :return: None
    """
    dprint("Update project table", priority_level=3, preprint="\n")

    # Fetch both basic and included data from the API
    list_of_projets_to_update = get_list_of_element(
        "/projects",
        period="updated",
        startDate=start_day,
        endDate=end_day
    )

    included_data = list_of_projets_to_update.get('included', [])

    for projet in list_of_projets_to_update['data']:
        projet_to_update_all_informations = get_projet_all_informations(projet, included_data)  # Pass included data

        # Update the database with the new information, including the company name
        safe_update_table_row(
            table=Projets,
            filters={"boond_id": projet_to_update_all_informations["boond_id"]},
            boond_id=projet_to_update_all_informations["boond_id"],
            boond_rm_id=projet_to_update_all_informations["boond_rm_id"],
            boond_besoin_id=projet_to_update_all_informations["boond_besoin_id"],
            date_de_debut=projet_to_update_all_informations["date_de_debut"],
            date_de_fin=projet_to_update_all_informations["date_de_fin"],
            company_name=projet_to_update_all_informations["company_name"]  # Include the company name
        )
        dprint("Update project: {}".format(projet_to_update_all_informations['boond_id']), priority_level=4)
