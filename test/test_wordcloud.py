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
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from sklearn.datasets import load_files

def get_stop_words():
    stop_words_direito = ['impressao','artigo','direita', 'processo','sentenca','documento','digitalmente','direito', 'juiz','nao','autos','lauda','margem']
    stop_words_direito = stop_words_direito + stopwords.words("portuguese")
    return stop_words_direito

def tdm(list_docs, list_files):
    vectorizer = CountVectorizer(strip_accents="unicode", max_df =0.8, stop_words=get_stop_words())
    x1 = vectorizer.fit_transform(list_docs)
    df = pd.DataFrame(x1.toarray().transpose(), index=vectorizer.get_feature_names())
    df.columns = list_files
    return df

def jdefault(o):
            return o.__dict__

if __name__ == "__main__":
    dir_ = os.path.dirname(os.path.abspath(__file__))
    files_names = os.listdir(dir_)
    files_names = [f for f in files_names if f.endswith(".json")]
    l_docs = []
    l_files = []
    for file_name in files_names:
        with codecs.open(os.path.join(dir_,"output.json"), "r","utf-8") as handle:
            text = handle.read()
        x = json.loads(text, object_hook=lambda d: create_process(d.keys(), d.values()))
        for p in x:
            if p.assunto == "Dívida Ativa":
                l_docs.append(p.abstract)
                l_files.append(p.npu_process)

    result = tdm(l_docs, l_files)
    print(result.shape)
    word_count = result.sum(1)
    total_words = word_count.sum(0)
    word_count2 = word_count / total_words
    wc = WordCloud(background_color="white", max_words=2000)
    wc.generate_from_frequencies(word_count2.to_dict())
    wc.to_file(dir_)