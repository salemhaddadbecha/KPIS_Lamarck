def safe_dict_get(data, list_keys):
    """
    Permet d'accéder à la valeur d'un dictionnaire composé: valuer accéssible par
    la succession de clés.
    Fonctionne également pour les listes.
    En cas de clé incorrecte retourne None
    :param data:
    :param list_keys:
    :param fail_result:
    :return: valeur ciblée
    """
    target_value = data
    for key in list_keys:

        if isinstance(key, (str, int)):
            try:
                target_value = target_value[key]
            except:
                return None

    return target_value


def is_in_the_list(research_list, value):
    """
    Amelioration de l'operand 'in', fonctionne avec les entiers
    :param research_list:
    :param value:
    :return: est dedans (Boolean)
    """
    for element in research_list:
        if element == value:
            return True
    return False


def safe_count_type_of_dict_in_list(research_list, list_keys_to_indentify_type_of_dict, target_type):
    """
    Compte le nombre d'occurences d'une valeur dans une liste

    :param research_list:
    :param list_keys_to_indentify_type_of_dict:
    :param target_type:
    :return: nombre d'occurences
    """
    count = 0
    try:
        if isinstance(research_list, list):
            for element in research_list:
                if isinstance(target_type, list):
                    count += is_in_the_list(target_type, safe_dict_get(element, list_keys_to_indentify_type_of_dict))
                else:
                    count += (safe_dict_get(element, list_keys_to_indentify_type_of_dict) == target_type)
    except:
        pass
    return count


def safe_date_convert(date_str):
    """
    Permet de convertir un string() en date.
    En cas d'erreur de conversion retourne None
    :param date_str:
    :return:
    """
    formated_date = None

    from datetime import datetime
    # Format boond = 2022-07-07T09:52:57+0200
    if date_str is not None:
        split_date = date_str.split("T")
        try:
            formated_date = datetime.strptime(split_date[0], "%Y-%m-%d")
        except:
            pass

    return formated_date


def dprint(str_to_print, priority_level=1, preprint="", hashtag_display=True):
    """
    Fonction de print, dépend du paramètre global de l'app DEBUG
    Inclus une fonctionnalité de priorité de print dépendant du paramètre global de l'app PRIORITY_DEBUG_LEVEL
    ainsi que d'une indentation représentée par des "-" liée à la priorité de print
    :param str_to_print:
    :param priority_level:
    :param preprint:
    :param hashtag_display:
    :return:
    """
    from configuration import APP_CONFIG
    if APP_CONFIG.DEBUG and APP_CONFIG.PRIORITY_DEBUG_LEVEL >= priority_level:
        str_ident = "".join("-" for _ in range(priority_level))
        if hashtag_display:
            print(f"{preprint}#{str_ident} {str_to_print}")
        else:
            print(f"{preprint}{str_to_print}")


def safe_update_table_row(table, filters, **params):
    """
    Permet de mettre à jour une ligne dans une table
    vérifie si l'élément existe déjà, si oui on le met à jour
    sinon on le crée.
    :param table:
    :param filters:
    :param **params:
    :return:
    """
    from connectors.database_connectors import get_database_session

    if table is not None and filters is not None:
        with get_database_session() as session:

            row = None
            for index, (filter_key, filter_value) in enumerate(filters.items()):
                # Premier filtre -> on crée la requête
                if index == 0:
                    row = session.query(table)

                # Si la clé de la colonne et la clé de que l'on veut changer correspondent alors on fait la modif
                row = row.filter(getattr(table, filter_key) == filter_value)

            # Test d'existance
            result = row.all()

            # Si plusieurs row sont trouvées -> on les supprime toutes sauf une
            if len(result) > 1:
                for row in result[1:]:
                    session.delete(row)

            # Si une row est trouvée (forcément une unique) alors on l'update
            if len(result) == 1:
                for key, value in params.items():
                    try:
                        row.update({getattr(table, key): value})
                    except:
                        pass

            # Sinon on crée la ligne
            # Si c'est une update est_corrige = True, on ne crée pas de nouvel élément
            elif params.get("est_corrige", None) is False or params.get("est_corrige", None) is None:
                new_row = table(**params)
                session.add(new_row)

            session.commit()


def get_period_dates():
    """
    Permet de récupérer la period de travail
    demandee
    :param:
    :return: [date de debut, date de fin]
    """
    from configuration import APP_CONFIG
    from datetime import datetime, timedelta

    date = datetime.today()
    if APP_CONFIG.CRONJOB_EXECUTION == "jour_precedent":
        yesterday = date - timedelta(days=1)
        return [yesterday.strftime('%Y-%m-%d'), yesterday.strftime('%Y-%m-%d')]

    elif APP_CONFIG.CRONJOB_EXECUTION == "test_period":
        last_month = date - timedelta(weeks=2)
        return [last_month.strftime('%Y-%m-%d'), date.strftime('%Y-%m-%d')]

    return [date.strftime('%Y-%m-%d'), date.strftime('%Y-%m-%d')]


def get_current_date():
    """
    Permet la date du jour
    :param:
    :return: date du jour
    """
    from datetime import datetime
    return datetime.today()


def safe_table_read(table, filters):
    """
    Permet lire les lignes d'un tableau en focntion de filtres
    :param: table
    :param: filters
    :return: liste des lignes
    """
    from connectors.database_connectors import get_database_session
    result = None
    try:
        if table is not None:
            with get_database_session() as session:
                # On crée la requête
                row = session.query(table)

                # Si filtre non renseigné (on veut toute la table)
                if filters is None:
                    row = row.filter(getattr(table, "id") >= 0)

                else:
                    for index, (filter_key, filter_value) in enumerate(filters.items()):
                        # Si la clé de la colonne et la clé de que l'on veut changer correspondent alors on fait la modif
                        row = row.filter(getattr(table, filter_key) == filter_value)

                result = row.all()
    except:
        pass

    return result
