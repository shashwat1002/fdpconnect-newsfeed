import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import json




def scrap_english_page(url, corpus_file):
    # assuming that both the files are in append mode
    headers ={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
    response = requests.get(url, headers=headers)
    soup_for_page = BeautifulSoup(response.content, 'html.parser')

    all_paragraphs = soup_for_page.find_all('p')
    parsed_url = urllib.parse.urlparse(url)
    title = soup_for_page.title

    publish_time = soup_for_page.find("meta", attrs={"name": "publish-date"})

    update_time = soup_for_page.find("meta", attrs={"name": "publish-date"})
    #print(time)

    output_text = ""

    for para in all_paragraphs:
        for content in para.contents:


            content_string = content.string
            if content_string is not None:
                # if it's a reference then we don't want to write the text
                output_text += content_string
    
    output_dict = {
        "url": url,
        "title": title.string,
        "publish_time": publish_time.string,
        "updated_time": update_time.string,
        "content": output_text
    }
    json_content = json.dumps(output_dict, indent=4)
    corpus_file.write(json_content)
    return json_content

# Driving code begins here: 

def main():

    url = input()
    corpus_file = open("hindu_article.json", "a")

    scrap_english_page(url, corpus_file)

main()







