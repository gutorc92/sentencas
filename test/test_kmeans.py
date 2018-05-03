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
from test_cut import getting_data_all, cut_data, getting_data_subject
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
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
s = Settings()

def get_stop_words():
    stop_words_direito = ['impressao','artigo','direita', 'processo','sentenca','documento','digitalmente','direito', 'juiz','nao','autos','lauda','margem']
    stop_words_direito = stop_words_direito + stopwords.words("portuguese")
    return stop_words_direito

def target_encode(l_target):
    le = preprocessing.LabelEncoder()
    le.fit(np.unique(l_target))
    return le.transform(l_target)

if __name__ == "__main__":
    assuntos = getting_data_subject(attr='classe_process')
    l_docs, l_target = cut_data(assuntos, -1)
    vectorizer = CountVectorizer(strip_accents="unicode", max_df=0.8, stop_words=get_stop_words())
    counts = vectorizer.fit_transform(l_docs)
    tfidf_transformer = TfidfTransformer().fit_transform(counts)
    l_target_en = target_encode(l_target)
    centers = [[1, 1], [-1, -1], [1, -1]]

    X = StandardScaler().fit_transform(tfidf_transformer.todense())

    # #############################################################################
    # Compute DBSCAN
    db = DBSCAN(eps=0.3, min_samples=10).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)
    print("Homogeneity: %0.3f" % metrics.homogeneity_score(l_target_en, labels))
    print("Completeness: %0.3f" % metrics.completeness_score(l_target_en, labels))
    print("V-measure: %0.3f" % metrics.v_measure_score(l_target_en, labels))
    print("Adjusted Rand Index: %0.3f"
          % metrics.adjusted_rand_score(l_target_en, labels))
    print("Adjusted Mutual Information: %0.3f"
          % metrics.adjusted_mutual_info_score(l_target_en, labels))
    print("Silhouette Coefficient: %0.3f"
          % metrics.silhouette_score(X, labels))

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each)
              for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.savefig(s.join("figuras", 'resultado_kmeans_' + datetime.now().strftime("%d%m%Y_%H_%M_%S") + '.png'))
