import requests
import lxml.html as html
import pandas as pd

newspaper = []
titles = []
bodies = []
dates = []
categories = []


HOME_LINK = 'https://eldeber.com.bo'
XPATH_LINK_TO_ARTICLE = '//a[@class = "nota-link"]/@href'
XPATH_TITLE = '//div[@class = "text"]/h1/text()'
XPATH_BODY = '//div[@class = "text-editor"]//p/text()'
XPATH_DATE = '//div[@class = "bottom"]/h6/span/text()'
XPATH_TAG1 = '(//div[@class = "top"])[1]/h4/text()'

def add_to_data(title, body, date, category):
    if len(body)>0:
        newspaper.append('El Deber')
        titles.append(title.strip())
        dates.append(date)
        # Category clean
        if category == 'PAÍS ' or category=='Tarija' or category=='Santa Cruz' or category=='USTED ELIGE':
            category = 'nacional'
        elif category == 'Rfi' or category=='Mundo' or category=='BBC' or category=='Dw':
            category = 'mundial'
        elif category == 'Dinero':
            category = 'economia'
        elif category == 'Multideportivo' or category=='Vehiculos' or category == 'Always Ready' or category == 'The Strongest' or category=='Futbol':
            category = 'deportes'
        elif category == 'Coronavirus':
            category = 'sociedad'
        categories.append(category)
        # Body clean
        body_new = ""
        for p in body:
            body_new = body_new + p.strip() + " "
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
    df.to_csv('eldeber.csv', index=False)


def parse_notice(link):
    try:
        response = requests.get(HOME_LINK + link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                body = parsed.xpath(XPATH_BODY)
                date = parsed.xpath(XPATH_DATE)[0].split()[0].replace("/","-")
                tag1 = parsed.xpath(XPATH_TAG1)[0]
                return (title,body,date,tag1)
            except IndexError:
                return (0,0,0,0)
        else:
            raise ValueError(f'Error: {response.status_code} in {link}')
    except ValueError as ve:
        print(ve)
        return (0,0,0,0)

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
                title, body, date, category = parse_notice(link)
                if title != 0 and body != 0:
                    add_to_data(title, body, date, category)
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