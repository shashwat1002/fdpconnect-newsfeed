from nltk.corpus import stopwords
from time import time 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from icecream import ic

import re

from sklearn import metrics

import pandas as pd

import sys

import pickle

CLASSIFIER = None

STOPWORDS_SET = set(stopwords.words('english'))

STOPWORD_CUSTOM = []
# if we want to add more

STOPWORD_CUSTOM_SET = set(STOPWORD_CUSTOM)

VECTORIZER = TfidfVectorizer(stop_words=set(stopwords.words("english")).union(STOPWORD_CUSTOM_SET))

CLASSIFIER_FILE_NAME = "classifier.sav"
VECTORIZER_FILE_NAME = "vectorizer.sav"



INDEX_OF_ARTICLES_IN_CSV = 'article'
INDEX_OF_VERDICTS = 'verdict'


train_set = None

test_set = None
train_articles = None
train_verdicts = None

test_articles = None 
train_articles = None


def initialize_data():
    global train_articles
    global test_articles
    global train_verdicts
    global test_verdicts

    train_articles = train_set[''+str(INDEX_OF_ARTICLES_IN_CSV)]
    train_verdicts = train_set[''+str(INDEX_OF_VERDICTS)]

    test_articles = test_set[''+str(INDEX_OF_ARTICLES_IN_CSV)]
    test_verdicts = test_set[''+str(INDEX_OF_VERDICTS)]





train_vectorized = None
test_vectorized = None


def vectorize():

    # Removing stopwords from articles in both test set and the train set 
    global train_articles
    global test_articles
    global train_vectorized
    global test_vectorized


    # Vectorization will happen here
    train_vectorized = VECTORIZER.fit_transform(train_articles)
    test_vectorized = VECTORIZER.transform(test_articles)



def train():

    # This is assuming that all the vectorization has been done 
    global CLASSIFIER

    CLASSIFIER.fit(train_vectorized, train_verdicts)

def test():

    global CLASSIFIER

    test_predicted = CLASSIFIER.predict(test_vectorized)

    score = metrics.accuracy_score(test_verdicts, test_predicted)
    print("The accuracy: " + str(score))



def main(train_file, test_file, input_file):

    # Train file is supposed to have path of csv that should be used for training 
    # Test file is supposed to have path of test csv 
    # input_file is the file we actually want to predict shit for

    global train_set
    global test_set
    global CLASSIFIER
    global VECTORIZER

    try:
        # load the model if it already exists
        CLASSIFIER = pickle.load(open(CLASSIFIER_FILE_NAME, "rb"))
        VECTORIZER = pickle.load(open(VECTORIZER_FILE_NAME, "rb"))

        article = input()
        vectorized = VECTORIZER.transform([article])
        prediction = CLASSIFIER.predict(vectorized)
        print(prediction)

    except FileNotFoundError:
        CLASSIFIER = MultinomialNB()

        train_set = pd.read_csv(train_file, engine="python", error_bad_lines=False)
        test_set = pd.read_csv(test_file, engine="python", error_bad_lines=False)

        initialize_data()

        vectorize()
        train()
        test()

        # save model and the vectorizer 
        pickle.dump(CLASSIFIER, open(CLASSIFIER_FILE_NAME, "wb"))
        pickle.dump(VECTORIZER, open(VECTORIZER_FILE_NAME, "wb"))


    # input_set = pd.read_csv(input_set)
    # # Assuming we only have the set of articles as text 

    # input_set_vectorized = VECTORIZER.fit(input_set['0'])

    # predictions = CLASSIFIER.predict(input_set_vectorized)

    # for i in predictions:
    #     print(i)


main(sys.argv[1], sys.argv[2], sys.argv[3])


def classify_articles_set(classifier, vectorizer, articles):

    vectorized_matrix = vectorizer(articles)
    predictions = classifier(vectorized_matrix)

    return predictions

def generate_vectors_tokens(vectorizer, tokens):

    return vectorizer(tokens)