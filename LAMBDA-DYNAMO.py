import json
import requests
import boto3
from datetime import datetime

# DynamoDB Connection
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('weatherapi_table')
API_KEY = "ee585e200edb4feda8964503262705"

def get_weather_data(city):
    api_url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(api_url)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()


def lambda_handler(event, context):

    cities = ["Kochi","Bangalore","Delhi","Mumbai","Chennai","Kashmir","Dehradun","Hyderabad"]   
    for city in cities:
        data = get_weather_data(city)

        temp = data['current']['temp_c']
        wind_speed = data['current']['wind_mph']
        wind_dir = data['current']['wind_dir']
        pressure_mb = data['current']['pressure_mb']
        humidity = data['current']['humidity']

        table.put_item(
            Item={
                'city': city,
                'time': datetime.now().isoformat(),
                'temp': str(temp),
                'humidity': str(humidity),
                'wind_speed': str(wind_speed),
                'wind_dir': wind_dir,
                'pressure_mb': str(pressure_mb)
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Weather data saved to DynamoDB')
    }