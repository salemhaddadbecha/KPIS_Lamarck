def safe_dict_get(data, list_keys):
    target_value = data
    for key in list_keys:

        if isinstance(key, (str, int)):
            try:
                target_value = target_value[key]
            except:
                return None

    return target_value


def is_in_the_list(research_list, value):
    for element in research_list:
        if element == value:
            return True
    return False


def safe_count_type_of_dict_in_list(research_list, list_keys_to_indentify_type_of_dict, target_type):
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


def dprint(str_to_print):
    from configuration import APP_CONFIG
    if APP_CONFIG.DEBUG:
        print(str_to_print)


def safe_update_table_row(table, filters, **params):
    from sqlalchemy import inspect
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
            else:
                new_row = table(**params)
                session.add(new_row)

            session.commit()


def get_period_dates():
    from configuration import APP_CONFIG
    from datetime import datetime, timedelta

    date = datetime.today()
    if APP_CONFIG.CRONJOB_EXECUTION == "jour_precedent":
        yesterday = date - timedelta(days=1)
        return [yesterday.strftime('%Y-%m-%d'), yesterday.strftime('%Y-%m-%d')]

    elif APP_CONFIG.CRONJOB_EXECUTION == "test_period":
        last_month = date - timedelta(weeks=4)
        return [last_month.strftime('%Y-%m-%d'), date.strftime('%Y-%m-%d')]

    return [date.strftime('%Y-%m-%d'), date.strftime('%Y-%m-%d')]

def get_current_date():
    from datetime import datetime
    return datetime.today()