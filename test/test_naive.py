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
from test_cut import getting_data_all, cut_data
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, auc
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
from sklearn.model_selection import cross_val_score
from test_figure import plot_confusion_matrix
s = Settings()

def get_stop_words():
    stop_words_direito = ['impressao','artigo','direita', 'processo','sentenca','documento','digitalmente','direito', 'juiz','nao','autos','lauda','margem']
    stop_words_direito = stop_words_direito + stopwords.words("portuguese")
    return stop_words_direito

def target_encode(l_target):
    le = preprocessing.LabelEncoder()
    le.fit(np.unique(l_target))
    return le.transform(l_target)

def best_knn(X_train, y_train):
    plt.figure()
    # creating odd list of K for KNN
    myList = list(range(1, 20))

    # subsetting just the odd ones
    neighbors = list(filter(lambda x: x % 2 != 0, myList))

    # empty list that will hold cv scores
    cv_scores = []

    # perform 10-fold cross validation
    for k in neighbors:
        knn = KNeighborsClassifier(n_neighbors=k)
        scores = cross_val_score(knn, X_train, y_train, cv=10, scoring='accuracy')
        cv_scores.append(scores.mean())

    # changing to misclassification error
    MSE = [1 - x for x in cv_scores]

    # determining best k
    optimal_k = neighbors[MSE.index(min(MSE))]
    print("The optimal number of neighbors is %d" % optimal_k)

    # plot misclassification error vs k
    plt.title('Número de K vizinhos por erro de classificação')
    plt.plot(neighbors, MSE)
    plt.xlabel('K vizinho')
    plt.ylabel('Error de classificação')
    plt.savefig(s.join("figuras", 'resultado_knn_optimal_' + datetime.now().strftime("%d%m%Y_%H_%M_%S") + '.png'))
    return optimal_k

def knn_confusion_matrix(X_train, X_test, y_train, y_test, l_target):
    best_k = best_knn(X_train, y_train)
    clf = KNeighborsClassifier(best_k).fit(X_train, y_train)
    predicted = clf.predict(X_test)
    cnf_matrix = confusion_matrix(y_test, predicted)
    plot_confusion_matrix(cnf_matrix, classes=np.unique(l_target), normalize=True, 
                      title='Matriz de confusão Knn normalizada', settings=s, algoritm='knn')
    return best_k

def naive_confusion_matrix(X_train, X_test, y_train, y_test, l_target):
    clf = MultinomialNB().fit(X_train, y_train)
    predicted = clf.predict(X_test)
    cnf_matrix = confusion_matrix(y_test, predicted)
    plot_confusion_matrix(cnf_matrix, classes=np.unique(l_target), normalize=True,
                      title='Matriz de confusão Naive Bayses', settings=s, algoritm='naive')

def write_classes(l_target_en, l_target):
    with codecs.open(s.join("lista", 'resultado_lista_' + datetime.now().strftime("%d%m%Y_%H_%M_%S") + '.csv'), 'w',
                     'utf-8') as handle:
        for code, classe_str in zip(l_target_en, l_target):
            handle.write("{}, {}\n".format(str(code), classe_str))

if __name__ == "__main__":
    cut_max = 300
    step = 100
    list_cut = list(range(step, cut_max+step, step))
    l_class, assuntos = getting_data_all(cut_max, attr='classe_process', del_keys=False)

    for cut in list_cut:
        l_docs, l_target = cut_data(assuntos, cut)
        for i, d in enumerate(l_docs):
            if type(d) == list:
                l_docs[i] = ""
        for d in l_docs:
            if type(d) == list:
                print(d)

        l_target_en = target_encode(l_target)
        write_classes(l_target_en, l_target)
        y = label_binarize(l_target_en, classes=np.unique(l_target_en))
        n_classes = y.shape[1]
        vectorizer = CountVectorizer(strip_accents="unicode", max_df =0.8, stop_words=get_stop_words())
        counts = vectorizer.fit_transform(l_docs)
        tfidf_transformer = TfidfTransformer().fit_transform(counts)
        random_state = np.random.RandomState(0)
        X_train, X_test, y_train, y_test, y_train_, y_test_ = train_test_split(tfidf_transformer, y, l_target_en, test_size=0.33, random_state=42)
        #print(len(X_train), len(X_test), len(y_train), len(y_test))
        best_k = knn_confusion_matrix(X_train, X_test, y_train_, y_test_, l_target)
        naive_confusion_matrix(X_train, X_test, y_train_, y_test_, l_target)
        #naive
        classifier = OneVsRestClassifier(MultinomialNB())
        y_score = classifier.fit(X_train, y_train).predict_proba(X_test)
        #knn
        knn_classifier = OneVsRestClassifier(KNeighborsClassifier(best_k))
        y_score_knn = knn_classifier.fit(X_train, y_train).predict_proba(X_test)
        y_knn = classifier.predict(X_test)

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
        plt.xlabel('Falso Positivos')
        plt.ylabel('Verdadeiros Positivos')
        plt.title('ROC curves')
        plt.legend(loc="lower right")
        plt.savefig(s.join("figuras", 'resultado_roc_curve_' + datetime.now().strftime("%d%m%Y_%H_%M_%S") + '.png'))
