import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import json
from icecream import ic
import xmltodict

def process_sitemap_xml(url, scrap_english_page):

    response = requests.get(url)



    obj_rep = xmltodict.parse(response.content)

    list_of_article_dicts = []



    for num, dict_rep in enumerate(obj_rep["urlset"]["url"]):
        article_dict = {}
        article_dict["url"] = dict_rep["loc"]
        article_dict["title"] = dict_rep["news:news"]["news:title"]
        article_dict["lastmod"] = dict_rep["lastmod"]

        try:
            article_dict["image_url"] = dict_rep["image:image"]["image:loc"]
        except KeyError:
            article_dict["image_url"] = ""

        content_dict = scrap_english_page(article_dict["url"])
        article_dict.update(content_dict)
        list_of_article_dicts.append(article_dict)
        # if num == 10:
        #     break


    return list_of_article_dicts
