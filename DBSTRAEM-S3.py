import json
import boto3
import csv
import io
from datetime import datetime

# AWS client
s3 = boto3.client('s3')
BUCKET_NAME = 'weatherpro-bucket'
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

        
            csv_buffer = io.StringIO()

            writer = csv.writer(csv_buffer)

            # writing csv header
            writer.writerow([
                'city',
                'time',
                'temp',
                'humidity',
                'wind_speed',
                'wind_dir',
                'pressure_mb'
            ])

            writer.writerow([
                city,
                time,
                temp,
                humidity,
                wind_speed,
                wind_dir,
                pressure_mb
            ])

            file_name = f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            # step to load data to s3
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=f"{FOLDER_NAME}/{file_name}",
                Body=csv_buffer.getvalue()
            )

    return {
        'statusCode': 200,
        'body': json.dumps('CSV uploaded to S3 folder successfully')
    }