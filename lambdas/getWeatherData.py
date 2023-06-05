import json
import pymysql
import requests

# Configuration for RDS connection
rds_host = "mysql-ssa-1.c3uztxubh3hp.us-east-2.rds.amazonaws.com"
db_username = "photoapp-read-write"
db_password = "def456!!"
db_name = "weatherapp"

def compute_weather_data(data):
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    cloudiness = data['clouds']['all']
    
    # Perform complex computation based on weather data
    heat_index = compute_heat_index(temperature, humidity)
    wind_chill = compute_wind_chill(temperature, wind_speed)
    visibility = compute_visibility(cloudiness)
    
    # Perform some computation based on the weather data
    temperature_celsius = temperature - 273.15
    temperature_fahrenheit = (temperature_celsius * 9/5) + 32
    
    # Create the computed weather data payload
    computed_data = {
        'heat_index': round(heat_index, 2),
        'wind_chill': round(wind_chill, 2),
        'visibility': visibility,
        'temperature_celsius': temperature_celsius,
        'temperature_fahrenheit': temperature_fahrenheit,
        'humidity': humidity
    }
    
    return computed_data

def compute_heat_index(temperature, humidity):
    # Perform heat index calculation
    # Replace this with your own heat index computation logic
    heat_index = temperature + humidity
    
    return heat_index

def compute_wind_chill(temperature, wind_speed):
    # Perform wind chill calculation
    # Replace this with your own wind chill computation logic
    wind_chill = temperature - wind_speed
    
    return wind_chill

def compute_visibility(cloudiness):
    # Perform visibility computation
    # Replace this with your own visibility computation logic
    if cloudiness < 30:
        visibility = 'High'
    elif cloudiness < 70:
        visibility = 'Medium'
    else:
        visibility = 'Low'
    
    return visibility

def lambda_handler(event, context):
    # Retrieve the location from the event payload
    location = event['location']
    username = event['username']
    
    # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    api_key = '467f68b6a5c985be90102bca610238c5'
    
    # Make a request to the OpenWeatherMap API
    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    # print(data)
    # Compute additional weather data
    computed_data = compute_weather_data(data)
                                 
    connection = pymysql.connect(host=rds_host,
                                 user=db_username,
                                 password=db_password,
                                 database=db_name)
    
    try:
        with connection.cursor() as cursor:
            # Check if the location exists in the table
            insert_query = "INSERT INTO locations (username, location) VALUES (%s, %s)"
            cursor.execute(insert_query, (username, location))
            connection.commit()
            # If no unique values found, return a message
            # return "No unique values found in the table"
    
    except Exception as e:
        print("Error:", str(e))
        return "Error occurred"
    
    five_locations = []
    
    try:
        with connection.cursor() as cursor:
            # Check if the location exists in the table
            query = "SELECT DISTINCT location FROM locations where username = %s LIMIT 5"
            cursor.execute(query, (username,))
    
            result = cursor.fetchall()
            if result:
                five_locations = [row[0] for row in result]  # Return a list of usernames
        
            # If no unique values found, return a message
            # return "No unique values found in the table"
    
    except Exception as e:
        print("Error:", str(e))
        return "Error occurred"
    
    finally:
        connection.close()
        
    # Create the weather response payload
    response = {
        'location': location,
        'data': computed_data,
        'locations': five_locations
    }
    
    # Return the weather response
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }