"""
Class which allow us to buld and send an email with our daily digest information
"""

import datetime
from email.message import EmailMessage
from smtplib import SMTP
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
        self.recipients = ['aleccaswell@gmail.com']
        self.sender_cerdentials = { 'email':'aleccaswell@outlook.com',
                                   'password': open("src/Email_pwd.txt", 'r', encoding='utf-8').read().strip()}

    def send_email(self):
        """ 
        Send the email
        """
        message = EmailMessage()
        message['Subject'] = f'Alec\'s Daily Digest - {datetime.date.today().strftime("%d %b %Y")}'
        message['From'] = self.sender_cerdentials['email']
        message['To'] = 'aleccaswell@gmail.com'
        
        self.format_message()
        message.set_content(self.email['plain'])
        message.add_alternative(self.email['html'], subtype='html')

        with SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(self.sender_cerdentials['email'],
                            self.sender_cerdentials['password'])
            server.send_message(message)

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
        <body style="background-color:lightblue;">
            <div style="text-align:center;">  
                <h1>Daily Digest - {datetime.date.today().strftime("%d %b %Y")}</h1>
                <h3>Today's Quote</h3>
                <p><i>"{body}"</i> -{author}</p>
            </div>
            <div id="contentcols"  style="margin:0px auto; width:70%">
                <div id="weathercol" style="float:left; margin:0; width:50%;">
                    <h3>Today's Weather</h3>
                    <p>Weather forecast for {forecast_content["city"]}, {forecast_content["country"]} is....</p>
                    <p>{weather[0][1:]}</p>
                    <p>{weather[1][1:]}</p>
                    <p>{weather[2][1:]}</p>
                    <p>{weather[3][1:]}</p>
                    <p>{weather[4][1:]}</p>
                    <p>{weather[5][1:]}</p>
                    <p>{weather[6][1:]}</p>
                    <p>{weather[7][1:]}</p>
                    <p>{weather[8][1:]}</p>
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
