import requests
import lxml.html as html
import pandas as pd

newspaper = []
titles = []
bodies = []
dates = []
categories = []


HOME_LINK = 'https://www.paginasiete.bo'
XPATH_LINK_TO_ARTICLE = '//h2[@class="titulo"]/a/@href'
XPATH_TITLE = '//h1[@class="titular"]/text()'
XPATH_BODY = '//div[@class="cuerpo-nota"]//p[position()>1]/text()'

def add_to_data(title, body, date, category):
    if len(body)>0:
        newspaper.append('Pagina 7')
        titles.append(title)
        dates.append(date)
        # Category clean
        if category=='rascacielos':
            category = 'entretenimiento'
        elif category=='planeta':
            category = 'mundial'
        elif category=='campeones':
            category = 'deportes'
        elif category=='gente':
            category = 'sociedad'
        elif category=='ideas':
            category = 'opinion'
        elif category=='miradas':
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
    df.to_csv('paginasiete.csv', index=False)


def parse_notice(link):
    try:
        response = requests.get(HOME_LINK+link)
        if response.status_code == 200:
            notice = response.content.decode('ISO-8859-1')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','')
                body = parsed.xpath(XPATH_BODY)
                return (title,body)                
            except IndexError:
                return (0,0)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)

def parse_home():
    try:
        response = requests.get(HOME_LINK)
        if response.status_code == 200:
            home = response.content.decode('ISO-8859-1')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            print("Encontramos {} noticias".format(len(links_to_notices)))
            ide = 1
            for link in links_to_notices:
                print(ide)
                url_content = link.split('/')
                category = url_content[1]
                year = url_content[2]
                month = url_content[3]
                day = url_content[4]
                date = day+"-"+month+"-"+year
                if category != 'inf' and category != 'publicaciones':
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