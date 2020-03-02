import re
import time
import urllib
from multiprocessing import Pool
import requests
from requests_html import HTML
from utils import pretty_print

def page_info(url):                                                                    #擷取網頁頁面
    response = requests.get(url, cookies={'over18': '1'})  # 一直向 server 回答滿 18 歲了 !
    return response

def get_board_link(doc):                                                             #抓整行區塊
    board_urls = []
    html = HTML(html=doc)
    board_links = html.find('div.b-ent a.board')                                     #抓取各版網址
    for board_link in board_links:
        link = board_link.attrs.get('href')
        board_urls.append(urllib.parse.urljoin('https://www.ptt.cc/', link))
    return board_urls

def article_info(url_list):
    def get_article_link(doc):
        article_urls = []
        html = HTML(html=doc)
        article_links = html.find('div.title')                                      # 抓取各文章網址
        for article_link in article_links:
            art_link = article_link.attrs.get('href')
            article_urls.append(urllib.parse.urljoin('https://www.ptt.cc/', art_link))
            # print(art_link)
        return article_urls

    for board_url in url_list:
        board_resp = page_info(board_url)
        article = get_article_link(board_resp.text)





url = 'https://www.ptt.cc/bbs/index.html'
resp = page_info(url)
board_urls = get_board_link(resp.text)
# articleurl = article_info(board_urls)
print(board_urls)

