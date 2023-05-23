#! /usr/bin/env python3

# THIS CODE IS UTTER CRAP
# and I know it. to be totally honest I was about to 
# completely abandon this project after I got what I needed
# because it was becoming a timesuck.
# however, I noticed it was being watched by someone.
# and I have never had anyone star/watch one of my little projects before.
# so, I decided to do a quick and dirty finish just for that person.
# This one is for you, wervland.

# many of the images in this wiki are hidden behind js
# and I don't care enough to use selenium to work around that.

import requests, os, json
from shutil import rmtree
from bs4 import BeautifulSoup
from pathlib import Path


p = Path(__file__).parents[1]

if not os.path.exists(f'{p}/scraped/cavestory'):
    os.mkdir(f'{p}/scraped/cavestory')
    os.mkdir(f'{p}/scraped/cavestory/emojis')
else:
    print('Scrape Directory already exists. Overwrite? Y/n')
    if input() == 'y':
        rmtree(f'{p}/scraped/cavestory')
        os.mkdir(f'{p}/scraped/cavestory')
        os.mkdir(f'{p}/scraped/cavestory/emojis')
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
        sprite = None
        print(f'\n\nPage scraped: {url}')
        http = requests.get(url)
        soup = BeautifulSoup(http.text, 'html.parser')
        header2 = soup.find_all('h2')
        infobox = soup.find('table', class_='infobox')
        for h2 in header2:
            if h2.text == 'Sprites':
                figure = h2.find_next('figure')
                sprite = figure.img

        if infobox:
            for th in infobox.find_all('th'):
                if th.text == 'Sprites':
                    sprite = th.img
        if sprite:
            sprite_src = sprite.get('src')
            sprite_url.add(sprite_src)
            print(f'Sprite URL: {sprite_src}')
            name = soup.find('span', class_='mw-page-title-main').text
            name = name.replace(' ', '_')
            get_sprites = requests.get(sprite_src)
            with open(f'{p}/scraped/cavestory/emojis/cavestory_{name}.png', 'wb') as wb:
                wb.write(get_sprites.content)

            pack['files'].update({f'{name}':f'{name}.png'})






def sprite_dict_constructor(url):
    http = requests.get(url)
    soup = BeautifulSoup(http.text, 'html.parser')

    return name.text

character_index_url = 'https://cavestory.fandom.com/wiki/Category:Characters'
enemy_index_url = 'https://cavestory.fandom.com/wiki/Category:Enemies'
character_page_urls = set(get_pages(character_index_url))
enemy_page_urls = set(get_pages(enemy_index_url))

sprite_url = set()
pack = {'files': {}, 'pack': {}, 'files_count': 0}
get_sprites(enemy_page_urls)
get_sprites(character_page_urls)


# write out the files
with open(f'{p}/scraped/cavestory/emojis/pack.json', 'w') as w:
    json.dump(pack, w)

for url in sprite_url:
    with open(f'{p}/scraped/cavestory/sprite_url.csv', 'a') as a:
        a.write(f'{url},\n')

    with open(f'{p}/scraped/cavestory/sprites.html', 'a') as a:
        a.write(f'<img src="{url}"><br>')

