# Modules / Dépendances
from tables import Controle_qualite
from modules.requests_tools import get_list_of_element
from modules.safe_actions import safe_dict_get, safe_date_convert, safe_update_table_row, get_current_date, get_period_dates, dprint


def controle_1(start_date, end_date):
    def create_failure(resource):
        def get_last_prestation(resource):
            prestations = get_list_of_element(f"/resources/{resource['id']}/deliveries-inactivities")
            last_prestation = safe_dict_get(prestations, [0])
            last_prestation_lite = {
                "etat": None,
                "en_cours": False,
                "debut": False,
                "fin": False
            }

            if safe_dict_get(resource, ["attributes", "state"]) is not None:
                liste_etats = ["out", "en mission", "en interne", "en arrêt", "signé"]
                last_prestation_lite["etat"] = safe_dict_get(liste_etats, [int(safe_dict_get(resource, ["attributes", "state"]))])

            if safe_dict_get(last_prestation, ["attributes", "startDate"]) is not None:
                last_prestation_lite["debut"] = safe_date_convert(safe_dict_get(last_prestation, ["attributes", "startDate"]))

            if safe_dict_get(last_prestation, ["attributes", "endDate"]) is not None:
                last_prestation_lite["fin"] = safe_date_convert(safe_dict_get(last_prestation, ["attributes", "endDate"]))

            if last_prestation_lite["debut"] is not False and \
                    last_prestation_lite["fin"] is not False and \
                    last_prestation_lite["debut"] <= get_current_date() <= last_prestation_lite["fin"]:

                last_prestation_lite["en_cours"] = True
            return last_prestation_lite

        last_prestation = get_last_prestation(resource)

        if not last_prestation["debut"]:
            defaut = f"Défaut KPI12: Le dernier contrat de "\
                     f"{safe_dict_get(resource, ['attributes', 'lastName'])} "\
                     f"{safe_dict_get(resource, ['attributes', 'firstName'])}"\
                     f" n'a pas de date de début"

            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=get_current_date(),
                nom_table_correspondante="ressources",
                id_correspondant=safe_dict_get(resource, ["id"])
            )
            dprint(f"#-- [{safe_dict_get(resource, ['id'])}] {defaut}")


        if not last_prestation["fin"]:
            defaut = f"Défaut KPI12: Le dernier contrat de "\
                     f"{safe_dict_get(resource, ['attributes', 'lastName'])} "\
                     f"{safe_dict_get(resource, ['attributes', 'firstName'])}"\
                     f" n'a pas de date de fin"

            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=get_current_date(),
                nom_table_correspondante="ressources",
                id_correspondant=safe_dict_get(resource, ["id"])
            )
            dprint(f"#-- [{safe_dict_get(resource, ['id'])}] {defaut}")


        if last_prestation["etat"] is None:
            defaut = f"Défaut KPI12: "\
                     f"{safe_dict_get(resource, ['attributes', 'lastName'])} "\
                     f"{safe_dict_get(resource, ['attributes', 'firstName'])}"\
                     f" n'a pas d'état de renseigné (en mission, en interne, etc)"

            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=get_current_date(),
                nom_table_correspondante="ressources",
                id_correspondant=safe_dict_get(resource, ["id"])
            )
            dprint(f"#-- [{safe_dict_get(resource, ['id'])}] {defaut}")

        elif last_prestation["etat"] == "en mission" and last_prestation["en_cours"] == False:
            defaut = f"Défaut KPI12: "\
                     f"{safe_dict_get(resource, ['attributes', 'lastName'])} "\
                     f"{safe_dict_get(resource, ['attributes', 'firstName'])}"\
                     f" état 'en mission' alors qu'aucune mission est en cours"

            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=get_current_date(),
                nom_table_correspondante="ressources",
                id_correspondant=safe_dict_get(resource, ["id"])
            )
            dprint(f"#-- [{safe_dict_get(resource, ['id'])}] {defaut}")

        elif last_prestation["etat"] == "en interne" and last_prestation["en_cours"] == True:
            defaut = f"Défaut KPI12: "\
                     f"{safe_dict_get(resource, ['attributes', 'lastName'])} "\
                     f"{safe_dict_get(resource, ['attributes', 'firstName'])}"\
                     f" état 'en interne' alors qu'une mission est en cours"

            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=get_current_date(),
                nom_table_correspondante="ressources",
                id_correspondant=safe_dict_get(resource, ["id"])
            )
            dprint(f"#-- [{safe_dict_get(resource, ['id'])}] {defaut}")


    for resource in get_list_of_element("/resources", startDate=start_date, endDate=end_date, period="updated"):
        create_failure(resource)

def controle_qualite_kpi12():
    dates = get_period_dates()


    # Point de contrôle 1:
    """
    Mise à jour de l’état de la Ressource sur Boond
    """
    dprint(f"#- KPI12: contrôle qualité 1")
    controle_1(dates[0], dates[1])

