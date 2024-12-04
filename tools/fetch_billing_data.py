import boto3
import psycopg2
from datetime import datetime, timedelta

db_params = {
    'dbname': 'x',  # Remplacez "postgresql" par "lamarckinitial"
    'user': 'x',
    'password': 'x',
    'host': 'x',
    'port': 'x'
}
def get_data():
    # Initialize AWS Cost Explorer client
    client = boto3.client('ce')

    # Define the time range for the query
    start_date = (datetime.now() - timedelta(days=34)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    # Fetch cost and usage data
    response = client.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='DAILY',
        Metrics=['UnblendedCost'],
        GroupBy=[
            {'Type': 'DIMENSION', 'Key': 'SERVICE'}
        ]
    )
    return response


# Insert data into PostgreSQL
def insert_data_to_db(date, service, cost):
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        query = """
            INSERT INTO aws_billing (usage_date, service_name, cost)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (date, service, cost))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Inserted data for {service} on {date}: ${cost}")
    except Exception as e:
        print(f"Error inserting data: {e}")

