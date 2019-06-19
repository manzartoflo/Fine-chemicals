#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 11:47:29 2019

@author: manzar
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

url = 'https://www.informa-japan.com/finechemicals/complist/en/index.php'
req = requests.get(url)
soup = BeautifulSoup(req.text, 'lxml')
uls = soup.findAll('ul', {'class': 'exhibitor'})
count = 0
links = []
for ul in uls:
    lis = ul.findAll('li')
    for li in lis:
        try:
            links.append(urljoin(url, li.a.attrs['href']))
            count += 1
        except:
            pass
header = 'Company Name, telephone, Fax, Email, Website\n'
file = open('assignment.csv', 'w')
file.write(header)
for link in links:
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    name = soup.findAll('div', {'class': 'companyName'})[0].text.replace('\r', '').replace('\n', '').replace(',', '')
    block = soup.findAll('table', {'class': 'MgnT10'})
    contents = block[0].findAll('td')
    number = []
    email = ''
    web = ''
    for x in contents:
        try:
            if(not any(c.isalpha() for c in x.text.replace('-', ''))):
                number.append(x.text)
        except:
            pass
        
        try:
            if('@' in x.a.attrs['href']):
                email = x.a.attrs['href'].split('mailto:')[1]
        except:
            pass
        
        try:
            if('www' in x.a.attrs['href']):
                web = x.a.attrs['href']
        except:
            pass
        
    if(len(number) == 0):
        tel = 'NaN'
        fax = 'NaN'
    elif(len(number) == 1):
        if(len(number[0]) > 3):
            tel = number[0]
        else:
            tel = 'NaN'
            fax = 'NaN'
    elif(len(number) == 2):
        tel = number[0]
        fax = number[1]
        
    if(len(email) > 3):
        pass
    else:
        email = 'NaN'
        
    if(len(web) > 3):
        pass
    else:
        web = 'NaN'
    file.write(name.replace('  ', '') + ', ' + tel + ', ' + fax + ', ' + email + ', ' + web + '\n')
    print(name.replace('  ', ''))
file.close()
file = pd.read_csv('assignment.csv')
        