import wolframalpha
import os

app_id = os.environ["WOLFRAM"]

client = wolframalpha.Client(app_id)

def call(query):
    return next(client.query(query).results).text