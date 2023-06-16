import os
import openai
from news import get_news
from astros import get_num_astronauts, list_astronauts
from schema import functions

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
  else:
    results = f"Error: function {message['function_call']['name']} does not exist"
  #print(results)
  return results


messages = [
  {
    "role": "system",
    "content": "You are a personal assistant. Use functions when necessary."
  },
]
while True:
  q = input("User:")
  messages.append({"role": "user", "content": q})
  response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613",
                                          messages=messages,
                                          functions=functions)
  msg = response.choices[0].message.content
  msg_outer = response.choices[0].message
  messages.append(response["choices"][0]["message"])
  if msg_outer.get("function_call"):
    results = execute_function_call(msg_outer)
    messages.append({
      "role": "function",
      "name": msg_outer.get("function_call").get("name"),
      "content": results
    })
    #print(messages)
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613", messages=messages,
    functions=functions).choices[0].message.content
  messages.append({"role": "assistant", "content": response})
  print("Assistant: ", response)
