""" #Test dependencies
import sys
sys.path.insert(0, '/opt/python/lib/python3.11/site-packages')

required_packages = [   "psycopg2", "sqlalchemy", "certifi", "chardet",
    "greenlet", "idna", "requests", "urllib3"]


def lambda_handler(event,context):
    print("Testing Python Environment and Dependencies\n")
    print("Python Path:", sys.path)


    # Test imports and versions
    for package in required_packages:
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'No version attribute')
            print(f"{package} is installed. Version: {version}")
        except ImportError as e:
            print(f"Error importing {package}: {e}")
        except Exception as e:
            print(f"Unexpected error with {package}: {e}")


"""
import boto3
import time

# Initialize AWS clients
region = 'XXX'
ec2_instance_id = 'XXX'  # Replace with your EC2 instance ID
rds_instance_id = 'XXX'  # Replace with your RDS instance ID

ec2 = boto3.client('ec2', region_name=region)
rds = boto3.client('rds', region_name=region)
ssm = boto3.client('ssm', region_name=region)


def wait_for_ssm_command(instance_id, command_id):
    # Wait for the SSM command to complete.
    while True:
        time.sleep(30)
        response = ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        status = response['Status']
        print(f"SSM Command Status: {status}")
        if status in ['Success', 'Failed', 'Cancelled']:
            return status
        # Poll every 30 seconds
        time.sleep(10)  # Poll every 10 seconds





def lambda_handler(event, context):
    try:
        # Step 1: Start EC2 instance
        ec2.start_instances(InstanceIds=[ec2_instance_id])
        print(f"EC2 instance {ec2_instance_id} started.")

        # Wait for EC2 instance to be running
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[ec2_instance_id])
        print(f"EC2 instance {ec2_instance_id} is now running.")

        # Step 2: Start RDS instance
        rds.start_db_instance(DBInstanceIdentifier=rds_instance_id)
        print(f"RDS instance {rds_instance_id} started.")

        # Wait for RDS instance to be available
        rds_waiter = rds.get_waiter('db_instance_available')
        rds_waiter.wait(DBInstanceIdentifier=rds_instance_id)
        print(f"RDS instance {rds_instance_id} is now available.")

        # Step 3: Execute the Python script via SSM
        commands = [
            "export ENV=production && /usr/local/bin/python3.8 -m pip install --user -r /home/ec2-user/kpis/requirements.txt && /usr/local/bin/python3.8 /home/ec2-user/kpis/main.py >> /home/ec2-user/kpis/logs/logfile_$(date +\\%Y\\%m\\%d_\\%H\\%M\\%S).log 2>&1"
        ]

        response = ssm.send_command(
            InstanceIds=[ec2_instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={"commands": commands},
        )
        command_id = response["Command"]["CommandId"]
        print(f"Command sent to EC2 via SSM. Command ID: {command_id}")

        # Skip waiting for the SSM command to complete
        print("Lambda's role is completed after sending the command.")

    except Exception as e:
        print(f"An error occurred: {e}")
        raise  # Reraise the exception for AWS Lambda to handle
    finally:
        print("Function execution completed.")

