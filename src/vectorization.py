from nltk.corpus import stopwords
from time import time 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from sklearn import metrics

import pandas as pd

import pickle

VECTORIZER = TfidfVectorizer()
CLASSIFIER = None

STOPWORDS_SET = set(stopwords.words('english'))

STOPWORD_CUSTOM = []
# if we want to add more 

STOPWORD_CUSTOM_SET = set(STOPWORD_CUSTOM)

CLASSIFIER_FILE_NAME = "classifier.sav"

def remove_stopwords(article):

    # wrapping punctuation with spaces 

    article_modified = re.sub(r",", " , ", article)
    article_modified = re.sub(r"\.[^$]", " . ", article)
    article_modified = re.sub(r"\.$", " .", article)
    article_modified = re.sub(r"!$", " !", article)
    article_modified = re.sub(r"![^$]", " ! ", article)
    article_modified = re.sub(r"\?[^$]", " ? ", article)
    article_modified = re.sub(r"\?$", " ?", article)
    article_modified = re.sub(r"\;[^$]", " ? ", article)
    article_modified = re.sub(r"\;$", " ?", article)
    article_modified = re.sub(r"\:[^$]", " ? ", article)
    article_modified = re.sub(r"\:$", " ?", article)



    article_modied = re.sub(r"(\(|\)|\[|\]|\{|\})", r" \1 ", article)

    word_array = re.split(r"\s+", article_modied)

    article_return = ""

    for word in word_word_array:
        if (word not in STOPWORDS_SET) and (word not in STOPWORD_CUSTOM_SET):

            article_return += word 

    return article_return



train_set = None

test_set = None



def initialize_data():
    pass


INDEX_OF_ARTICLES_IN_CSV = 0
INDEX_OF_VERDICTS = 1



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

    train_articles = train_articles.apply(remove_stopwords)
    test_articles = test_articles.apply(remove_stopwords)

    # Vectorization will happen here
    train_vectorized = VECTORIZER.fit_transform(train_articles)
    test_vectorized = VECTORIZER.fit(test_articles)



def train():

    # This is assuming that all the vectorization has been done 
    global CLASSIFIER

    CLASSIFIER.fit(train_vectorized, train_verdicts)

def test():

    global CLASSIFIER

    test_predicted = CLASSIFIER.predict(test_vectorized)

    score = metrics.accuracy_score(test_vectorized, test_predicted)
    print("The accuracy: " + str(score))



def main(train_file, test_file, input_file):

    # Train file is supposed to have path of csv that should be used for training 
    # Test file is supposed to have path of test csv 
    # input_file is the file we actually want to predict shit for

    global train_set
    global test_set
    global CLASSIFIER

    try:
        # load the model if it already exists
        CLASSIFIER = pickle.load(open(CLASSIFIER_FILE_NAME, "rb"))

    except FileNotFoundError:
        CLASSIFIER = MultinomialNB()

        train_set = pd.read_csv(train_file)
        test_set = pd.read_csv(test_set)

        vectorize()
        train()
        test()
        pickle.dump(CLASSIFIER, open(CLASSIFIER_FILE_NAME, "wb"))

    input_set = pd.read_csv(input_set)
    # Assuming we only have the set of articles as text 

    input_set_vectorized = VECTORIZER.fit(input_set['0'])

    predictions = CLASSIFIER.predict(input_set_vectorized)

    for i in predictions:
        print(i)




