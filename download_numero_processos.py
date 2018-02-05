import requests as req
import logging
import os
from datetime import datetime
from bs4 import BeautifulSoup
from settings import Settings
import threading
from downloadsentences import DownloadSetence
import platform
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class Extract_Numbers:

    def __init__(self, pagInit, pagEnd,session,url, num = 0):
        self.arquivo = None
        self.s = Settings()
        self.create_log_()
        self.pagInit = 1 if pagInit == 0 else pagInit
        self.pagEnd = pagEnd
        self.num = num
        self.arquivos = []
        self.session = session
        self.url = url
        self.total = 0


    def create_log_(self):
        name = "log_extract_numbers_" + datetime.now().strftime("%d%m%Y_%H_%M")
        self.log_file = "log_extract_numbers_" + datetime.now().strftime("%d%m%Y_%H_%M") + ".txt"
        self.logger = self.s.createLogFile(name, self.log_file)

    def extrai_numero_processo(self, response):
        page = BeautifulSoup(response.content, "html.parser")
        div = page.find("div", {"id": "divDadosResultado"})
        if div is None:
            self.logger.info("Nao encontrou a div de dados")
            print(page)
            return 0

        as_tag = div.find_all("a")
        if as_tag is None:
            self.logger.info("Não encontrou links")
            return None
        names = set()
        for a in as_tag:
            names.add(a["name"])
        self.save_processos(names)

    def save_processos(self, names):
        if self.num + len(names) < 10000 and self.arquivo is not None:
            arquivo = self.arquivo 
        else:
            arquivo = "resultado_"  + datetime.now().strftime("%d%m%Y_%H_%M") + ".txt"
            print(arquivo)
            self.arquivo = arquivo
            self.arquivos.append(self.arquivo)
            self.num = 0
        self.logger.info("Quantidade de registros %d" % len(names))
        with open(os.path.join(self.s.path, "numero_processos", arquivo), "a") as f:
            for n in names:
                f.write(n)
                f.write("\n")
        self.num += len(names)
        self.total += len(names)

    def download(self):
        start = datetime.now()
        response = self.session.get(self.url)
        if response.status_code != req.codes.ok:
            self.logger.info("A url inicial nao pode se encontrada para a thread: %s", str(self.id))
            return 1

        self.extrai_numero_processo(response)
        for i in range(self.pagInit, self.pagEnd):
            url_t = "http://esaj.tjsp.jus.br/cjpg/trocarDePagina.do?pagina=" + str(i) + "&conversationId="
            self.logger.info("Pagina %s", str(i))
            response = self.session.get(url_t)
            if response.status_code == req.codes.ok:
                self.extrai_numero_processo(response)
            else:
                self.logger.info("A url nao pode ser encontrada: %s", str(url_t))
        end = datetime.now()
        print("Demorou {}s para fazer download das paginas".format((end - start).total_seconds()))
