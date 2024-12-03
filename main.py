from datetime import datetime, timedelta
import boto3

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

# Configure logging


# AWS region
region = 'XXX'
ec2_instance_id = 'XXX'  # Replace with your EC2 instance ID
rds_instance_id = 'XXX'  # Replace with your RDS instance ID

ec2 = boto3.client('ec2', region_name=region)
rds = boto3.client('rds', region_name=region)
ssm = boto3.client('ssm', region_name=region)

end_date = datetime.now() + timedelta(days=5)  # .date().strftime('%Y-%m-%d')
start_date = datetime.now() - timedelta(days=6)  # .strftime('%Y-%m-%d')
# end_date =   '2024-11-22'
# start_date =  '2024-11-21'
current_date = start_date
while current_date <= end_date:
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

try:
    print(f"Stopping RDS instance: {rds_instance_id}")
    rds.stop_db_instance(DBInstanceIdentifier=rds_instance_id)
    print(f"RDS instance {rds_instance_id} stopped successfully.")
except Exception as e:
    print(f"Failed to stop RDS instance: {e}")
try:
    print(f"Stopping EC2 instance: {ec2_instance_id}")
    ec2.stop_instances(InstanceIds=[ec2_instance_id])
    print(f"EC2 instance {ec2_instance_id} stopped successfully.")
except Exception as e:
    print.error(f"Failed to stop EC2 instance: {e}")

print("Script completed execution.")
