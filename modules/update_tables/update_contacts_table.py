# Modules / Dépendances
from tables import Contacts
from modules.requests_tools import request, get_list_of_element
from modules.safe_actions import safe_dict_get, safe_date_convert, dprint, safe_update_table_row, get_period_dates

def get_contact_all_informations(basic_data):
    # Indexation d'éléments utiles:
    provenances =  ["prospection", "1", "consultant", "réseau", "appel d'offre", "non renseigné",] # index-1 pour avoir la valeur correspondante / dernier index reservé au non renseigné auquel l'index est de -1

    informations = {
        "boond_id": int(),
        "boond_rm_id": int(),
        "nom": str(),
        "prenom": str(),
        "provenance": str(),
        "detail_provenance": str(),
        "date_de_creation": None
    }
    informations["boond_id"] = safe_dict_get(basic_data, ["id"])
    informations["boond_rm_id"] = safe_dict_get(basic_data, ["relationships", "mainManager", "data", "id"])
    informations["nom"] = safe_dict_get(basic_data, ["attributes", "lastName"])
    informations["prenom"] = safe_dict_get(basic_data, ["attributes", "firstName"])
    informations["date_de_creation"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "creationDate"]))

    # Pour la provenance et la date il nous faut plus d'informations
    contact = request(f"/contacts/{informations['boond_id']}/information")

    if safe_dict_get(contact, ["data", "attributes", "origin", "typeOf"]) is not None:
        informations["provenance"] = safe_dict_get(provenances, [int(safe_dict_get(contact, ["data", "attributes", "origin", "typeOf"]))])
    informations["detail_provenance"] = safe_dict_get(contact, ["data", "attributes", "origin", "detail"])

    return informations


def check_new_and_update_contacts():
    dates = get_period_dates()

    # Update contact -> type = updated
    dprint(f"#- Update contact: period({dates[0]})")
    list_of_contacts_to_update = get_list_of_element("/contacts", period="updated", startDate=dates[0], endDate=dates[1])

    for contact_to_update_basic_informations in list_of_contacts_to_update:
        contact_to_update_all_informations = get_contact_all_informations(contact_to_update_basic_informations)

        safe_update_table_row(
            table=Contacts,
            filters={"boond_id": contact_to_update_all_informations["boond_id"]},
            boond_id=contact_to_update_all_informations["boond_id"],
            boond_rm_id=contact_to_update_all_informations["boond_rm_id"],
            nom=contact_to_update_all_informations["nom"],
            prenom=contact_to_update_all_informations["prenom"],
            provenance=contact_to_update_all_informations["provenance"],
            detail_provenance=contact_to_update_all_informations["detail_provenance"],
            date_de_creation=contact_to_update_all_informations["date_de_creation"]
        )
        dprint(f"#-- Update candidat: {contact_to_update_all_informations['nom']} {contact_to_update_all_informations['prenom']}")

    dprint("\n")