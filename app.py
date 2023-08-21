"""Only for using the messenger bot"""
from flask import Flask, request, Response
import requests, json, random, os
import openai
import wolframalpha

app = Flask(__name__)

functions = [{
  "name": "get_news",
  "description": "Use this function to get the latest news.",
  "parameters": {
    "type": "object",
    "properties": {
      "N-Results": {
        "type": "string",
        "description": "The number of results. Try to get at least 5."
      }
    },
    "required": ["N-Results"],
  },
}, {
  "name": "get_num_astronauts",
  "description": "Use this function to get the number of astronauts in space.",
  "parameters": {
    "type": "object",
    "properties": {},
    "required": [],
  },
}, {
  "name": "list_astronauts",
  "description":
  "Use this function to get a table of who is in space and what craft they are on.",
  "parameters": {
    "type": "object",
    "properties": {},
    "required": [],
  },
}, {
  "name": "generate_image",
  "description":
  "Use this function to generate an image from a prompt using OpenAI DALL-E. Please note that it returns a URL linking to the image and the URL must be copied verbatim in order for the link to work.",
  "parameters": {
    "type": "object",
    "properties": {
      "prompt": {
        "type": "string",
        "description": "A description of the image to be generated."
      }
    },
    "required": ["prompt"],
  },
  }, {
  "name": "wolfram_alpha",
  "description":
  "This function accesses Wolfram Alpha. Use it when doing any sort of mathematical operation or if you need up to date info.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "The query to send to wolfram alpha."
      }
    },
    "required": ["query"],
  },
}, {
  "name": "weather",
  "description":
  "Get a description of the weather in any city in the world.",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "The city you want information about."
      }
    },
    "required": ["city"],
  },
}]

def get_num_astronauts():
  #Get the data
  response = requests.get("http://api.open-notify.org/astros.json")
  #Convert it to JSON
  data = response.json()
  #Extract the number and return it
  return str(data["number"])


def list_astronauts():
  #Get the data
  response = requests.get("http://api.open-notify.org/astros.json")
  #Convert it to JSON
  data = response.json()
  #Extract the number and return it
  astros = "| Name | Craft |"
  for i in data.get("people"):
    astros += "\n| " + i.get("name") + " | " + i.get("craft") + " |"
  return astros

news_key = os.environ['NEWSAPIKEY']

def get_news(n):
  url = 'https://newsapi.org/v2/top-headlines?country=us&sortBy=popularity&apiKey=' + news_key
  response = requests.get(url)
  articles = response.json()["articles"]
  news = "|summary|link|"

  for i in range(n):
    news += "\n|" + str(articles[i]["description"]) + "|" + str(articles[i]["url"]) + "|"
  return news

# Enter your API key here
weather_key = os.environ["WEATHER"]
 
# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather(city):
    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + weather_key + "&q=" + city

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

app_id = os.environ["WOLFRAM"]

client = wolframalpha.Client(app_id)

def call(query):
    return next(client.query(query).results).text


openai_key = os.environ['OPENAI_KEY']

openai.api_key = openai_key


def generate_image(prompt):
  """"Generate an image from a prompt"""
  img_url = openai.Image.create(
    prompt=prompt,
    n=1,
    size="256x256",
    response_format="url",
  ).get("data")[0].get("url")
  print(img_url)
  return img_url


def execute_function_call(message):
  #print(message["function_call"]["name"])
  if message.get("function_call").get("name") == "get_news":
    query = int(eval(message["function_call"]["arguments"])["N-Results"])
    #print(query)
    results = get_news(query)
    #print("Used func")
  elif message.get("function_call").get("name") == "get_num_astronauts":
    results = get_num_astronauts()
  elif message.get("function_call").get("name") == "list_astronauts":
    results = list_astronauts()
  elif message.get("function_call").get("name") == "generate_image":
    prompt = eval(message["function_call"]["arguments"])["prompt"]
    results = generate_image(prompt)
  elif message.get("function_call").get("name") == "wolfram_alpha":
    query = eval(message["function_call"]["arguments"])["query"]
    results = call(query)
  elif message.get("function_call").get("name") == "weather":
    city = eval(message["function_call"]["arguments"])["city"]
    results = get_weather(city)
  else:
    results = f"Error: function {message['function_call']['name']} does not exist"
  
  return results



def responseGenerator(msgs):
  response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                          messages=msgs,
                                          functions=functions)
  msg = response.choices[0].message.content
  msg_outer = response.choices[0].message
  msgs.append(response["choices"][0]["message"])
  if msg_outer.get("function_call"):
    results = execute_function_call(msg_outer)
    msgs.append({
      "role": "function",
      "name": msg_outer.get("function_call").get("name"),
      "content": results
    })
    #print(messages)
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613", messages=msgs,
    functions=functions).choices[0].message.content
  msgs.append({"role": "assistant", "content": response})
  return response
# env_variables
# token to verify that this bot is legit
verify_token = os.getenv('VERIFY_TOKEN')
# token to send messages through facebook messenger
access_token = os.getenv('ACCESS_TOKEN')

@app.route('/webhook', methods=['GET'])
def webhook_verify():
    if request.args.get('hub.verify_token') == verify_token:
        return request.args.get('hub.challenge')
    return "Wrong verify token"

@app.route('/webhook', methods=['POST'])
def webhook_action():
    data = json.loads(request.data.decode('utf-8'))
    for entry in data['entry']:
        user_message = entry['messaging'][0]['message']['text']
        user_id = entry['messaging'][0]['sender']['id']
        response = {
            'recipient': {'id': user_id},
            'message': {}
        }
        response['message']['text'] = handle_message(user_id, user_message)
        r = requests.post(
            'https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=response)
    return Response(response="EVENT RECEIVED",status=200)

@app.route('/webhook_dev', methods=['POST'])
def webhook_dev():
    # custom route for local development
    data = json.loads(request.data.decode('utf-8'))
    user_message = data['entry'][0]['messaging'][0]['message']['text']
    user_id = data['entry'][0]['messaging'][0]['sender']['id']
    response = {
        'recipient': {'id': user_id},
        'message': {'text': handle_message(user_id, user_message)}
    }
    return Response(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )

def handle_message(user_id, user_message):
    prompt = [
        {
            "role": "system",
            "content": "You are a personal assistant. Use functions when necessary."
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
    res = responseGenerator(prompt)
    return res

@app.route('/privacy', methods=['GET'])
def privacy():
    # needed route if you need to make your bot public
    return "This facebook messenger bot's only purpose is to [...]. That's all. We don't use it in any other way."

@app.route('/', methods=['GET'])
def index():
    return "Hello there, I'm a facebook messenger bot."

app.run(debug=True, host='0.0.0.0')
