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
    client = MongoClient('mongodb://localhost:27017/')
    db = client.process_database
    mprocesses = db.processes
    dir_ = os.path.dirname(os.path.abspath(__file__))
    processes_id = mprocesses.insert_one({'npu_process': '4654654654'}).inserted_id
    print(processes_id)
    with codecs.open(os.path.join(dir_,"output.json"), "r","utf-8") as handle:
        text = handle.read()


    
    x = json.loads(text, object_hook=lambda d: create_process(d.keys(), d.values()))
    for p in x:
        #print(type(p), p)
        processes_id = mprocesses.insert_one(p.__dict__).inserted_id
        print(processes_id)
