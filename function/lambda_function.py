import boto3
import time

# Initialize AWS clients
region = 'us-east-1'
ec2_instance_id = 'i-0e6c2d0ef1dfbb086'  # Replace with your EC2 instance ID
rds_instance_id = 'lamarcksolutions'     # Replace with your RDS instance ID

ec2 = boto3.client('ec2', region_name=region)
rds = boto3.client('rds', region_name=region)
ssm = boto3.client('ssm', region_name=region)

def wait_for_ssm_command(instance_id, command_id):
    """Wait for the SSM command to complete."""
    while True:
        response = ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        status = response['Status']
        print(f"SSM Command Status: {status}")
        if status in ['Success', 'Failed', 'Cancelled']:
            return status
        time.sleep(30)  # Poll every 30 seconds

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
            "/usr/bin/python3 /home/ec2-user/kpis/main.py >> /home/ec2-user/kpis/logs/logfile_$(date +\%Y\%m\%d_\%H\%M\%S).log 2>&1 "
        ]
        response = ssm.send_command(
            InstanceIds=[ec2_instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={"commands": commands},
        )
        command_id = response["Command"]["CommandId"]
        print(f"Command sent to EC2 via SSM. Command ID: {command_id}")

        # Step 4: Wait for SSM command to complete
        status = wait_for_ssm_command(ec2_instance_id, command_id)
        if status != "Success":
            print(f"SSM Command failed with status: {status}")
            raise Exception("Script execution failed.")

        # Step 5: Stop EC2 instance
        ec2.stop_instances(InstanceIds=[ec2_instance_id], Force=True)
        print(f"EC2 instance {ec2_instance_id} stopped.")

        # Step 6: Stop RDS instance
        rds.stop_db_instance(DBInstanceIdentifier=rds_instance_id)
        print(f"RDS instance {rds_instance_id} stopped.")

    except Exception as e:
        print(f"An error occurred: {e}")
        raise
