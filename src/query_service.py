from flask import Flask
from flask import request, json
from settings import *
import os

from vectorization import sort_relevance
import pickle

import pandas as pd

from icecream import ic

HOST = "localhost"

VECTORIZER = pickle.load(open(os.path.join(SAVE_ROOT_DIR, VECTORIZER_FILE_NAME), "rb"))


app = Flask(__name__)

@app.route("/query", methods=['GET'])
def query_feed():

    keywords = request.args["keywords"]
    dataframe = pd.read_csv("scraped.csv", engine="python", error_bad_lines=False)

    sorted_dataframe = sort_relevance(VECTORIZER, dataframe, keywords)
    ic(sorted_dataframe.head(10))

    list_of_dicts = []

    for entry in sorted_dataframe.head(10).iterrows():
        article_dict = {}
        ic(entry[1])
        article_dict["title"] = entry[1]["title"]
        article_dict["url"] = entry[1]["url"]
        article_dict["image_url"] = entry[1]["image_url"]
        article_dict["lastmod"] = entry[1]["lastmod"]
        list_of_dicts.append(article_dict)

    response = app.response_class(
        response=json.dumps(list_of_dicts),
        status=200,
        mimetype='application/json'
    )

    return response



if __name__ == "__main__":

    app.run(host=HOST, port=5000)

