import boto3

def list_rds_instances():
    # Create an RDS client # setting your region 
    rds_client = boto3.client('rds', region_name='ap-east-1')

    # Call to get list of RDS instances
    response = rds_client.describe_db_instances()

    # Initialize a list to hold all DB instances
    db_instances = []

    # Loop through the response and add instance identifiers to the list
    for db_instance in response['DBInstances']:
        instance_info = {
            'DBInstanceIdentifier': db_instance['DBInstanceIdentifier'],
            'DBInstanceClass': db_instance['DBInstanceClass'],
            'DBInstanceStatus': db_instance['DBInstanceStatus'],
            'Engine': db_instance['Engine'],
            'EngineVersion': db_instance['EngineVersion']
        }
        db_instances.append(instance_info)

    return db_instances

# Run the function and print the results
if __name__ == "__main__":
    instances = list_rds_instances()
    for instance in instances:
        print(instance)
