import re
import time
import urllib
from multiprocessing import Pool
import requests
from requests_html import HTML
from utils import pretty_print


def fetch(url):                     #擷取網頁頁面
    response = requests.get(url, cookies={'over18': '1'})  # 一直向 server 回答滿 18 歲了 !
    return response

def parse_article_entries(doc):            #抓整行區塊
    html = HTML(html=doc)
    post_entries = html.find('div.r-ent')
    return post_entries

def parse_article_meta(ent):               #抓區塊內想要的資料
    ''' Step-3: parse the metadata in article entry
    '''
    meta = {
        'title': ent.find('div.title', first=True).text,
        'push': ent.find('div.nrec', first=True).text,
        'date': ent.find('div.date', first=True).text,
    }

    try:
        meta['author'] = ent.find('div.author', first=True).text
        meta['link'] = ent.find('div.title > a', first=True).attrs['href']
    except AttributeError:
        if '(本文已被刪除)' in meta['title']:
            match_author = re.search('\[(\w*)\]', meta['title'])
            if match_author:
                meta['author'] = match_author.group(1)
        elif re.search('已被\w*刪除', meta['title']):
            match_author = re.search('\<(\w*)\>', meta['title'])
            if match_author:
                meta['author'] = match_author.group(1)
    return meta

def get_metadata_from(url):

    def parse_next_link(doc):
        html = HTML(html=doc)
        controls = html.find('.action-bar a.btn.wide')
        link = controls[1].attrs.get('href')
        return urllib.parse.urljoin('https://www.ptt.cc/', link)

    resp = fetch(url)
    post_entries = parse_article_entries(resp.text)
    next_link = parse_next_link(resp.text)

    metadata = [parse_article_meta(entry) for entry in post_entries]
    return metadata, next_link

def get_paged_meta(url, num_pages):
    collected_meta = []

    for _ in range(num_pages):
        posts, link = get_metadata_from(url)
        collected_meta += posts
        url = urllib.parse.urljoin('https://www.ptt.cc/', link)

    return collected_meta

start_url = 'https://www.ptt.cc/bbs/movie/index.html'
metadata = get_paged_meta(start_url, num_pages=5)
for meta in metadata:
    pretty_print(meta['push'], meta['title'], meta['date'], meta['author'])
    # print(meta)

# url = 'https://www.ptt.cc/bbs/movie/index.html'
# resp = fetch(url)  # step-1
# post_entries = parse_article_entries(resp.text)  # step-2
#
# for entry in post_entries:
#     meta = parse_article_meta(entry)
#     print(meta)  # result of setp-3