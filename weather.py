# import required modules
import requests, json, os
 
# Enter your API key here
api_key = os.environ["WEATHER"]
 
# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather(city):
    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city

    # get method of requests module
    # return response object
    response = requests.get(complete_url)
    
    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()
 
    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":
        # store the value of "weather"
        # key in variable z
        z = x["weather"]
 
        # store the value corresponding
        # to the "description" key at
        # the 0th index of z
        weather_description = z[0]["description"]
 
        # return following values
        return weather_description

    else:
       return "City Not Found"