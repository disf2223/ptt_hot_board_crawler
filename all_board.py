import urllib
import requests
from requests_html import HTML
import pymongo


def page_info(url):                                                                    # 擷取網頁頁面
    response = requests.get(url, cookies={'over18': '1'})  # 一直向 server 回答滿 18 歲了 !
    return response


def get_board_link(doc):                                                               # 抓取各版網址
    board_urls = []
    html = HTML(html=doc)
    board_links = html.find('div.b-ent a.board')  # 抓取各版網址
    for board_link in board_links:
        link = board_link.attrs.get('href')
        board_urls.append(urllib.parse.urljoin('https://www.ptt.cc/', link))
    return board_urls

def get_article_link(doc):                                                              #取得當前頁面的全部文章網址
    article_urls = []
    html = HTML(html=doc)
    article_links = html.find('div.title a')  # 抓取各文章網址
    for article_link in article_links:
        art_link = article_link.attrs.get('href')
        article_urls.append(urllib.parse.urljoin('https://www.ptt.cc/', art_link))
    return article_urls


def next_page_link(doc):                                                                #取得下一頁的網址
    html = HTML(html=doc)
    next_link = html.find('.action-bar a.btn.wide')
    link = next_link[1].attrs.get('href')
    next_url = urllib.parse.urljoin('https://www.ptt.cc/', link)
    return next_url

def get_meta_data(doc):                                                                 #取得文章想要的資料
    mata = {}
    push_list = []
    html = HTML(html=doc)
    mata['作者'] = html.find('span.article-meta-value')[0].text
    mata['標題'] = html.find('span.article-meta-value')[2].text
    mata['文章分類'] = html.find('span.article-meta-value')[1].text
    mata['內文'] = html.find('div#main-container')[0].text.split('--')[0].split("\n")[4]
    mata['貼文時間'] = html.find('span.article-meta-value')[3].text
    mata['標準網址'] = article_url
    art_pushs = html.find('div.push')
    for art_push in art_pushs:
        push_list.append(art_push.text)
    mata['推文'] = push_list
    return mata

"""
連接MongoDB
"""
myclient = pymongo.MongoClient('http://localhost')
db = myclient.db_name
col = db.collection_name


url = 'https://www.ptt.cc/bbs/index.html'
resp = page_info(url)
board_urls = get_board_link(resp.text)
for board_url in board_urls:
    board_resp = page_info(board_url)
    article_urls = get_article_link(board_resp.text)
    for article_url in article_urls:
        article_resp = page_info(article_url)
        meta = get_meta_data(article_resp.text)
        tcol.insert_one(meta)
    while next_page_link(board_resp.text) != 0:
        board_resp = page_info(next_page_link(board_resp.text))
        article_urls = get_article_link(board_resp.text)
        for article_url in article_urls:
            article_resp = page_info(article_url)
            meta = get_meta_data(article_resp.text)
            print(meta)
            tcol.insert_one(meta)

