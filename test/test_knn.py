# -*- coding: utf-8 -*-
import os
import codecs
import sys
import platform
import re
import requests as req
from bs4 import BeautifulSoup
from pages.scrapypage import ScrapyNrProcess
from settings import Settings
from networking import ProxedHTTPRequester
import json
from collections import namedtuple
from model.models import Process, create_process
import pymongo
from pymongo import MongoClient
import os
import re
import codecs
from settings import Settings
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from wordcloud import WordCloud
from nltk.corpus import stopwords
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import metrics
from test.test_cut import getting_data

def get_stop_words():
    stop_words_direito = ['impressao','artigo','direita', 'processo','sentenca','documento','digitalmente','direito', 'juiz','nao','autos','lauda','margem']
    stop_words_direito = stop_words_direito + stopwords.words("portuguese")
    return stop_words_direito

def target_encode(l_target):
    le = preprocessing.LabelEncoder()
    le.fit(np.unique(l_target))
    return le.transform(l_target)

if __name__ == "__main__":
    l_docs, l_target = getting_data()
    l_target_en = target_encode(l_target)
    vectorizer = CountVectorizer(strip_accents="unicode", max_df =0.8, stop_words=get_stop_words())
    counts = vectorizer.fit_transform(l_docs)
    X_train, X_test, y_train, y_test = train_test_split(counts, l_target_en, test_size=0.33, random_state=42)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train)
    clf = MultinomialNB().fit(X_train_tfidf, y_train)
    X_test_tfidf = tfidf_transformer.fit_transform(X_test)
    predicted = clf.predict(X_test_tfidf)
    print(metrics.classification_report(y_test, predicted, target_names=np.unique(l_target)))
