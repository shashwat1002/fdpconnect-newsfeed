import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import json
import xml.etree.ElementTree as ET
from icecream import ic

XML_SITEMAP_URL = "https://www.maritimegateway.com/post-sitemap1.xml"


def scrap_english_page(url):
    # assuming that both the files are in append mode
    headers ={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    response = requests.get(url, headers=headers)
    soup_for_page = BeautifulSoup(response.content, 'html.parser')

    all_paragraphs = soup_for_page.find_all('p')
    parsed_url = urllib.parse.urlparse(url)
    title = soup_for_page.title

    output_text = ""

    for para in all_paragraphs:
        for content in para.contents:


            content_string = content.string
            if content_string is not None:
                # if it's a reference then we don't want to write the text
                output_text += content_string

    title = ""

    title_obj = soup_for_page.find("title")
    title = title_obj.contents[0]

    output_dict = {
        "title": title,
        "content": output_text
    }
    return output_dict

# Driving code begins here: 

def main():

    url = input()
    corpus_file = open("hindu_article.json", "a")

    scrap_english_page(url)

# main()


def process_sitemap_xml(url):
    headers ={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    response = requests.get(url, headers=headers)

    tree = ET.fromstring(response.content)

    list_of_article_dicts = []

    for num, child in enumerate(tree):
        article_dict = {}
        lastmod = ""
        url = ""
        image_url = ""
        keywords = ""
        for i, child2 in enumerate(child):
            if i == 0:
                article_dict["url"] = child2.text
            if i == 1:
                article_dict["lastmod"] = child2.text
            if i == 2:
                for j, child3 in enumerate(child2):
                    if j == 0:
                        article_dict["image_url"] = child3.text
        article_dict["keywords"] = ""
        # the above line is to adhere to format

        content_dict = scrap_english_page(article_dict["url"])
        content_dict.update(article_dict)
        list_of_article_dicts.append(content_dict)
        if num == 10:
            break


    return list_of_article_dicts



# list_of_articles = process_sitemap_xml(XML_SITEMAP_URL)
# ic(list_of_articles)





