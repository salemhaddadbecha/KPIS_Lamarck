# Modules / Dépendances
from tables import Actions
from modules.requests_tools import get_list_of_element
from modules.safe_actions import safe_dict_get, safe_date_convert, dprint, safe_update_table_row, get_period_dates

def get_action_all_informations(basic_data):
    # Indexation d'éléments utiles:
    types = [str(index) for index in range(500)]

    # On s'intéresse uniquement aux actions: proposition sur profil(candidat, 43) / proposition sur mission(candidat, 130) / prospection(contacts, 61) / soutenance(contacts, 10)
    types[10] = "soutenance"
    types[43] = "proposition sur profil"
    types[61] = "prospection"
    types[130] = "proposition sur mission"

    informations = {
        "boond_id": int(),
        "date_de_creation": None,
        "table_associee": str(),
        "type": int(),
        "boond_id_element_associe": str()
    }

    informations["boond_id"] = safe_dict_get(basic_data, ["id"])
    informations["date_de_creation"] = safe_date_convert(safe_dict_get(basic_data, ["attributes", "creationDate"]))

    # Actions qui nous intéresse : proposition sur profil(candidat, 43) / proposition sur mission(candidat, 130) / prospection(contacts, 61) / soutenance(contacts, 10)
    # Actions liées à la table "candidats"
    if safe_dict_get(types, [safe_dict_get(basic_data, ["attributes", "typeOf"])]) == "proposition sur profil":
        informations["table_associee"] = "candidats"
        informations["type"] = "proposition sur profil"
        informations["boond_id_element_associe"] = safe_dict_get(basic_data, ["relationships", "dependsOn", "data", "id"])

    elif safe_dict_get(types, [safe_dict_get(basic_data, ["attributes", "typeOf"])]) == "proposition sur mission":
        informations["table_associee"] = "candidats"
        informations["type"] = "proposition sur mission"
        informations["boond_id_element_associe"] = safe_dict_get(basic_data, ["relationships", "dependsOn", "data", "id"])

    # Actions liées à la table "contacts"
    elif safe_dict_get(types, [safe_dict_get(basic_data, ["attributes", "typeOf"])]) == "prospection":
        informations["table_associee"] = "contacts"
        informations["type"] = "prospection"
        informations["boond_id_element_associe"] = safe_dict_get(basic_data, ["relationships", "dependsOn", "data", "id"])

    elif safe_dict_get(types, [safe_dict_get(basic_data, ["attributes", "typeOf"])]) == "soutenance":
        informations["table_associee"] = "contacts"
        informations["type"] = "soutenance"
        informations["boond_id_element_associe"] = safe_dict_get(basic_data, ["relationships", "dependsOn", "data", "id"])

    return informations


def check_new_and_update_actions_with_param(filter):
    dates = get_period_dates()

    # Update action -> type = updated
    dprint(f"#- Update action type {filter}")
    dprint(f"#-- Update action: period({dates[0]})")
    list_of_actions_to_update = get_list_of_element("/actions", period="updated", actionTypes=filter, startDate=dates[0], endDate=dates[1])

    for action_to_update_basic_informations in list_of_actions_to_update:
        action_to_update_all_informations = get_action_all_informations(action_to_update_basic_informations)

        safe_update_table_row(
            table=Actions,
            filters={"boond_id": action_to_update_all_informations["boond_id"]},
            boond_id=action_to_update_all_informations["boond_id"],
            date_de_creation=action_to_update_all_informations["date_de_creation"],
            table_associee=action_to_update_all_informations["table_associee"],
            type=action_to_update_all_informations["type"],
            boond_id_element_associe=action_to_update_all_informations["boond_id_element_associe"]
        )
        dprint(f"#--- Update action: {action_to_update_all_informations['boond_id']}")

    dprint("\n")

def check_new_and_update_actions():
    # Actions qui nous intéresse : proposition sur profil(candidat, 43) / proposition sur mission(candidat, 130) / prospection(contacts, 61) / soutenance(contacts, 10)
    check_new_and_update_actions_with_param(43)
    check_new_and_update_actions_with_param(130)
    check_new_and_update_actions_with_param(61)
    check_new_and_update_actions_with_param(10)