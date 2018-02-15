# -*- coding: utf-8 -*-
import os
import sys
import platform
import requests as req
from bs4 import BeautifulSoup

if __name__ == "__main__":
    with open("varas.txt") as handle:
        text = handle.readlines()
    text = text[0].split(",")
    print(len(text))
    url_begin = "http://esaj.tjsp.jus.br/cjpg/pesquisar.do?conversationId=&dadosConsulta.pesquisaLivre=&tipoNumero=UNIFICADO&numeroDigitoAnoUnificado=&foroNumeroUnificado=&dadosConsulta.nuProcesso=&dadosConsulta.nuProcessoAntigo=&classeTreeSelection.values=&classeTreeSelection.text=&assuntoTreeSelection.values=&assuntoTreeSelection.text=&agenteSelectedEntitiesList=&contadoragente=0&contadorMaioragente=0&cdAgente=&nmAgente=&dadosConsulta.dtInicio=&dadosConsulta.dtFim=&varasTreeSelection.values="
    url_end = "&varasTreeSelection.text=2+Registros+selecionados&dadosConsulta.ordenacao=DESC"
    for var1, var2 in zip(text[0:997], text[997:]):
        print(var1, var2)
        url_t = url_begin + var1 + "%2C" + var2 + url_end
        print(url_t)
        response = req.get(url_t)
        if response.status_code == req.codes.ok:
            print("Deu certo")
            page = BeautifulSoup(response.content, "html.parser")
            resultados = page.find('div', {'id': 'resultados'})
            if resultados is not None:
                table = resultados.find('table')
                #table_body = table.find('tbody')
                data = []
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    data.append([ele for ele in cols if ele])
                print(data[0])