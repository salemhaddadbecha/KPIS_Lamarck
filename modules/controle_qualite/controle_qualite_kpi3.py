# Modules / Dependances
from tables import Controle_qualite
# Tools
from tools.requests_tools import request, get_list_of_element
from tools.safe_actions import safe_dict_get, safe_update_table_row, dprint


def controle_1(day):
    """
    Existence pour tous les consultants d’au
    moins une ligne dans le bloc Ressources > Administratif > Contrat RH
    :param day:
    :return:
    """

    def _create_failure(resource, day):
        """
        Crée ou non (en fonction des consignes de controle) un relevé de défaut dans la table Controle qualite
        :param resource:
        :param day:
        :return:
        """

        def _get_hr_contract(resource):
            """
            Permet de récupérer tous les contrats RH d'une ressource
            :param resource:
            :return:
            """
            check = False
            administrative = request(f"/resources/{safe_dict_get(resource, ['id'])}/administrative")

            if safe_dict_get(administrative, ["data", "relationships", "contracts", "data"]) is not None and \
                    len(safe_dict_get(administrative, ["data", "relationships", "contracts", "data"])) > 0:
                check = True

            return check

        defaut = "Defaut KPI3: aucun contract RH renseigne sur la resource"
        if not _get_hr_contract(resource):
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=day,
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

    for resource in get_list_of_element("/resources", startDate=day, endDate=day, period="updated"):
        _create_failure(resource, day)


def controle_2(day):
    """
    Mettre à jour l’ensemble des titres de profils Ressources pour standardiser
    les titres avec le profil du consultant
    :param day:
    :return:
    """

    def _create_failure(resource, day):
        """
        Crée ou non (en fonction des consignes de controle) un relevé de défaut dans la table Controle qualite
        :param resource:
        :param day:
        :return:
        """
        liste_titre_autorise = [
            "Business Development Manager",
            "Business Manager",
            "Charge des Ressources Humaines",
            "Chargee de communication",
            "Chargee de recrutement",
            "Consultant",
            "Consultant Confirme",
            "Consultant Directeur",
            "Consultant Junior",
            "Consultant Manager",
            "Consultant Senior",
            "Consultante",
            "Consultante Confirmee",
            "Consultante Senior",
            "DG",
            "Directeur",
            "Directeur Lab Innovation",
            "DRH",
            "Freelance",
            "Responsable Ressources Humaines"
        ]
        title = safe_dict_get(resource, ["attributes", "title"])

        defaut = f"Defaut KPI3: titre de la resource non conforme: '{title}'"
        if title not in liste_titre_autorise:
            safe_update_table_row(
                table=Controle_qualite,
                filters={"id_correspondant": safe_dict_get(resource, ["id"]),
                         "nom_table_correspondante": "ressources",
                         "defaut": defaut},
                defaut=defaut,
                date_releve=day,
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

    for resource in get_list_of_element("/resources", startDate=day, endDate=day, period="updated"):
        _create_failure(resource, day)


def controle_qualite_kpi3(day):
    """
    Controle qualite KPI3
    :param day:
    :return:
    """

    # Point de controle 1:
    """
    Existence pour tous les consultants d’au
    moins une ligne dans le bloc Ressources > Administratif > Contrat RH
    """
    dprint(f"KPI3: controle qualite 1", priority_level=3, preprint="\n")
    controle_1(day)

    # Point de controle 2:
    """
    Mettre à jour l’ensemble des titres de profils Ressources pour standardiser 
    les titres avec le profil du consultant
    """
    dprint(f"KPI3: controle qualite 2", priority_level=3, preprint="\n")
    controle_2(day)
