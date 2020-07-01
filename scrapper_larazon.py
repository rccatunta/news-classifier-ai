import requests
import lxml.html as html
import pandas as pd

newspaper = []
titles = []
bodies = []
dates = []
categories = []


HOME_LINK = 'https://www.la-razon.com/'
XPATH_LINK_TO_ARTICLE = '//a[@class = "title  " or @class = "title" or @class= "title  normal"]/@href'
XPATH_TITLE = '//h1[@class = "title"]/text()'
XPATH_BODY = '(//div[@class="article-body"])[1]/p/text()'


def add_to_data(title, body, date, category):
    if len(body)>0:
        newspaper.append('La Razon')
        titles.append(title)
        dates.append(date)
        # Category clean
        if category=='seguridad-ciudadana':
            category = 'seguridad'
        elif category=='voces':
            category = 'opinion'
        elif category=='marcas':
            category = 'deportes'
        elif category=='escape':
            category = 'cultura'
        elif category=='la-revista':
            category = 'entretenimiento'
        elif category=='financiero':
            category = 'economia'
        elif category=='ciudades':
            category = 'sociedad'
        elif category=='mia':
            category = 'entretenimiento'
        elif category=='politico':
            category = 'nacional'
        elif category=='mundo':
            category = 'mundial'
        categories.append(category)
        # Body clean
        body_new = ""
        for p in body:
            body_new = body_new + p + " "
        bodies.append(body_new)
    else:
        return


def convert_to_csv():
    df = pd.DataFrame({
        'periodico': newspaper,
        'titulo': titles,
        'cuerpo': bodies,
        'fecha': dates,
        'categoria': categories
    })
    df.to_csv('larazon.csv', index=False)


def parse_notice(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                body = parsed.xpath(XPATH_BODY)
                return (title,body)                
            except IndexError:
                return (0,0)
        else:
            raise ValueError(f'Error: {response.status_code} in {link}')
    except ValueError as ve:
        print(ve)
        return (0,0)

def parse_home():
    try:
        response = requests.get(HOME_LINK)
        if response.status_code == 200:
            cat = {""}
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            print("Encontramos {} noticias".format(len(links_to_notices)))
            ide = 1
            for link in links_to_notices:
                print(ide)
                url_content = link.split('/')
                if len(url_content) > 6:
                    category = url_content[3]
                    year = url_content[4]
                    month = url_content[5]
                    day = url_content[6]
                    date = day+"-"+month+"-"+year
                    if category != 'extra' and category != 'tendencias' and category !='lr-article':
                        title,body = parse_notice(link)
                        if title != 0 and body != 0:
                            add_to_data(title,body,date,category)
                ide+=1
            convert_to_csv()
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()

if __name__ == '__main__':
    run()