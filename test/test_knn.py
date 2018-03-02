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

def get_stop_words():
    stop_words_direito = ['impressao','artigo','direita', 'processo','sentenca','documento','digitalmente','direito', 'juiz','nao','autos','lauda','margem']
    stop_words_direito = stop_words_direito + stopwords.words("portuguese")
    return stop_words_direito

def target_encode(l_target):
    le = preprocessing.LabelEncoder()
    le.fit(np.unique(l_target))
    return le.transform(l_target)

def jdefault(o):
            return o.__dict__

def getting_data():
    dir_ = os.path.dirname(os.path.abspath(__file__))
    files_names = os.listdir(dir_)
    files_names = [f for f in files_names if f.endswith(".json")]
    l_docs = []
    l_files = []
    l_target = []
    for file_name in files_names:
        print(file_name)
        with codecs.open(os.path.join(dir_,file_name), "r","utf-8") as handle:
            text = handle.read()
        x = json.loads(text, object_hook=lambda d: create_process(d.keys(), d.values()))
        for p in x:
            #print(p.assunto)
            l_docs.append(p.abstract)
            l_files.append(p.npu_process)
            l_target.append(p.assunto.strip())
    return l_docs, l_files, l_target

if __name__ == "__main__":
    l_docs, l_target = getting_data()
    l_target_en = target_encode(l_target)
    X_train, X_test, y_train, y_test = train_test_split(l_docs, l_target_en, test_size=0.33, random_state=42)
    print(len(l_docs), len(l_files))
    vectorizer = CountVectorizer(strip_accents="unicode", max_df =0.8, stop_words=get_stop_words())
    X_train_counts = vectorizer.fit_transform(X_train)
    print(X_train_counts.shape)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clf = MultinomialNB().fit(X_train_tfidf, y_train)
    X_test_counts = vectorizer.fit_transform(X_test)
    X_test_tfidf = tfidf_transformer.fit_transform(X_test_counts)
    predicted = clf.predict(X_test_tfidf)
    print(metrics.classification_report(y_test, predicted, target_names=np.unique(l_target)))
