import requests
import bs4
import pandas as pd
import unidecode

#Getting the url
req = requests.get('http://billwurtz.com/songs.html')
bs = bs4.BeautifulSoup(req.text, 'lxml')

#Create title series
title = []
for i in bs.find_all('a'):
    title.append(i.contents[0])
title.pop()
title = pd.Series(title)

#Create link series
link = []
for i in bs.find_all('a', href=True):
    link.append('https://' + i['href'])
link.pop()
link = pd.Series(link)

#Create released and duration series
released = []
duration = []
for i in bs.find_all('td'):
    if len(i.contents) == 1:
        i = unidecode.unidecode(i.contents[0])
        if i in (' ', '\n'):
            pass
        else:
            released.append(i)
    elif len(i.contents) == 2:
        if i.contents[1] in (' ', '\n'):
            pass
        else:
            i = unidecode.unidecode(i.contents[1])
            duration.append(i)
released.pop()
released = pd.Series(released)

#Cleaning the duration
dur = []
for i in duration:
    i = i.replace(' ', '').replace('(', '').replace(')', '')
    dur.append(i)
dur = pd.Series(dur)

#Making the dataframe of the result
result = pd.DataFrame(data={'title':title,
                            'link':link,
                            'released':released,
                            'duration':duration})

#Convert into csv file
result.to_csv('result_billwurtz.csv')
#Convert into json file
result.to_json('result_billwurtz.json', orient='records'    )
