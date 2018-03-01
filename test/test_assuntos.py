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
from collections import namedtuple
from model.models import Process, create_process
import pymongo
from pymongo import MongoClient

def jdefault(o):
            return o.__dict__

if __name__ == "__main__":
    dir_ = os.path.dirname(os.path.abspath(__file__))
    files_names = os.listdir(dir_)
    files_names = [f for f in files_names if f.endswith(".json")]
    assuntos = {}
    for file_name in files_names:
        print("Processing", file_name)
        with codecs.open(os.path.join(dir_,file_name), "r","utf-8") as handle:
            text = handle.read()
        x = json.loads(text, object_hook=lambda d: create_process(d.keys(), d.values()))
        for p in x:
            assunto = p.assunto.strip()
            if assunto in assuntos:
                assuntos[assunto] += 1
            else:
                assuntos[assunto] = 1

    for k, v in sorted(assuntos.items(), key=lambda x: x[1], reverse=True):
        if v > 300:
            print(k, v)

