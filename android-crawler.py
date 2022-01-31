import json
import requests
import datetime
import pandas as pd
import bs4
import os
from _operator import indexOf

location = os.path.dirname(__file__)
try:
    os.makedirs(location + '/outFiles')
except FileExistsError as e:
    pass
new_location = os.path.dirname(__file__) + '/outFiles/'

list_of_links = []
path = ''
host = 'https://developer.android.com/reference/android/app/'
list_of_packge = 'https://developer.android.com/reference/android/app/package-summary'
packages = requests.get(list_of_packge)
package_soup = bs4.BeautifulSoup(packages.text, 'html.parser')
article = package_soup.find('div', class_='devsite-article-body clearfix devsite-no-page-title')
total_package_list = article.find('div', id='jd-content')
package_list = total_package_list.find_all('table', class_='jd-sumtable-expando')
for i in package_list:
    divide = i.find_all('td', class_='jd-linkcol')
    for obj in divide: 
        list_of_links.append(obj.text.strip())

for k in list_of_links:
    newlink = host + k
    if('<' in newlink):
        z = newlink.index('<')
        newlink = newlink[0:z]
    names = []
    warnings = []
    test = {}
    page = requests.get(newlink)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    list = soup.find('article', class_='devsite-article')
    total = list.find('div', id='jd-content')
    api = total.find_all('div')
    filename = k + '.txt'
    complete_file = os.path.join(new_location, filename)
    f = open(complete_file, "w+")
    
    for i in api:
        caution = i.find_all('p', class_='caution')
        name = i.find('h3', class_='api-name')
        note = i.find_all('p', class_='note')
        if (name == None):
            continue
        result = ''
        for ca in caution:
            result += ca.text.strip().replace('\n','').replace('\r',"").replace('\t', '') + " "
        name = name.text.strip()
        note_result = ''
        for no in note:
            note_result += no.text.strip().replace('\n','').replace('\r',"").replace('\t', '') + " "
        if(result == '' and note_result == ''):
            continue
        else:
            if(result == ''):
                f.write(name + ":")
                f.write(note_result + '\n')
            else:
                f.write(name + ":")
                f.write(result + '\n')
    f.close()
    filesize = os.path.getsize(complete_file)
    if(filesize == 0):
        os.remove(complete_file)
