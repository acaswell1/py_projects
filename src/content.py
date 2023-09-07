""" 
The following module contains the methods which will fetch the
data needed to aquire the different type of content to be 
included in the newsletter.

Methods: get_random_quote() -> str, 

"""
import random
from string import punctuation
import requests
from bs4 import BeautifulSoup


def get_random_quote():
    """
    This method scrapes a random inspirational quote from www.goodreads.com to
    include in the newsletter
    """
    response = requests.get(
        'https://www.goodreads.com/quotes/tag/inspirational', timeout=30)

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

    author, quote = random.choice(list(quote_dictionary.items()))
    return quote, author

if __name__ == '__main__':
    get_random_quote()