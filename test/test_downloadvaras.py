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
    dir_ = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(dir_,"./varas.txt")) as handle:
        text = handle.readlines()
    text = text[0].split(",")
    print(len(text))
    url_begin = "http://esaj.tjsp.jus.br/cjpg/pesquisar.do?conversationId=&dadosConsulta.pesquisaLivre=&tipoNumero=UNIFICADO&numeroDigitoAnoUnificado=&foroNumeroUnificado=&dadosConsulta.nuProcesso=&dadosConsulta.nuProcessoAntigo=&classeTreeSelection.values=&classeTreeSelection.text=&assuntoTreeSelection.values=&assuntoTreeSelection.text=&agenteSelectedEntitiesList=&contadoragente=0&contadorMaioragente=0&cdAgente=&nmAgente=&dadosConsulta.dtInicio=&dadosConsulta.dtFim=&varasTreeSelection.values="
    url_end = "&varasTreeSelection.text=2+Registros+selecionados&dadosConsulta.ordenacao=DESC"
    #for var1, var2 in zip(text[0:997], text[997:]):
    session = ProxedHTTPRequester()
    settings = Settings()
    ex = ScrapyNrProcess(session, settings.createLogFile("log_extracted_numbers__varas_"))
    for var1 in text:
        url_t = url_begin + var1 + url_end
        response = session.get(url_t)
        if response.status_code == req.codes.ok:
            print("Deu certo")
            page = BeautifulSoup(response.content, "html.parser")
            resultados = page.find('div', {'id': 'resultados'})
            if resultados is not None:
                nr_results = number_of_results(resultados)
                all_processes = []
                for x in range(1, nr_results):
                    all_processes = all_processes + ex.download_page(x)

                serialized = json.dumps(all_processes, indent=4, default=jdefault,ensure_ascii=False )
                with codecs.open(os.path.join(dir_, "output.json"), "w", "utf-8") as handle:
                    handle.write(serialized)
                break
