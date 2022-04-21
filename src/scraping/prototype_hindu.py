import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import json
from icecream import ic
import xmltodict
XML_SITEMAP_URL = "https://www.thehindu.com/sitemap/googlenews/all/all.xml"


def scrap_english_page(url):
    # assuming that both the files are in append mode
    headers ={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
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
        except KeyError:
            pass

    output_dict = {
        "image_url": img_url,
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

    response = requests.get(url)



    obj_rep = xmltodict.parse(response.content)

    list_of_article_dicts = []



    for num, dict_rep in enumerate(obj_rep["urlset"]["url"]):
        article_dict = {}
        article_dict["url"] = dict_rep["loc"]
        article_dict["title"] = dict_rep["news:news"]["news:title"]
        article_dict["lastmod"] = dict_rep["lastmod"]

        content_dict = scrap_english_page(article_dict["url"])
        content_dict.update(article_dict)
        list_of_article_dicts.append(content_dict)
        # if num == 10:
        #     break


    return list_of_article_dicts



# list_of_articles = process_sitemap_xml(XML_SITEMAP_URL)
# ic(list_of_articles)





