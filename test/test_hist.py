# -*- coding: utf-8 -*-
import os
import codecs
import sys
import re
from settings import Settings
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from test_cut import getting_data_subject
from settings import Settings


def plot_subject_distribution(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):


    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    classes = np.array([ c[0:5] for c in classes ])
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90)
    plt.yticks(tick_marks, classes)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

if __name__ == "__main__":
    s = Settings()
    size = 11
    assuntos = getting_data_subject()
    keys = []
    values = []
    for k, v in assuntos.items():
        if v['valor'] < 2000:
            keys.append(k)
            values.append(v['valor'])
    print(len(keys), len(values))
    plt.hist(values, bins=20, range=(0,2000))
    plt.ylabel('Quantidade')
    plt.xlabel('Classe')
    plt.show()
    plt.savefig(s.join("figuras",  'resultado' + datetime.now().strftime("%d%m%Y_%H_%M_%S")+'.png'))
