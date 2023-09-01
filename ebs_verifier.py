import boto3
import json
import os
from datetime import datetime
import sys


def write_json(file_name, data):
    with open('/tmp/' + file_name,  mode='w') as json_file:
        json.dump(data, json_file, indent=4)

def lambda_handler(event, context):
    ACCOUNT_ID = context.invoked_function_arn.split(":")[4]
    ec2_client = boto3.client('ec2')
    s3_client = boto3.client('s3')
    volumes_unattached = ec2_client.describe_volumes(Filters=[{
            'Name': 'status',
            'Values': ['available'],
        }])
    volumes_unencrypted = ec2_client.describe_volumes(Filters=[{
         'Name': 'encrypted',
         'Values': ['False'],
     }
    ])
    snapshots_dic = ec2_client.describe_snapshots(Filters=[{
            'Name': 'owner-id',
            'Values': [ACCOUNT_ID],
        }])
    

    volumes=volumes_unattached['Volumes']+volumes_unattached['Volumes']

    total_unattached_size = 0
    total_unencrypted_size = 0
    total_snapshots_size = 0

    print('calculating unattached and unecrypted discs')
    
    for volume in volumes:

        data = {
            'VolumeId': volume['VolumeId'],
            'Size': volume['Size'],
            "VolumeType": volume['VolumeType'],
            'Encrypted': volume['Encrypted'],
            'AvailabilityZone': volume['AvailabilityZone'],
            'CreateTime': volume['CreateTime'].isoformat()
        }
        
        unattached = []
        unecrypted = []
        snapshots = []
        
        if volume['State']== "available":
            unattached.append(data)
            total_unattached_size=total_unattached_size+volume['Size']
        if volume['Encrypted'] == False:
            unecrypted.append(data)
            total_unencrypted_size=total_unencrypted_size+volume['Size']
            
        write_json('unattached_ebs.json', unattached)
        write_json('unecrypted_ebs.json', unecrypted)
            
    print('calculating encrypted snapshots')

    for snapshot in snapshots_dic['Snapshots']:
        if snapshot['Encrypted'] == False:

            snapshots.append({
                'SnapshotId': snapshot['SnapshotId'],
                'VolumeSize': snapshot['VolumeSize'],
                'OwnerId': snapshot['OwnerId'],
                'State':  snapshot['State'],
                'VolumeId': snapshot['VolumeId'],
                'StorageTier': snapshot['StorageTier']
            })

            total_snapshots_size=total_snapshots_size+volume['Size'] 
        
    write_json('snapshots.json', snapshots)
        
    write_json('summary.json', [{
        'Total unattached ebs size': total_unattached_size,
        'Total unencryptd ebs size:': total_unencrypted_size,
        'Total snapshots size': total_snapshots_size
        
    }])
    
    print('uploading files to s3')
    
    for i in ['unattached_ebs.json', 'unecrypted_ebs.json', 'snapshots.json', 'summary.json']:
        try:
            s3_client.upload_file('/tmp/'+ i, os.environ["BUCKET_NAME"] , i + '_' + datetime.now().date().strftime("%Y-%m-%d"))
            print(f'file {i} uploaded successfully')
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            sys.exit(1)

    print('function run successfully')
