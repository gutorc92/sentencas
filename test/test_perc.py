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
from matplotlib import mlab
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

if __name__ == "__main__":
    plt.figure()
    assuntos = getting_data_subject(attr='classe_process')
    values = []
    for k, v in assuntos.items():
        if 'valor' in v:
            values.append(v['valor'])
    #d = np.sort(np.random.randint(0, 1000, 1000)).cumsum()
    d = sorted(values)
    print(d)

    # Percentile values
    p = np.array([0.0, 25.0, 50.0, 75.0, 100.0])

    perc = mlab.prctile(d, p=p)

    plt.plot(d)
    # Place red dots on the percentiles
    plt.plot((len(d) - 1) * p / 100., perc, 'ro')

    # Set tick locations and labels
    plt.xticks((len(d) - 1) * p / 100., map(str, p))

    plt.savefig(s.join("figuras", 'resultado_perc_' + datetime.now().strftime("%d%m%Y_%H_%M_%S") + '.png'))