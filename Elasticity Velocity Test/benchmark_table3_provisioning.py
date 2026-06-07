import boto3
import time

# EXPERIMENTAL SETUP:
# This script measures the Elasticity Velocity (Ve) and Time-to-Ready 
# for AWS Fargate (Table 3). Similar scripts are used for GCP/Azure.

def measure_fargate_cold_start():
    client = boto3.client('ecs', region_name='us-east-1')
    cluster_name = 'agile-benchmark-cluster'
    task_def = 'benchmark-task:1'

    print("Triggering AWS Fargate Container Provisioning...")
    start_time = time.time()

    # Request the cloud provider to spin up the container
    response = client.start_task(
        cluster=cluster_name,
        taskDefinition=task_def,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': ['subnet-12345678'],
                'assignPublicIp': 'ENABLED'
            }
        }
    )

    task_arn = response['tasks'][0]['taskArn']
    print(f"Task {task_arn} provisioning. Polling AWS API...")

    # Poll until the container is fully active
    while True:
        task_info = client.describe_tasks(cluster=cluster_name, tasks=[task_arn])
        status = task_info['tasks'][0]['lastStatus']
        
        if status == 'RUNNING':
            break
            
        time.sleep(2) # Cooldown polling

    end_time = time.time()
    provisioning_time = end_time - start_time

    print(f"SUCCESS: Fargate Container Reached RUNNING State.")
    print(f"Total Provisioning Time (Table 3 Data): {provisioning_time:.2f} seconds")

if __name__ == "__main__":
    # Ensure AWS credentials are configured via `aws configure` before running
    measure_fargate_cold_start()