import requests

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