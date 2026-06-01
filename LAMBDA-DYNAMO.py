# import json
# import boto3
# import requests
# from datetime import datetime
# from decimal import Decimal
# import os

# #creates a dynamodb service object
# dynamoDb = boto3.resource('dynamodb')  
# myTable = dynamoDb.Table('weather-api-table')

# #function to fetcg data from the api
# def get_weather_data(city):
#     api_url = "http://api.weatherapi.com/v1/current.json"
#     params = {
#         "q": city,
#         #to store in the lambda environment
#         "key": os.environ["WEATHER_API_KEY"]
#     }

#     #calling the weather api
#     response = requests.get(api_url, params=params)
#     #checking the API status 
#     if response.status_code != 200:  
#         return None
#     return response.json()

# def lambda_handler(event, context):
    
#     cities = ["Bangalore","Delhi","Mumbai","Chennai","Kashmir","Dehradun","Kochi","Kerala","Hyderabad","Sikkim"]
    
#     for city in cities:
#           #to fetch weather data
#         data = get_weather_data(city)

#         if not data:
#             print(f"Failed for {city}")
#             continue
        
#         #extracting the info
#         temp = data['current']['temp_c']
#         wind_speed = data['current']['wind_mph']
#         wind_dir = data['current']['wind_dir']
#         pressure_mb = data['current']['pressure_mb']
#         humidity = data['current']['humidity']

#         current_timestamp = datetime.utcnow().isoformat()

#         item = {
#             'city': city,
#             'time': current_timestamp,
#             'temp': Decimal(str(temp)),
#             'wind_speed': Decimal(str(wind_speed)),
#             'wind_dir': wind_dir,
#             'pressure_mb': Decimal(str(pressure_mb)),
#             'humidity': Decimal(str(humidity))
#         }
#         #step to insert the data into dynamodb table
#         myTable.put_item(Item=item) 

#     return {
#         'statusCode': 200,
#         'body': json.dumps('Weather data stored successfully')
#     }
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

    cities = ["Kollam","Kochi","Bangalore","Delhi","Mumbai","Chennai","Kashmir","Dehradun","Hyderabad"]

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