# -*- coding: utf-8 -*-
import os
import codecs
import sys
sys.path.append('C:\\Users\\b15599226\\Documents\\sentencas\\test\\test_cut.py')
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import metrics
from test_cut import getting_data
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix


def get_stop_words():
    stop_words_direito = ['impressao','artigo','direita', 'processo','sentenca','documento','digitalmente','direito', 'juiz','nao','autos','lauda','margem']
    stop_words_direito = stop_words_direito + stopwords.words("portuguese")
    return stop_words_direito

def target_encode(l_target):
    le = preprocessing.LabelEncoder()
    le.fit(np.unique(l_target))
    return le.transform(l_target)

if __name__ == "__main__":
    dir_ = os.path.dirname(os.path.abspath(__file__))
    l_docs, l_target = getting_data()
    for i, d in enumerate(l_docs):
        if type(d) == list:
            l_docs[i] = ""
    for d in l_docs:
        if type(d) == list:
            print(d)
    l_target_en = target_encode(l_target)
    vectorizer = CountVectorizer(strip_accents="unicode", max_df =0.8, stop_words=get_stop_words())
    counts = vectorizer.fit_transform(l_docs)
    X_train, X_test, y_train, y_test = train_test_split(counts, l_target_en, test_size=0.33, random_state=42)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train)
    clf = KNeighborsClassifier().fit(X_train_tfidf, y_train)
    X_test_tfidf = tfidf_transformer.fit_transform(X_test)
    predicted = clf.predict(X_test_tfidf)
    r = metrics.classification_report(y_test, predicted, target_names=np.unique(l_target))
    with codecs.open(os.path.join(dir_, "..", "resultados", "report_knn.txt"), "w", "utf-8") as handle:
        handle.write(r)
    print(r)
    cnf_matrix = confusion_matrix(y_test, predicted)
    np.save(os.path.join(dir_, "confusion_matrix_knn"), cnf_matrix)
    np.save(os.path.join(dir_, "l_target_knn"), l_target)
