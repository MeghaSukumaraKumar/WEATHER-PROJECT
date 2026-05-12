import json
import boto3
import requests
from datetime import datetime
from decimal import Decimal
import os

#creates a dynamodb service object
dynamoDb = boto3.resource('dynamodb')  
myTable = dynamoDb.Table('weather-api-table')

#function to fetcg data from the api
def get_weather_data(city):
    api_url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "q": city,
        #to store in the lambda environment
        "key": os.environ["WEATHER_API_KEY"]
    }

    #calling the weather api
    response = requests.get(api_url, params=params)
    #checking the API status 
    if response.status_code != 200:  
        return None
    return response.json()

def lambda_handler(event, context):
    
    cities = ["Bangalore","Delhi","Mumbai","Chennai","Kashmir","Dehradun","Kochi","Kerala","Hyderabad","Sikkim"]
    
    for city in cities:
          #to fetch weather data
        data = get_weather_data(city)

        if not data:
            print(f"Failed for {city}")
            continue
        
        #extracting the info
        temp = data['current']['temp_c']
        wind_speed = data['current']['wind_mph']
        wind_dir = data['current']['wind_dir']
        pressure_mb = data['current']['pressure_mb']
        humidity = data['current']['humidity']

        current_timestamp = datetime.utcnow().isoformat()

        item = {
            'city': city,
            'time': current_timestamp,
            'temp': Decimal(str(temp)),
            'wind_speed': Decimal(str(wind_speed)),
            'wind_dir': wind_dir,
            'pressure_mb': Decimal(str(pressure_mb)),
            'humidity': Decimal(str(humidity))
        }
        #step to insert the data into dynamodb table
        myTable.put_item(Item=item) 

    return {
        'statusCode': 200,
        'body': json.dumps('Weather data stored successfully')
    }
