#Code by Kenzawaa
#Copyright © by Kenzawaa
#GitHub: https://github.com/pengode-handal/nontonanimeid-dl

from random_user_agent.user_agent import UserAgent
from tabulate import tabulate
import requests
from bs4 import BeautifulSoup as bs
s = requests.Session()
import argparse

parse = argparse.ArgumentParser()

parse.add_argument('-t', '--title', help='Get anime by title', nargs='+')
args = parse.parse_args()

import random

xsrf = (random.random())*10**16
s.headers.update({
"Cookie": "_xsrf="+str(xsrf),
"X-XSRFToken": str(xsrf),
"User-Agent": UserAgent().get_random_user_agent()
})

def pendekinUrl(url):
    BASEURL = 'https://bitly.com/data/anon_shorten'
    BASEURL1 = 'https://snip.ly/pub/snip'
    data = {
        "url": url
    }
    res = s.post(BASEURL, data).json()
    if res['status_txt'] != 'OK':
        if res['status_txt'] == 'RATE_LIMIT_EXCEEDED':
            data['button_url'] = 'https://sniply.io/pricing/'
            data['cta_message'] = "Sign up and customize the CTA!"
            try: return requests.post('https://snip.ly/pub/snip', data).json()['snip_url']
            except: return url+' (bit.ly limit)'
        return 'Error: ' + res['status_txt']
    else:
        return res['data']['link']
    

def animDl(url):
    res = s.get(url)
    soup_raw = bs(res.content, 'html.parser').find_all('div', {'class': 'listlink'})
    data = []
    for soup in soup_raw:
        listlink = soup.find_all('a')
        print('='*30)
        for i in listlink:
            try: link = pendekinUrl(i['href'])
            except: link = i['href']
            anu = i.text
            data.append([anu,link])
        print(tabulate(data, [soup.span.text.strip(), '']))
        data.clear()
        


def Main(title):
    url = 'https://75.119.159.228/?s={}'.format(title)
    if s.get(url).status_code == 404:
        exit('Anime not found')
    else: base = s.get(url).content
    soup = bs(base, 'html.parser').find('div', {'class': 'result'}).find_all('a')
    data = []
    for i in soup:
        data.append(i['href'])
    a = 1
    for x in data: print(str(a)+'. '+x); a +=1
    if len(data) == 1:
        nexturl = data[0]
    else:
        try: 
            choice = int(input(f'input from 1 to {len(data)}: '))
            nexturl = data[choice-1]
        except: exit('Input the correct choice')
    soub = bs(s.get(nexturl).content, 'html.parser').find('div', string='Episode Terakhir')
    jumlahEps = soub.next_sibling.text.replace('Episode ', '').strip()
    link = soub.parent.find('a')['href'].split('episode')[0]
    choice = int(input(f'Select episode from 1 to {jumlahEps}: '))
    if choice > int(jumlahEps): exit('Input the correct choice')
    else: pass
    link = link+'episode-'+str(choice)
    animDl(link)
    print('\n Lokal harus headernya Referer: 75.119.159.228')
    

if args.title:
    Main(' '.join(args.title))
else:
    print('Input argumen')
