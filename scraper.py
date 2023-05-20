#! /usr/bin/env python3
from bs4 import BeautifulSoup
import requests

url = 'https://cavestory.fandom.com/wiki/Category:Characters'
http = requests.get(url)

soup = BeautifulSoup(http.text, 'html.parser')

page_members = soup.find('div', class_='category-page__members')
page_member_categories = page_members.find_all('div', class_='category-page__members-wrapper')

page_urls = set()
for i in page_member_categories:
    page_anchors = i.select('ul > li > a')
    for a in page_anchors:
        if not 'Category' in a.get('href'):
            page_urls.add(f'https://cavestory.fandom.com{a.get("href")}')


for url in page_urls:
    print(f'Page scraped: {url}')
    print('')
    http = requests.get(url)
    soup = BeautifulSoup(http.text, 'html.parser')
    sprite = soup.find('img', class_='pi-image-thumbnail')
    sprite_src = sprite.get('src')
    print(f'Sprite URL: {sprite_src}')
