import os
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_news(api_key, query):
    base_url = 'https://newsapi.org/v2/everything'
    articles = []
    page = 1
    total_articles = 100
    language = 'en'

    while len(articles) < total_articles:

        params = {
            'apiKey': api_key,
            'q': query,
            'language': language,
            'pageSize': min(100, total_articles - len(articles)),
            'page': page
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = json.loads(response.text)
            if data['status'] == 'ok' and data['totalResults'] > 0:
                articles.extend(data['articles'])
                page += 1
            else:
                break
        else:
            print(f"Error: {response.status_code}")
            break

        # To avoid hitting API rate limits
        time.sleep(1)

    return articles[:total_articles]


def main():
    api_key = os.getenv('NEWS_API_KEY')

    # Movies released in Fall 2023
    movies = ['Five Nights at Freddy’s', 'Napoleon',
              'The Hunger Games: Ballad of Songbirds and Snakes', 'The Marvels', 'Priscilla', 'Killers of the Flower Moon']

    # create dict to store all articles and count per movie
    all_articles = {}

    for movie in movies:
        movie_articles = get_news(api_key, movie)
        all_articles[movie] = {
            'count': len(movie_articles),
            'articles': movie_articles
        }

    # Save the articles to a JSON file
    with open('movie_articles.json', 'w', encoding='utf-8') as file:
        json.dump(all_articles, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
