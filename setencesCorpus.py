# -*- coding: utf-8 -*-
import os
import logging
import codecs
import re
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import PlaintextCorpusReader
from settings import Settings
from datetime import datetime


class ReadSentences(object):

    def __init__(self):
        self.s = Settings()
        self.s.extract_settings()
        self.createLog()

    def createLog(self):
        log_file = "log" + datetime.now().strftime("%d%m%Y_%M_%H")
        self.log_file = os.path.join(self.s.path, "log", log_file)
        logging.basicConfig(filename=self.log_file, format='%(levelname)s:%(message)s', level=logging.INFO)

    def getJudge(self, text):
        judge = ""
        pattern = re.compile(r"Este documento é cópia do original, assinado digitalmente por ([A-Z ]*), liberado nos autos em", re.MULTILINE)
        for match in pattern.finditer(text):
            match_return = match.groups()
            print(match_return[0])
            judge = match_return[0]
        return judge

    def readText(self):
        text = ""
        with codecs.open(os.path.join(self.s.path, "textos", "0A0012HV50000_10_PG5REG_73823129.txt"), "r", "UTF-8") as handle:
           text = handle.read()

        #print(text)
        judge = self.getJudge(text)
        print("Judge", judge)
        portuguese_sent_tokenizer = nltk.data.load("tokenizers/punkt/portuguese.pickle")
        tokens = portuguese_sent_tokenizer.tokenize(text)
        print(len(tokens))
        nltk_text = nltk.Text(tokens)
        print(type(nltk_text))
        fd1 = nltk.FreqDist(tokens)
        print(fd1["cumprimento"])

    def read(self):
        portuguese_sent_tokenizer = nltk.data.load("tokenizers/punkt/portuguese.pickle")
        newcorpus = PlaintextCorpusReader(os.path.join(self.s.path, "textos"), ".*", sent_tokenizer=portuguese_sent_tokenizer)
        print(newcorpus.words())
        words = newcorpus.words()
        words = [w.lower() for w in words]
        fd1 = nltk.FreqDist(newcorpus.words())
        filtered_words = [word for word in words if word not in stopwords.words('english')]
        for word in filtered_words:
            print(fd1[word])

if __name__ == "__main__":
    r = ReadSentences()
    r.read()
    #print(stopwords.words("portuguese"))

