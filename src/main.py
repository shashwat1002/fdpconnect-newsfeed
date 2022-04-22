from settings import *
from scraping.google_news_sitemap import *

import scraping.scraping_hindu as hindu
import scraping.scraping_businessstandard as businessstandard
import scraping.scraping_economictimes as economictimes
import scraping.scraping_financialexpress as financialexpress
import scraping.scraping_livelaw as livelaw
import scraping.scraping_maritime as maritime
import scraping.scraping_mint as mint

from icecream import ic
import pickle
import csv



def load_vecorizer_classifier():
    CLASSIFIER = pickle.load(open(os.path.join(SAVE_ROOT_DIR, CLASSIFIER_FILE_NAME), "rb"))
    VECTORIZER = pickle.load(open(os.path.join(SAVE_ROOT_DIR, VECTORIZER_FILE_NAME), "rb"))

    return (CLASSIFIER, VECTORIZER)

def write_articles(articles):
    with open(SCRAPED_DATA, "a") as output_file:
        fieldnames = ['title', 'keywords', 'url', 'image_url', 'lastmod', 'content']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        for article in articles:
            writer.writerow(article)

def main():

    classifier, vectorizer = load_vecorizer_classifier()

    if not os.path.exists(SCRAPED_DATA):
        with open(SCRAPED_DATA, "w") as output_file:
            output_file.write("title,keywords,url,image_url,lastmod,content\n")
            output_file.close()

    articles = []

    articles += process_sitemap_xml(hindu.XML_SITEMAP_URL, hindu.scrap_english_page, -1, vectorizer, classifier)
    write_articles(articles)
    articles += process_sitemap_xml(businessstandard.XML_SITEMAP_URL, businessstandard.scrap_english_page, -1, vectorizer, classifier)
    write_articles(articles)
    articles += process_sitemap_xml(economictimes.XML_SITEMAP_URL, economictimes.scrap_english_page, -1, vectorizer, classifier)
    write_articles(articles)
    articles += process_sitemap_xml(financialexpress.XML_SITEMAP_URL, financialexpress.scrap_english_page, -1, vectorizer, classifier)
    write_articles(articles)
    articles += process_sitemap_xml(livelaw.XML_SITEMAP_URL, livelaw.scrap_english_page, -1, vectorizer, classifier)
    write_articles(articles)
    articles += maritime.process_sitemap_xml(maritime.XML_SITEMAP_URL, maritime.scrap_english_page, -1)
    write_articles(articles)
    articles += process_sitemap_xml(mint.XML_SITEMAP_URL, mint.scrap_english_page, -1, vectorizer, classifier)
    write_articles(articles)



main()
