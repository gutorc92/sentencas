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
    varas = Varas.all() 
    session = ProxedHTTPRequester()
    settings = Settings()
    client = MongoClient('mongodb://localhost:27017/')
    db = client.process_database
    mprocesses = db.processes
    ex = ScrapyNrProcess(session, settings.createLogFile("log_extracted_numbers__varas_"))
    for var1 in varas:
        response = session.get(var1.get_url())
        if response.status_code == req.codes.ok:
            print("Deu certo")
            page = BeautifulSoup(response.content, "html.parser")
            resultados = page.find('div', {'id': 'resultados'})
            if resultados is not None:
                nr_results = number_of_results(resultados)
                all_processes = []
                for x in range(1, nr_results):
                    all_processes = all_processes + ex.download_page(x)

                for p in all_processes: 
                    processes_id = mprocesses.insert_one(p.__dict__).inserted_id
                    print(processes_id)
                 
                
