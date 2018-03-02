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
    assuntos = {}
    for file_name in files_names:
        print(file_name)
        with codecs.open(os.path.join(dir_,file_name), "r","utf-8") as handle:
            text = handle.read()
        x = json.loads(text, object_hook=lambda d: create_process(d.keys(), d.values()))
        for p in x:
            #print(p.assunto)
            assunto = p.assunto.strip()
            if assunto in assuntos:
                assuntos[assunto]['valor'] += 1
                assuntos[assunto]['list_docs'].append(p.abstract)
                assuntos[assunto]['list_target'].append(assunto)
            else:
                assuntos[assunto] = {}
                assuntos[assunto]['valor'] = 1
                assuntos[assunto]['list_docs'] = [p.abstract]
                assuntos[assunto]['list_target'] = [assunto]
    l_docs = []
    l_target = []
    i = 0
    for k, v in sorted(assuntos.items(), key=lambda x: x[0][0], reverse=True):
        if v['valor'] > 600:
            i += 1
            l_docs = l_docs + v['list_docs']
            l_target = l_target + v['list_target']
            print(k, v['valor'])
    print(i)
    return l_docs, l_target

if __name__ == "__main__":
    getting_data() 
