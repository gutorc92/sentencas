# -*- coding: utf-8 -*-
import os
import codecs
import sys
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import metrics
from test.test_cut import getting_data_all, cut_data
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, auc
from test.test_figure import plot_roc_curve
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from settings import Settings
from datetime import datetime
from scipy import interp
from itertools import cycle
from test_figure import plot_confusion_matrix

def get_stop_words():
    stop_words_direito = ['impressao','artigo','direita', 'processo','sentenca','documento','digitalmente','direito', 'juiz','nao','autos','lauda','margem']
    stop_words_direito = stop_words_direito + stopwords.words("portuguese")
    return stop_words_direito

def target_encode(l_target):
    le = preprocessing.LabelEncoder()
    le.fit(np.unique(l_target))
    return le.transform(l_target)

if __name__ == "__main__":
    l_class, assuntos = getting_data_all()
    for cut in [100, 200, 300]:
        s = Settings()
        l_docs, l_target = cut_data(assuntos, cut)
        for i, d in enumerate(l_docs):
            if type(d) == list:
                l_docs[i] = ""
        for d in l_docs:
            if type(d) == list:
                print(d)

        l_target_en = target_encode(l_target)
        y = label_binarize(l_target_en, classes=np.unique(l_target_en))
        n_classes = y.shape[1]
        vectorizer = CountVectorizer(strip_accents="unicode", max_df =0.8, stop_words=get_stop_words())
        counts = vectorizer.fit_transform(l_docs)
        tfidf_transformer = TfidfTransformer().fit_transform(counts)
        random_state = np.random.RandomState(0)
        X_train, X_test, y_train, y_test = train_test_split(tfidf_transformer, y, test_size=0.33, random_state=42)
        #print(len(X_train), len(X_test), len(y_train), len(y_test))
        #naive
        classifier = OneVsRestClassifier(MultinomialNB())
        y_score = classifier.fit(X_train, y_train).predict_proba(X_test)
        y = classifier.predict(X_test)
        cnf_matrix = confusion_matrix(y_test, y)
        plot_confusion_matrix(cnf_matrix, classes=np.unique(y_score), normalize=True,
                              title='Confusion matrix, with normalization',algortim='Naive')
        #knn
        knn_classifier = OneVsRestClassifier(KNeighborsClassifier())
        y_score_knn = knn_classifier.fit(X_train, y_train).predict_proba(X_test)
        y_knn = classifier.predict(X_test)
        cnf_matrix_knn = confusion_matrix(y_test, y_knn)
        plot_confusion_matrix(cnf_matrix_knn, classes=np.unique(y_score_knn), normalize=True,
                              title='Confusion matrix, with normalization')

        fpr_knn = dict()
        tpr_knn = dict()
        roc_auc_knn = dict()
        for i in range(n_classes):
            fpr_knn[i], tpr_knn[i], _ = roc_curve(y_test[:, i], y_score_knn[:, i])
            roc_auc_knn[i] = auc(fpr_knn[i], tpr_knn[i])

        # Compute micro-average ROC curve and ROC area
        fpr_knn["micro"], tpr_knn["micro"], _ = roc_curve(y_test.ravel(), y_score_knn.ravel())
        roc_auc_knn["micro"] = auc(fpr_knn["micro"], tpr_knn["micro"])


        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        for i in range(n_classes):
            fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])

        # Compute micro-average ROC curve and ROC area
        fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
        plt.figure()
        lw = 2
        plt.plot(fpr[2], tpr[2], color='red',
                 lw=lw, label='ROC curve naive (area = %0.2f)' % roc_auc[2])
        plt.plot(fpr_knn[2], tpr_knn[2], color='darkorange',
                 lw=lw, label='ROC curve knn (area = %0.2f)' % roc_auc_knn[2])
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver operating characteristic example')
        plt.legend(loc="lower right")
        plt.savefig(s.join("figuras", 'resultado' + datetime.now().strftime("%d%m%Y_%H_%M_%S") + '.png'))
