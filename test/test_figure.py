# -*- coding: utf-8 -*-
import os
import re
import codecs
from settings import Settings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import itertools
from datetime import datetime


def plot_roc_curve(fpr_rt_lm, tpr_rt_lm):
    s = Settings()
    plt.figure(1)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.plot(fpr_rt_lm, tpr_rt_lm, label='RT + LR')
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve')
    plt.legend(loc='best')
    plt.savefig(s.join("figuras", 'resultado' + datetime.now().strftime("%d%m%Y_%H_%M_%S") + '.png'))


def plot_confusion_matrix(cm, classes, settings,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues,
                          algoritm='knn'):
    size = 10
    plt.figure(figsize=(size, size))
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    #print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    classes = np.array([ c[0:5] for c in classes ])
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig(settings.join("figuras", 'resultado_confusion_' + algoritm + "_" + datetime.now().strftime("%d%m%Y_%H_%M_%S") + '.png'))

if __name__ == "__main__":
    size = 10
    dir_ = os.path.dirname(os.path.abspath(__file__))
    cnf_matrix = np.load(os.path.join(dir_, "confusion_matrix_svc.npy"))
    l_target = np.load(os.path.join(dir_, "l_target_svc.npy"))
    plt.figure(figsize=(size, size))
    plot_confusion_matrix(cnf_matrix, classes=np.unique(l_target), normalize=True, 
                      title='Confusion matrix, with normalization')

