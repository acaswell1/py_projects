""" 
The following module contains the methods which will fetch the
data needed to aquire the different type of content to be 
included in the newsletter.

Methods: get_random_quote() -> (str, str),
get_weather_forecast(zip_code, country_code) -> {city, country, periods},
get_current_x_trends(woeid) -> void,
def get_wikipedia_article() -> {Title, Summary, Link, Thumbnail}
"""
from random import randint, choice
from string import punctuation
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup
import tweepy


def get_random_quote():
    """
    This method scrapes a random inspirational quote from www.goodreads.com to
    include in the newsletter
    """
    page_number = randint(1, 100)

    response = requests.get(
        f'https://www.goodreads.com/quotes/tag/inspirational?page={page_number}', timeout=60)

    soup = BeautifulSoup(response.text, features="html.parser")
    quotes = soup.find_all('div', class_='quoteText')
    quote_dictionary = {}

    for raw_quote in quotes:
        quote_body = ""
        for char in raw_quote.text:
            if (char.isalnum() or char in punctuation or char in " "):
                quote_body += char
        split_quote_and_author = quote_body.split("            ")
        quote_dictionary[split_quote_and_author[1].strip(
        )] = split_quote_and_author[0].strip()

    list_quotes = list(quote_dictionary.items())
    author, quote = choice(list_quotes)
    return quote, author


def get_weather_forecast(zip_code=85701, country_code="US"):
    """ 
    Get today's weather forecast using OpenWeatherAPI
    """

    key_reader = open("src/OpWthr_Key.txt", 'r', encoding='utf-8')
    key = key_reader.read().strip()

    try:
        params = f'zip?zip={zip_code},{country_code}&appid={key}'

        response = requests.get(
            f'http://api.openweathermap.org/geo/1.0/{params}', timeout=10)

        location_data = json.loads(response.text)
        lat = location_data['lat']
        lon = location_data['lon']

        params = f'forecast?lat={lat}&lon={lon}&units=imperial&appid={key}'

        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/{params}', timeout=10)

        weather_data = json.loads(response.text)

        forecast = {'city': weather_data['city']['name'],
                    'country': weather_data['city']['country'],
                    'periods': list()}

        for period in weather_data['list'][0:9]:
            forecast['periods'].append({'timestamp': datetime.fromtimestamp(period['dt']),
                                        'temperature': round(period['main']['temp']),
                                        'description': period['weather'][0]['description'].title(),
                                        })

        return forecast

    except KeyError as error:
        print(error)

    except ConnectionError as error:
        print(error)


def get_current_x_trends(woeid=23424977):
    """
    Retrieve the top tending articles from the X api
    """
    key_reader = open("src/Twitter_Key.txt", 'r', encoding='utf-8')
    key = key_reader.read().strip()

    secret_reader = open("src/Twitter_Key_Secret.txt", 'r', encoding='utf-8')
    secret = secret_reader.read().strip()

    try:
        _ = tweepy.AppAuthHandler(key, secret)
        # Elon made the twitter API cost $100 a month so I'm not paying that
        # return tweepy.API(auth=authentication).get_place_trends(woeid)[0]['trends']
    except TypeError as _:
        print(woeid)


def get_wikipedia_article():
    """
    Get a random article from Wikipedia
    """
    url = 'https://en.wikipedia.org/api/rest_v1/page/random/summary'

    try:
        response = requests.get(url, timeout=20)
        article_json = json.loads(response.text)

        article = {'Title': article_json["title"],
                   'Summary': article_json["extract"],
                   'Link': article_json["content_urls"]["desktop"]["page"],
                   'Thumbnail': article_json["thumbnail"]["source"]}
        return article
    except ConnectionError as error:
        print(error)


def test_get_random_quote():
    """
    Ensure that get_random_quote() gives a properly formatted quote
    """
    quote = get_random_quote()
    if quote:
        body, author = quote
        print(f'{body} -{author}')


def test_get_weather_forecast():
    """
    Test the get_weather_forecast function by calling and printing
    """
    forecast = get_weather_forecast()
    if forecast:
        print(
            f'\n Weather forecast for {forecast["city"]}, {forecast["country"]} is....')
        for period in forecast['periods']:
            print(
                f' - {period["timestamp"]} | {period["temperature"]} | {period["description"]}')

    forecast = get_weather_forecast(zip_code=43221)
    if forecast:
        print(
            f'\n Weather forecast for {forecast["city"]}, {forecast["country"]} is....')
        for period in forecast['periods']:
            print(
                f' - {period["timestamp"]} | {period["temperature"]} | {period["description"]}')

    forecast = get_weather_forecast(zip_code=21218)
    if forecast:
        print(
            f'\n Weather forecast for {forecast["city"]}, {forecast["country"]} is....')
        for period in forecast['periods']:
            print(
                f' - {period["timestamp"]} | {period["temperature"]} | {period["description"]}')

    forecast = get_weather_forecast(zip_code=-1)
    if forecast:
        print(
            f'\n Weather forecast for {forecast["city"]}, {forecast["country"]} is....')
        for period in forecast['periods']:
            print(
                f' - {period["timestamp"]} | {period["temperature"]} | {period["description"]}')


def test_get_wikipedia_article():
    """
    Test to see if a random article is given
    """
    article = get_wikipedia_article()
    if article:
        print(f'{article["Title"]}\n<{article["Link"]}>\n{article["Summary"]}')


if __name__ == '__main__':
    print('#####################################################################')

    print('Quote Test')
    test_get_random_quote()

    print('#####################################################################')

    print('Forecast Test')
    test_get_weather_forecast()

    print('#####################################################################')

    print('Wikipedia Article Test')
    test_get_wikipedia_article()

    print('#####################################################################')
