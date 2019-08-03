# -*- coding: utf-8 -*-
import requests
import sys
import os
from bs4 import BeautifulSoup
url = 'http://admlist.ru/'
import codecs
import sqlite3
import html as h

if len(sys.argv)<2 or sys.argv[1] == '--help' :
    print('Create [n]ew table or [F]ind student')
elif sys.argv[1].lower() == 'n':
    print('Going to delete previous db, are you sure? y/n')
    while inp.lower() not in 'yn':        
        inp = input()
        if inp.lower() == 'y':
            pass
        elif inp.lower() == 'n':
            print('Try again')
            quit()
        else:
            print('Can\'t recognize, try again.')
    try:
        os.remove('Students.db')
    except:
        print('Did not find the previous database, creating a new one')
    conn=sqlite3.connect('Students.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE students
                      (surname text, name text, patronymic text,
                       university text, faculty text)
                   """)
      

    def get_html(url):
        response = requests.get(url)
#        print(response.encoding)
        text = h.unescape(response.text)
        return (codecs.decode((bytearray(str(text.replace('\u221e',' ')),response.encoding))))

    def get_all_links(html):
        soup = BeautifulSoup(html, features = "html.parser")
        ass = soup.find_all('a')
   
        links = []
        
        for a in ass:
            try:
                link = a.attrs['href']
               # print(a.text)
                links.append((link,a.text))
            except Exception as e:
                print(e)
                pass
        return links
    Universities = get_all_links(get_html(url))[2:]
    for Univ,Univ_name in Universities:
        Univ_faculties = get_all_links(get_html(url+Univ))
#        print(Univ_name)
        for Faculty,Faculty_name in Univ_faculties[1:]:
            #print(url+Univ[:-11]+'/'+Faculty)
            html = get_html(url+Univ[:-11]+'/'+Faculty)
            soup = BeautifulSoup(html, features = "html.parser")
#            print(len(soup.find_all('table')))
            if len(soup.find_all('table')) < 2:
                print(Faculty_name + ' No students on faculty')
                continue
            trs = soup.find_all('table')[1].find_all('tr')
            i = 0

            for t in trs[1:]:
                tds = t.find_all('td')
#                print(type(tds))
                Full_name = str(tds[3])[4:-5].split()
                tmp = ['']
                if len(Full_name)>3:
                    for i in range(len(Full_name)-2):
                        tmp[0]+=(Full_name[i]+' ')
                    for i in range(len(Full_name)-2,len(Full_name)):
                        tmp.append(Full_name[i])
#                    print(tmp)
                    tmp[0] = tmp[0].strip()
                    Full_name = tmp
                elif len(Full_name)<3:
                    for i in range(3-len(Full_name)):
                        Full_name.append(' ')
                Full_name+=[Univ_name,Faculty_name]
                for i in Full_name:
                    i.replace(' ', '')
                try:
                    cursor.execute("INSERT INTO students VALUES (?,?,?,?,?)", tuple(Full_name))
                    conn.commit()
                except:
                    print(Full_name)
            
            print(Faculty_name)
        print(Univ_name)
elif sys.argv[1].lower() == 'f':
    conn=sqlite3.connect('Students.db')
    cursor = conn.cursor()
    while True:
        Name = input('Name : ')
        Surname = input('Surname : ')
        Patronymic = input('Patronymic : ')
        if Name:
            if Surname:
                if Patronymic:
                    sql = "SELECT * FROM students WHERE name=? AND surname = ? AND patronymic = ?  "
                    cursor.execute(sql, [Name,Surname,Patronymic])
                    for match in cursor.fetchall():
                        print(' '.join(match))
                else:
                    sql = "SELECT * FROM students WHERE name=? AND surname = ?"
                    cursor.execute(sql, [Name,Surname])
                    for match in cursor.fetchall():
                        print(' '.join(match))

            else:
                if Patronymic:
                    sql = "SELECT * FROM students WHERE name=? patronymic = ?  "
                    cursor.execute(sql, [Name,Patronymic])
                    for match in cursor.fetchall():
                        print(' '.join(match))
                else:
                    sql = "SELECT * FROM students WHERE name=? "
                    cursor.execute(sql, [Name])
                    for match in cursor.fetchall():
                        print(' '.join(match))
        else:
            if Surname:
                if Patronymic:
                    sql = "SELECT * FROM students WHERE surname = ? AND patronymic = ?  "
                    cursor.execute(sql, [Surname,Patronymic])
                    for match in cursor.fetchall():
                        print(' '.join(match))
                else:
                    sql = "SELECT * FROM students WHERE surname = ?"
                    cursor.execute(sql, [Surname])
                    for match in cursor.fetchall():
                        print(' '.join(match))

            else:
                if Patronymic:
                    sql = "SELECT * FROM students WHERE patronymic = ?  "
                    cursor.execute(sql, [Patronymic])
                    for match in cursor.fetchall():
                        print(' '.join(match))
                else:
                    print('Bye-bye')
                    quit()

            
    pass
else:
    pass
try:
    conn.commit()
except:
    print('--help to help')
