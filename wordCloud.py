import os
import re
import codecs
from settings import Settings
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from wordcloud import WordCloud

def readText(file_name, s):
        text = ""
        with codecs.open(os.path.join(s.path, "textos", file_name), "r", "UTF-8") as handle:
           for line in handle.readlines():
               text += " " + line
        line = re.sub("\s+", " ", text)
        return text

def tdm():
    s = Settings()
    vectorizer = CountVectorizer(strip_accents="unicode", max_df =0.8)
    list_files = os.listdir(os.path.join(s.path, "textos"))
    list_docs = [readText(x, s) for x in list_files]
    x1 = vectorizer.fit_transform(list_docs)
    # create dataFrame
    print()
    df = pd.DataFrame(x1.toarray().transpose(), index=vectorizer.get_feature_names())
    df.columns = list_files
    return df

if __name__ == "__main__":
    p = tdm()
    wc = WordCloud(background_color="white", max_words=2000)
    print(p.sum(0))

