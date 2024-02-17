from newspaper import Article
import requests

url="https://news.google.com/rss/articles/CBMiLGh0dHBzOi8vd3d3LmJiYy5jby51ay9zcG9ydC9jcmlja2V0LzY4MzIyMzI40gEuaHR0cHM6Ly93d3cuYmJjLmNvbS9zcG9ydC9jcmlja2V0LzY4MzIyMzI4LmFtcA?oc=5"

actual_url=requests.get(url).url

article=Article(actual_url)
article.download()
article.parse()

print(article.text)