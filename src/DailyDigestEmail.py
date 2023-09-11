"""
Class which allow us to buld and send an email with our daily digest information
"""

import datetime
from bs4 import BeautifulSoup
from content import get_random_quote as quote
from content import get_weather_forecast as forecast
from content import get_wikipedia_article as article


class DailyDigestEmail:
    """ Test """

    def __init__(self):
        self.email_content = {'quote': quote(),
                              'forecast': forecast(),
                              'article': article()}
        self.email = None

    def send_email(self):
        """ Test """
        if (email := self.email):
            print(email['plain'])
            print(email['html'])
        else:
            print("Formatted email does not exist")

    def format_message(self):
        """
        Format the email to be sent as a plain text or html message
        """
        ###### PLAIN TEXT ######
        plain_text = f'********* Daily Digest - {datetime.date.today().strftime("%d %b %Y")} ********* \n'
        
        if quote_content := self.email_content['quote']:
            body, author = quote_content
            plain_text += '\n********* Today\'s Quote ********* \n'
            plain_text += f'"{body}" -{author}\n'


        if forecast_content := self.email_content['forecast']:
            plain_text += '\n********* Today\'s Weather ********* \n'
            plain_text += f'\n Weather forecast for {forecast_content["city"]}, {forecast_content["country"]} is....\n'
            weather = ""
            for period in forecast_content['periods']:
                weather += f'- {period["timestamp"]} | {period["temperature"]} | {period["description"]}\n'
            plain_text += weather

        if article_content := self.email_content['article']:
            plain_text += '\n********* Today\'s Article ********* \n'
            plain_text += f'{article_content["Title"]}\n{article_content["Link"]}\
                        \n{article_content["Summary"]}\n'
            
        weather = weather.split('\n')
        
        ###### HTML MESSAGE ######
        html_msg = f"""
        <html>
        <head></head>
        <body>
            <div style="text-align:center;">  
                <h1>Daily Digest - {datetime.date.today().strftime("%d %b %Y")}</h1>
                <h3>Today's Quote</h3>
                <p>"{body}" -{author}</p>
            </div>
            <div id="contentcols"  style="margin:0px auto; width:70%">
                <div id="weathercol" style="float:left; margin:0; width:50%;">
                    <h3>Today's Weather</h3>
                    <p>Weather forecast for {forecast_content["city"]}, {forecast_content["country"]} is....</p>
                    <p>{weather[0]}</p>
                    <p>{weather[1]}</p>
                    <p>{weather[2]}</p>
                    <p>{weather[3]}</p>
                    <p>{weather[4]}</p>
                    <p>{weather[5]}</p>
                    <p>{weather[6]}</p>
                    <p>{weather[7]}</p>
                    <p>{weather[8]}</p>
                </div>
                <div id="articlecol" style="float:left; margin:0; width:50%;">
                    <h3>Today's Article</h3>
                    <img src={article_content["Thumbnail"]} alt="{article_content["Title"]} Thumbnail"></img>
                    <p>{article_content["Title"]}</p>
                    <p>{article_content["Summary"]}</p>
                    <a href={article_content["Link"]}>Read More Here</a>
                </div>
            </div>
        </body>
        </html>
        """
        soup = BeautifulSoup(html_msg, features='html.parser')
        self.email = { 'plain' : plain_text,
                      'html': str(soup.prettify())}


if __name__ == '__main__':
    digest = DailyDigestEmail()
    digest.send_email()
    digest.format_message()
    digest.send_email()
