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
from model.models import Varas, Mongo
from test_google_api import upload_file

def number_of_results(div_resultaos):
    table = div_resultaos.find('table')
    # table_body = table.find('tbody')
    if table is not None:
        data = []
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        str_r = data[0][0]
        str_r2 = re.sub('[\\n\\t]', ' ', str_r)
        str_r2 = re.sub(' +', ' ', str_r2)
        r = re.match("Resultados (\d+) a (\d+) de (\d+)", str_r2)
        if r is not None:
            return int(r.group(3))
        else:
            return 1
    else:
        return 1

def jdefault(o):
            return o.__dict__ 

if __name__ == "__main__":
    session = ProxedHTTPRequester()
    settings = Settings()
    mongo = Mongo()
    varas = Varas.all(mongo.get_varas()) 
    ex = ScrapyNrProcess(session, settings.createLogFile("log_extracted_numbers__varas_"))
    for var1 in varas:
        print(var1.nr_code)
        response = session.get(var1.get_url())
        if response.status_code == req.codes.ok:
            print("Deu certo")
            all_processes = []
            for x in range(1, var1.qtde):
                all_processes = all_processes + ex.download_page(x)

            serialized = json.dumps(all_processes, indent=4, default=jdefault,ensure_ascii=False )
            dir_path = settings.join('jsons')
            file_name = "output_" + var1.nr_code + ".json"
            with codecs.open(os.path.join(dir_path, file_name), "w", "utf-8") as handle:
                handle.write(serialized)
            upload_file(dir_path, file_name)
            var1.done = True
            var1.update(mongo.get_varas())
