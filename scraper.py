#! /usr/bin/env python3
import requests, os
from bs4 import BeautifulSoup
from pathlib import Path

p = Path(__file__).parents[1]

if not os.path.exists(f'{p}/scraped'):
    os.mkdir(f'{p}/scraped')
else:
    print('Scrape Directory already exists. Overwrite? Y/n')
    if input() == 'y':
        pass
    else:
        exit()

def get_pages(url):
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
    return page_urls

def get_sprites(page_urls):
    for url in page_urls:
        print(f'\n\nPage scraped: {url}')
        http = requests.get(url)
        soup = BeautifulSoup(http.text, 'html.parser')
        header2 = soup.find_all('h2')
        for h2 in header2:
            print(h2.text)
            if h2.text == 'Sprites':
                figure = h2.find_next('figure')
                sprite = figure.img
            else:
                continue

            sprite_src = sprite.get('src')
            sprite_url.add(sprite_src)
            print(f'Sprite URL: {sprite_src}')

character_index_url = 'https://cavestory.fandom.com/wiki/Category:Characters'
enemy_index_url = 'https://cavestory.fandom.com/wiki/Category:Enemies'
character_page_urls = set(get_pages(character_index_url))
enemy_page_urls = set(get_pages(enemy_index_url))

sprite_url = set()
unsuccesful_page_url = set()
get_sprites(enemy_page_urls)
get_sprites(character_page_urls)

for url in sprite_url:
    with open(f'{p}/scraped/sprite_url.csv', 'a') as a:
        a.write(f'{url},\n')

    with open(f'{p}/scraped/sprites.html', 'a') as a:
        a.write(f'<img src="{url}"><br>')

for url in unsuccesful_page_url:
    with open(f'{p}/scraped/unsuccesful_sprite_url.csv', 'a') as a:
        a.write(f'{url},\n')
