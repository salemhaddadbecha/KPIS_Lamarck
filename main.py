from datetime import datetime, timedelta

from modules.update_tables.update_all_actions_table import check_new_and_update_all_actions
from modules.update_tables.update_candidats_table import check_new_and_update_candidates
from modules.update_tables.update_resources_table import check_new_and_update_resources
from modules.update_tables.update_besoins_table import check_new_and_update_besoins
from modules.update_tables.update_projets_table import check_new_and_update_projets
from modules.update_tables.update_prestations_table import check_new_and_update_prestations
from modules.update_tables.update_contacts_table import check_new_and_update_contacts
from modules.update_tables.update_actions_table import check_new_and_update_actions
from modules.update_tables.update_temps_table import check_new_and_update_temps
from modules.update_tables.update_company_table import check_new_and_update_company

from modules.controle_qualite.controle_qualite_kpi1 import controle_qualite_kpi1
from modules.controle_qualite.controle_qualite_kpi2 import controle_qualite_kpi2
from modules.controle_qualite.controle_qualite_kpi3 import controle_qualite_kpi3
from modules.controle_qualite.controle_qualite_kpi8 import controle_qualite_kpi8
from modules.controle_qualite.controle_qualite_kpi12 import controle_qualite_kpi12
from modules.controle_qualite.controle_qualite_kpi16 import controle_qualite_kpi16

# end_date = datetime.now().date().strftime('%Y-%m-%d')
end_date =  '2024-09-02'
# start_date = (datetime.now().date() - timedelta(days=5)).strftime('%Y-%m-%d')
start_date = '2024-09-02'
start_date = datetime.strptime(start_date, "%Y-%m-%d")
end_dt = datetime.strptime(end_date, "%Y-%m-%d")
current_date = start_date
while current_date <= end_dt:
    day_str = current_date.strftime("%Y-%m-%d")
    print(f"Processing date: {day_str}")
    check_new_and_update_candidates(start_day=day_str, end_day=day_str)
    check_new_and_update_resources(start_day=day_str, end_day=day_str)
    check_new_and_update_besoins(start_day=day_str, end_day=day_str)
    check_new_and_update_projets(start_day=day_str, end_day=day_str)
    check_new_and_update_prestations(start_day=day_str, end_day=day_str)
    check_new_and_update_contacts(start_day=day_str, end_day=day_str)
    check_new_and_update_actions(start_day=day_str, end_day=day_str)
    check_new_and_update_all_actions(start_day=day_str, end_day=day_str)
    check_new_and_update_company(start_day=day_str, end_day=day_str)
    check_new_and_update_temps(start_day=day_str, end_day=day_str)
    # controle_qualite_kpi1()
    # controle_qualite_kpi2()
    # controle_qualite_kpi3()
    # controle_qualite_kpi8()
    # controle_qualite_kpi12()
    # controle_qualite_kpi16()
    current_date += timedelta(days=1)
