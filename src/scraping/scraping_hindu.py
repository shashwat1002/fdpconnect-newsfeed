import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import json
from icecream import ic
import xmltodict

from . import *

XML_SITEMAP_URL = "https://www.thehindu.com/sitemap/googlenews/all/all.xml"


def scrap_english_page(url):
    # assuming that both the files are in append mode
    headers = HEADERS
    response = requests.get(url, headers=headers)
    soup_for_page = BeautifulSoup(response.content, 'html.parser')

    all_paragraphs = soup_for_page.find_all('p')
    parsed_url = urllib.parse.urlparse(url)
    title = soup_for_page.title

    #print(time)

    output_text = ""

    for para in all_paragraphs:
        for content in para.contents:


            content_string = content.string
            if content_string is not None:
                # if it's a reference then we don't want to write the text
                output_text += content_string

    img_url = ""

    img_div = soup_for_page.find("div", {"class": "lead-img-cont"})

    if img_div is not None:
        source_obj = img_div.find("source")
        #ic(images)
        try:
            img_url = source_obj["srcset"]
        except TypeError:
            pass

    output_dict = {
        "content": output_text
    }

    if img_url != "":
        output_dict["image_url"] = img_url

    return output_dict

# Driving code begins here: 

def main():

    url = input()
    corpus_file = open("hindu_article.json", "a")

    scrap_english_page(url)

# main()





# list_of_articles = process_sitemap_xml(XML_SITEMAP_URL, scrap_english_page, NUM_ARTICLES)
# ic(list_of_articles)





