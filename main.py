# Librairie
from datetime import timedelta
from threading import Thread
from time import sleep
from concurrent.futures import ThreadPoolExecutor

# Modules / Dependances
from configuration import APP_CONFIG
# Tools
from tools.safe_actions import dprint, safe_date_convert, get_period_dates
# Modules
from modules.update_tables.update_candidats_table import check_new_and_update_candidates
from modules.update_tables.update_resources_table import check_new_and_update_resources
from modules.update_tables.update_besoins_table import check_new_and_update_besoins
from modules.update_tables.update_projets_table import check_new_and_update_projets
from modules.update_tables.update_prestations_table import check_new_and_update_prestations
from modules.update_tables.update_contacts_table import check_new_and_update_contacts
from modules.update_tables.update_actions_table import check_new_and_update_actions
from modules.update_tables.update_temps_table import check_new_and_update_temps

from modules.controle_qualite.controle_qualite_kpi1 import controle_qualite_kpi1
from modules.controle_qualite.controle_qualite_kpi2 import controle_qualite_kpi2
from modules.controle_qualite.controle_qualite_kpi3 import controle_qualite_kpi3
from modules.controle_qualite.controle_qualite_kpi6 import controle_qualite_kpi6
from modules.controle_qualite.controle_qualite_kpi8 import controle_qualite_kpi8
from modules.controle_qualite.controle_qualite_kpi12 import controle_qualite_kpi12
from modules.controle_qualite.controle_qualite_kpi16 import controle_qualite_kpi16


def datespan(start_date, end_date, delta):
    current_date = start_date
    while current_date < end_date:
        yield current_date.strftime('%Y-%m-%d')
        current_date += delta

dates = get_period_dates()

dprint(f"Run KPIs database script, for the period: from {dates[0]} to {dates[1]}", priority_level=1)
# On itere les jours presents dans la plage de temps (periode) pour avoir un element de temps par jour et par personne
for day in datespan(start_date=safe_date_convert(dates[0]), end_date=safe_date_convert(dates[1]), delta=timedelta(days=1)):
    dprint(f"Update the day: {day}, (period: from {dates[0]} to {dates[1]})", priority_level=2)
    dprint(f"Update multithreading mode: {APP_CONFIG.MULTI_THREADING}\n\n", priority_level=2)

    # 8 tables + 6 controles qualites = 14 fonctions en paralleles
    if APP_CONFIG.MULTI_THREADING == "no":
        # Update table
        check_new_and_update_candidates(day)
        check_new_and_update_resources(day)
        check_new_and_update_besoins(day)
        check_new_and_update_projets(day)
        check_new_and_update_temps(day)
        check_new_and_update_prestations(day)
        check_new_and_update_contacts(day)
        check_new_and_update_actions(day)

        dprint("\n", hashtag_display=False)

        # Controle qualite
        controle_qualite_kpi1(day)
        controle_qualite_kpi2(day)
        controle_qualite_kpi3(day)
        # controle_qualite_kpi6(day) rien à faire -> concerne l'operationnel
        controle_qualite_kpi8(day)
        controle_qualite_kpi12(day)
        controle_qualite_kpi16(day)

        dprint("\n", hashtag_display=False)

    elif APP_CONFIG.MULTI_THREADING == "soft":
        with ThreadPoolExecutor(14) as executor:
            # Update table
            executor.submit(check_new_and_update_candidates, day)
            executor.submit(check_new_and_update_resources, day)
            executor.submit(check_new_and_update_besoins, day)
            executor.submit(check_new_and_update_projets, day)
            executor.submit(check_new_and_update_temps, day)
            executor.submit(check_new_and_update_prestations, day)
            executor.submit(check_new_and_update_contacts, day)
            executor.submit(check_new_and_update_actions, day)

            # Controle qualite
            executor.submit(controle_qualite_kpi1, day)
            executor.submit(controle_qualite_kpi2, day)
            executor.submit(controle_qualite_kpi3, day)
            executor.submit(controle_qualite_kpi8, day)
            executor.submit(controle_qualite_kpi12, day)
            executor.submit(controle_qualite_kpi16, day)

    elif APP_CONFIG.MULTI_THREADING == "hard":
        # Update table
        Thread(target=check_new_and_update_candidates, args=day).start()
        Thread(target=check_new_and_update_resources, args=day).start()
        Thread(target=check_new_and_update_besoins, args=day).start()
        Thread(target=check_new_and_update_projets, args=day).start()
        Thread(target=check_new_and_update_temps, args=day).start()
        Thread(target=check_new_and_update_prestations, args=day).start()
        Thread(target=check_new_and_update_contacts, args=day).start()
        Thread(target=check_new_and_update_actions, args=day).start()

        # Controle qualite
        Thread(target=controle_qualite_kpi1, args=day).start()
        Thread(target=controle_qualite_kpi2, args=day).start()
        Thread(target=controle_qualite_kpi3, args=day).start()
        Thread(target=controle_qualite_kpi8, args=day).start()
        Thread(target=controle_qualite_kpi12, args=day).start()
        Thread(target=controle_qualite_kpi16, args=day).start()

        sleep(60)


