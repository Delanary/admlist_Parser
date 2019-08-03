import requests
import sys
from bs4 import BeautifulSoup
url = 'http://admlist.ru/'
import codecs
import sqlite3
conn=sqlite3.connect('Students.db')
cursor = conn.cursor()
if len(sys.argv)<2:
    print('Create [n]ew table or [F]ind student')
elif sys.argv[1].lower() == 'n':
    
    cursor.execute("""CREATE TABLE students
                      (name text, surname text, patronymic text,
                       university text, faculty text)
                   """)
      

    def get_html(url):
        response = requests.get(url)
        text = codecs.decode(response.text, 'unicode_escape')

        return text

    def get_all_links(html):
        soup = BeautifulSoup(html, features = "html.parser")
        ass = soup.find_all('a')

        links = []
        
        for a in ass:
            try:
                link = a.attrs['href']            
                links.append(link)
            except Exception as e:
                print(e)
                pass
        return links
    Universities = get_all_links(get_html(url))[2:]
    for Univ in Universities:
        Univ_faculties = get_all_links(get_html(url+Univ))
        for Faculty in Univ_faculties:
            html = get_html(url+Univ+Faculty)
            soup = BeautifulSoup(html, features = "html.parser")
            tds = soup.find_all('td')
            lol = 0
            for td in tds:
                if lol == 8:
                    pass
        print(Univ)
elif sys.argv[1].lower == 'f':
    pass
else:
    pass
