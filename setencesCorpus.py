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
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import lda


class ReadSentences(object):

    def __init__(self):
        self.s = Settings()
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

    def readText(self, file):
        text = ""
        with codecs.open(os.path.join(self.s.path, "leis", file), "r", "UTF-8") as handle:
           for line in handle.readlines():
               line = line.rstrip().lower()
               line = re.sub("[0-9]+", "", line)
               line = re.sub("[_]+", "", line)
               text += " " + line
        line = re.sub("\s+", " ", text)
        return text

    def tdm(self):
        vectorizer = CountVectorizer(strip_accents="unicode", max_df =0.8)
        list_files = os.listdir(os.path.join(self.s.path, "leis"))
        list_docs = [self.readText(x) for x in list_files]
        x1 = vectorizer.fit_transform(list_docs)
        # create dataFrame
        print()
        df = pd.DataFrame(x1.toarray().transpose(), index=vectorizer.get_feature_names())
        df.columns = list_files
        return df

    def stop_words(self):
        ponctuation = [".", "!", "-", "?", ",", "lei", "artigo", ")", "(", "subchefia", ":", "presidente", "$", "°"]
        ponctuation.append(stopwords.words("portuguese"))
        return ponctuation

    def tokenizer(self):
        # portuguese_sent_tokenizer = nltk.data.load("tokenizers/punkt/portuguese.pickle")
        tokens = nltk.word_tokenize(self.readText())
        print(len(tokens))
        # nltk_text = nltk.Text(tokens)
        # print(type(nltk_text))
        fd1 = nltk.FreqDist(tokens)
        for f in fd1:
            print(f, fd1[f])

    def read(self):
        portuguese_sent_tokenizer = nltk.data.load("tokenizers/punkt/portuguese.pickle")
        newcorpus = PlaintextCorpusReader(os.path.join(self.s.path, "leis"), ".*", sent_tokenizer=portuguese_sent_tokenizer)
        ponctuation = [".","!","-","?",",","lei","artigo",")","(","subchefia",":","presidente","$", "°"]
        #print(newcorpus.words())
        for files in newcorpus.fileids():
            words = newcorpus.words(files)
            words = [w.lower() for w in words]
            filtered_words = [word for word in words if word not in stopwords.words("portuguese")]
            filtered_words = [word for word in filtered_words if word not in ponctuation]
            fd1 = nltk.FreqDist(filtered_words)
            print(files, fd1.most_common(10))


if __name__ == "__main__":
    r = ReadSentences()
    p = r.tdm()
    print(p.shape)
    vocab = p.index.values
    print(vocab[2:20])
    p.reset_index(drop=True)
    model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
    model.fit(p.as_matrix())
    topic_word = model.topic_word_
    n_top_words = 8
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    #p.to_csv(os.path.join(r.s.path, "tabela2.csv"))

    #print(stopwords.words("portuguese"))
