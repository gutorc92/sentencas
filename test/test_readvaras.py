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
    client = MongoClient('mongodb://localhost:27017/')
    db = client.process_database
    mvaras = db.varas
    all_v = Varas.all(mvaras) 
    for v in all_v:
        print(v)
