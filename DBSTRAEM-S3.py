import boto3
import uuid
import csv
import io

s3 = boto3.client('s3')

BUCKET_NAME = 'bucket-weatherapi'


def lambda_handler(event, context):
    try:
        #checking db records exist 
        if 'Records' not in event:
            #return the error if invalid
            return {
                'statusCode': 400,
                'body': 'Invalid event format'
            }
            for record in event['Records']:
                if record['eventName'] == 'INSERT':
                    new_image = record['dynamodb']['NewImage']
                    item = {k: list(v.values())[0] for k, v in new_image.items()}
                    csv_buffer = io.StringIO()
                    writer = csv.writer(csv_buffer)

                writer.writerow([
                    'city',
                    'time',
                    'temp',
                    'wind_speed',
                    'wind_dir',
                    'pressure_mb',
                    'humidity'
                ])

                writer.writerow([
                    item.get('city', ''),
                    item.get('time', ''),
                    item.get('temp', ''),
                    item.get('wind_speed', ''),
                    item.get('wind_dir', ''),
                    item.get('pressure_mb', ''),
                    item.get('humidity', '')
                ])
                #generate csv file name
                file_name = f"weather/{uuid.uuid4()}.csv"

                # upload csv to s3
                s3.put_object(
                    Bucket=BUCKET_NAME,
                    Key=file_name,
                    Body=csv_buffer.getvalue(),
                    ContentType='text/csv'
                )

            return {
                        'statusCode': 200,
                        'body': 'CSV file uploaded successfully'
        }
    except Exception as e:

     return {
            'statusCode': 500,
            'body': str(e)
        }