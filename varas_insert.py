# -*- coding: utf-8 -*-
import os
import codecs
import sys
import platform
import re
import requests as req
from bs4 import BeautifulSoup
from pages.scrapypage import ScrapyNrProcess
from settings import Settings
from networking import ProxedHTTPRequester
import json
from pymongo import MongoClient
from model.models import Varas


if __name__ == "__main__":
    dir_ = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir_,"test", "varas.txt")) as handle:
        text = handle.readlines()
    text = text[0].split(",")
    print(len(text))
    client = MongoClient('mongodb://localhost:27017/')
    db = client.process_database
    mvaras = db.varas
    for var1 in text:
        v = Varas(var1)
        varas_id = v.insert(mvaras)
        print(varas_id)
         
