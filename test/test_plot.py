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
from test.test_cut import getting_data_subject
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
    size = 10
    assuntos = getting_data_subject('classe_process')
    keys = []
    values = []
    for k, v in sorted(assuntos.items(), key=lambda x: x[0][0]):
        if v['valor'] > 10:
            keys.append(k)
            values.append(v['valor'])
    print(len(keys), len(values))
    classes = np.array([c for c in keys])
    plt.figure(figsize=(size, size))
    tick_marks = np.arange(len(classes))
    plt.scatter(tick_marks, values)
    plt.xticks(tick_marks, classes, rotation=90)
    plt.ylabel('Quantidade')
    plt.xlabel('Classe')
    plt.show()
    plt.savefig(s.join("figuras",  'resultado' + datetime.now().strftime("%d%m%Y_%H_%M_%S")+'.png'))
