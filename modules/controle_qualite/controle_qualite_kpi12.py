# Modules / Dependances
from tables import Controle_qualite
# Tools
from tools.requests_tools import get_list_of_element
from tools.safe_actions import safe_dict_get, safe_date_convert, safe_update_table_row, get_current_date, dprint


def controle_1(start_date, end_date):
    def _create_failure(resource):
        """
        Crée ou non (en fonction des consignes de controle) un relevé de défaut dans la table Controle qualite
        :param resource:
        :return:
        """

        def _get_last_prestation(resource):
            """
            Permet de recuperer la derniere prestation d une ressource
            :param resource:
            :return: informations sur la derniere prestation d une ressource
            """
            prestations = get_list_of_element(f"/resources/{resource['id']}/deliveries-inactivities")
            last_prestation = safe_dict_get(prestations, [0])
            last_prestation_lite = {
                "etat": None,
                "en_cours": False,
                "debut": False,
                "fin": False
            }

            if safe_dict_get(resource, ["attributes", "state"]) is not None:
                liste_etats = ["out", "en mission", "en interne", "en arrêt", "signe"]
                last_prestation_lite["etat"] = safe_dict_get(liste_etats,
                                                             [int(safe_dict_get(resource, ["attributes", "state"]))])

            if safe_dict_get(last_prestation, ["attributes", "startDate"]) is not None:
                last_prestation_lite["debut"] = safe_date_convert(
                    safe_dict_get(last_prestation, ["attributes", "startDate"]))

            if safe_dict_get(last_prestation, ["attributes", "endDate"]) is not None:
                last_prestation_lite["fin"] = safe_date_convert(
                    safe_dict_get(last_prestation, ["attributes", "endDate"]))

            if last_prestation_lite["debut"] is not False and \
                    last_prestation_lite["fin"] is not False and \
                    last_prestation_lite["debut"] <= get_current_date() <= last_prestation_lite["fin"]:
                last_prestation_lite["en_cours"] = True
            return last_prestation_lite

        last_prestation = _get_last_prestation(resource)

        defaut = f"Defaut KPI12: Le dernier contrat de " \
                 f"{safe_dict_get(resource, ['attributes', 'lastName'])} " \
                 f"{safe_dict_get(resource, ['attributes', 'firstName'])}" \
                 f" n'a pas de date de debut"

        if not last_prestation["debut"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=get_current_date(),
                nom_table_correspondante="ressources",
                est_corrige=False,
                id_correspondant=safe_dict_get(resource, ["id"])
            )
            dprint(f"[{safe_dict_get(resource, ['id'])}] {defaut}", priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                est_corrige=True,
            )

        defaut = f"Defaut KPI12: Le dernier contrat de " \
                 f"{safe_dict_get(resource, ['attributes', 'lastName'])} " \
                 f"{safe_dict_get(resource, ['attributes', 'firstName'])}" \
                 f" n'a pas de date de fin"

        if not last_prestation["fin"]:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=get_current_date(),
                nom_table_correspondante="ressources",
                est_corrige=False,
                id_correspondant=safe_dict_get(resource, ["id"])
            )
            dprint(f"[{safe_dict_get(resource, ['id'])}] {defaut}", priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                est_corrige=True,
            )

        defaut = f"Defaut KPI12: " \
                 f"{safe_dict_get(resource, ['attributes', 'lastName'])} " \
                 f"{safe_dict_get(resource, ['attributes', 'firstName'])}" \
                 f" n'a pas d'etat de renseigne (en mission, en interne, etc)"
        if last_prestation["etat"] is None:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=get_current_date(),
                nom_table_correspondante="ressources",
                est_corrige=False,
                id_correspondant=safe_dict_get(resource, ["id"])
            )
            dprint(f"[{safe_dict_get(resource, ['id'])}] {defaut}", priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                est_corrige=True,
            )

        defaut = f"Defaut KPI12: " \
                 f"{safe_dict_get(resource, ['attributes', 'lastName'])} " \
                 f"{safe_dict_get(resource, ['attributes', 'firstName'])}" \
                 f" etat 'en mission' alors qu'aucune mission est en cours"
        if last_prestation["etat"] == "en mission" and last_prestation["en_cours"] == False:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=get_current_date(),
                nom_table_correspondante="ressources",
                est_corrige=False,
                id_correspondant=safe_dict_get(resource, ["id"])
            )
            dprint(f"[{safe_dict_get(resource, ['id'])}] {defaut}", priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                est_corrige=True,
            )

        defaut = f"Defaut KPI12: " \
                 f"{safe_dict_get(resource, ['attributes', 'lastName'])} " \
                 f"{safe_dict_get(resource, ['attributes', 'firstName'])}" \
                 f" etat 'en interne' alors qu'une mission est en cours"
        if last_prestation["etat"] == "en interne" and last_prestation["en_cours"] == True:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=get_current_date(),
                nom_table_correspondante="ressources",
                est_corrige=False,
                id_correspondant=safe_dict_get(resource, ["id"])
            )
            dprint(f"[{safe_dict_get(resource, ['id'])}] {defaut}", priority_level=4)
        else:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                est_corrige=True,
            )

    for resource in get_list_of_element("/resources", startDate=start_date, endDate=end_date, period="updated"):
        _create_failure(resource)


def controle_qualite_kpi12(start_date, end_date):
    """
    Controle qualite KPI12
    :param start_date:
    :param end_date:
    :return:
    """
    dates = [start_date, end_date]
    # Point de controle 1:
    """
    Mise à jour de l’etat de la Ressource sur Boond
    """
    dprint(f"KPI12: controle qualite 1", priority_level=3, preprint="\n")
    controle_1(dates[0], dates[1])
