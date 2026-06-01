# import boto3
# import uuid
# import csv
# import io

# s3 = boto3.client('s3')

# BUCKET_NAME = 'bucket-weatherapi'


# def lambda_handler(event, context):
#     try:
#         #checking db records exist 
#         if 'Records' not in event:
#             #return the error if invalid
#             return {
#                 'statusCode': 400,
#                 'body': 'Invalid event format'
#             }
#             for record in event['Records']:
#                 if record['eventName'] == 'INSERT':
#                     new_image = record['dynamodb']['NewImage']
#                     item = {k: list(v.values())[0] for k, v in new_image.items()}
#                     csv_buffer = io.StringIO()
#                     writer = csv.writer(csv_buffer)

#                 writer.writerow([
#                     'city',
#                     'time',
#                     'temp',
#                     'wind_speed',
#                     'wind_dir',
#                     'pressure_mb',
#                     'humidity'
#                 ])

#                 writer.writerow([
#                     item.get('city', ''),
#                     item.get('time', ''),
#                     item.get('temp', ''),
#                     item.get('wind_speed', ''),
#                     item.get('wind_dir', ''),
#                     item.get('pressure_mb', ''),
#                     item.get('humidity', '')
#                 ])
#                 #generate csv file name
#                 file_name = f"weather/{uuid.uuid4()}.csv"

#                 # upload csv to s3
#                 s3.put_object(
#                     Bucket=BUCKET_NAME,
#                     Key=file_name,
#                     Body=csv_buffer.getvalue(),
#                     ContentType='text/csv'
#                 )

#             return {
#                         'statusCode': 200,
#                         'body': 'CSV file uploaded successfully'
#         }
#     except Exception as e:

#      return {
#             'statusCode': 500,
#             'body': str(e)
#         }

import json
import boto3
import csv
import io
from datetime import datetime

# AWS Clients
s3 = boto3.client('s3')

# S3 Bucket Name
BUCKET_NAME = 'weatherpro-bucket'

# Folder inside S3 bucket
FOLDER_NAME = 'projectsnow/'


def lambda_handler(event, context):

    # Loop through DynamoDB Stream records
    for record in event.get('Records', []):

        # Process only INSERT events
        if record.get('eventName') == 'INSERT':

            # Extract DynamoDB data
            new_image = record.get('dynamodb', {}).get('NewImage', {})

            city = new_image.get('city', {}).get('S', '')
            time = new_image.get('time', {}).get('S', '')
            temp = new_image.get('temp', {}).get('S', '')
            humidity = new_image.get('humidity', {}).get('S', '')
            wind_speed = new_image.get('wind_speed', {}).get('S', '')
            wind_dir = new_image.get('wind_dir', {}).get('S', '')
            pressure_mb = new_image.get('pressure_mb', {}).get('S', '')

            # Create CSV in memory
            csv_buffer = io.StringIO()

            writer = csv.writer(csv_buffer)

            # CSV Header
            writer.writerow([
                'city',
                'time',
                'temp',
                'humidity',
                'wind_speed',
                'wind_dir',
                'pressure_mb'
            ])

            # CSV Data Row
            writer.writerow([
                city,
                time,
                temp,
                humidity,
                wind_speed,
                wind_dir,
                pressure_mb
            ])

            # File name
            file_name = f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            # Upload CSV to S3 folder
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=f"{FOLDER_NAME}/{file_name}",
                Body=csv_buffer.getvalue()
            )

    return {
        'statusCode': 200,
        'body': json.dumps('CSV uploaded to S3 folder successfully')
    }