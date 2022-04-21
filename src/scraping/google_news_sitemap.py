import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import json
from icecream import ic
import xmltodict

HEADERS ={"User-Agent" : "Googlebot-News Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
NUM_ARTICLES = 10

def process_sitemap_xml(url, scrap_english_page, num_articles):

    headers = HEADERS
    response = requests.get(url, headers=HEADERS)



    obj_rep = xmltodict.parse(response.content)

    list_of_article_dicts = []



    for num, dict_rep in enumerate(obj_rep["urlset"]["url"]):
        article_dict = {}
        article_dict["url"] = dict_rep["loc"]
        article_dict["title"] = dict_rep["news:news"]["news:title"]
        try:
            article_dict["lastmod"] = dict_rep["lastmod"]
        except KeyError:
            article_dict["lastmod"] = dict_rep["news:news"]["news:publication_date"]

        try:
            article_dict["image_url"] = dict_rep["image:image"]["image:loc"]
        except KeyError:
            article_dict["image_url"] = ""

        try:
            article_dict["keywords"] = dict_rep["news:news"]["news:keywords"]
        except KeyError:
            article_dict["keywords"] = ""

        content_dict = scrap_english_page(article_dict["url"])
        article_dict.update(content_dict)
        list_of_article_dicts.append(article_dict)
        if num == num_articles:
            break


    return list_of_article_dicts
