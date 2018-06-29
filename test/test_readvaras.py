# -*- coding: utf-8 -*-
import os
import codecs
import sys
import platform
import re
import requests as req
from bs4 import BeautifulSoup
from settings import Settings
import json
from pymongo import MongoClient
from model.models import Varas, Mongo
 

if __name__ == "__main__":
    m = Mongo()
    all_v = Varas.all(m.get_varas())
    print("quandidade de varas restantes", len(all_v))
    for v in all_v:
        print(v)

    #print(all_v[0].nr_code)
    #all_v[0].done = True
    #all_v[0].update
