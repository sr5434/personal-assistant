import requests
import os

news_key = os.environ['NEWSAPIKEY']

def get_news(n):
  url = 'https://newsapi.org/v2/top-headlines?country=us&sortBy=popularity&apiKey=' + news_key
  response = requests.get(url)
  articles = response.json()["articles"]
  news = "|summary|link|"

  for i in range(n):
    news += "\n|" + str(articles[i]["description"]) + "|" + str(articles[i]["url"]) + "|"
  return news