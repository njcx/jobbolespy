# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
from bs4 import BeautifulSoup
import pdfkit

def download(url):
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.15 Safari/537.36'}
    r=requests.get(url,headers=headers)
    return r
    
def get_url_list(url):
    response = download(url).text
    soup = BeautifulSoup(response, "lxml")
    menu_tag = soup.find_all(class_="grid-8")[0]
    urls = []
    for li in menu_tag.find_all(class_="post-thumb"):
        url = li.a.get("href")
        urls.append(url)
    return urls
def parse_url_to_html(url,name='1.html'):
    response = download(url).text
    soup = BeautifulSoup(response, "lxml")
    body = soup.find_all(class_="entry")[0]
    title = soup.find('h1').get_text()
    center_tag = soup.new_tag("center")
    title_tag = soup.new_tag('h1')
    title_tag.string = title
    center_tag.insert(1, title_tag)
    body.insert(1, center_tag)

    html =str(body)
    with open(name, 'wb') as f:
        f.write(html)
        
def save(url,page=None):
    urls = get_url_list(url)
    
    htmls=[]
    for x in urls:
        name = str(page)+str(urls.index(x))+'.html'
        print x
        parse_url_to_html(x,name)
        htmls.append(name)
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ]
    }
    pdfname = str(page)+'.pdf'
    pdfkit.from_file(htmls,pdfname, options=options)
    return htmls

if __name__ == '__main__':
    lists = []
    for page in range(1,13+1)[::-1]:
        url = 'http://python.jobbole.com/category/guide/page/{}/'.format(page)
        save(url,page)
        
