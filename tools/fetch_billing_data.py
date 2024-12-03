import boto3
import psycopg2
from datetime import datetime, timedelta

# Initialize AWS Cost Explorer client
client = boto3.client('ce')

# Define the time range for the query
start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
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
"db_conn_str": "postgresql://kpis:lamarck123@lamarcksolutions.cpaeaqu0asup.us-east-1.rds.amazonaws.com:5432/lamarckinitial",

# PostgreSQL database connection details
db_params = {
    'dbname': 'your_database',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'lamarck123@lamarcksolutions.cpaeaqu0asup.us-east-1.rds.amazonaws.com',
    'port': '5432'
}

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

# Process and store data
for result in response['ResultsByTime']:
    date = result['TimePeriod']['Start']
    for group in result['Groups']:
        service = group['Keys'][0]
        cost = float(group['Metrics']['UnblendedCost']['Amount'])
        insert_data_to_db(date, service, cost)
