"""Only for using the messenger bot"""
from flask import Flask, request, Response
import requests, json, random, os
app = Flask(__name__)
import os
import openai
import path
import sys
folder = path.Path(__file__).abspath()
sys.path.append(folder.parent)

from news import get_news
from astros import get_num_astronauts, list_astronauts
from schema import functions
from wolfram import call
from weather import get_weather

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
    # DO SOMETHING with the user_message ... ¯\_(ツ)_/¯
    prompt = [
        {
            "role": "system",
            "content": "You are a personal assistant. Use functions when necessary."
        },
        {
            "role": "users",
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')