import requests
import lxml.html as html
import pandas as pd

newspaper = []
titles = []
bodies = []
dates = []
categories = []


HOME_LINK = 'http://www.laprensa.com.bo'
XPATH_LINK_TO_ARTICLE = '//div[@class = "post-title"]/a/@href'
XPATH_TITLE = '//h1/span/text()'
XPATH_BODY = '//p[@class = "rtejustify" or @class= "rtejustify rteindent1"]/text()'


def add_to_data(title, body, date, category):
    if len(body)>0:
        newspaper.append('La Prensa')
        titles.append(title)
        dates.append(date[6]+date[7]+'-'+date[4]+date[5]+'-'+date[0:4])
        # Category clean
        if category == 'futbol' or category == 'futbol-int' or category == 'tennis':
            category = 'deportes'
        elif category == 'viral' or category == 'interesante' or category == 'bienestar':
            category = 'entretenimiento'
        elif category == 'ciencia' or category == 'tecnologia':
            category = 'cultura'
        elif category == 'salud' or category == 'medio-ambiente':
            category = 'sociedad'
        elif category == 'mundo':
            category = 'mundial'
        categories.append(category)
        # Body clean
        body_new = ""
        for p in body:
            p = p.replace('\n','')
            p = p.replace('\t','')
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
    df.to_csv('laprensa.csv', index=False)


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
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            print("Encontramos {} noticias".format(len(links_to_notices)))
            ide = 1
            for link in links_to_notices:
                print(ide)
                url_content = link.split('/')
                category = url_content[1]
                date = url_content[2]
                if category != 'index.php':
                    title, body = parse_notice(link)
                    if title != 0 and body != 0:
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