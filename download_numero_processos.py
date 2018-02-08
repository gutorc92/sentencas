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
from pages.scrapypage import ScrapyNrProcess


class Extract_Numbers:

    def __init__(self, pagInit, pagEnd,session, url):
        self.arquivo = None
        self.s = Settings()
        self.create_log_()
        self.pagInit = 1 if pagInit == 0 else pagInit
        self.pagEnd = pagEnd
        self.session = session
        self.url = url
        self.total = 0


    def create_log_(self):
        name = "log_extract_numbers_" + datetime.now().strftime("%d%m%Y_%H_%M")
        self.log_file = "log_extract_numbers_" + datetime.now().strftime("%d%m%Y_%H_%M") + ".txt"
        self.logger = self.s.createLogFile(name, self.log_file)

    def save_processos(self, names):
        arquivo = "resultado_" + datetime.now().strftime("%d%m%Y_%H_%M") + ".txt"
        self.logger.info("Quantidade de registros %d" % len(names))
        with open(os.path.join(self.s.path, "numero_processos", arquivo), "a") as f:
            for n in names:
                f.write(n)
                f.write("\n")

    def download(self):
        start = datetime.now()
        response = self.session.get(self.url)
        if response.status_code != req.codes.ok:
            self.logger.info("A url inicial nao pode se encontrada para a thread: %s", str(self.id))
            return 1

        scrapyprocesses = ScrapyNrProcess(self.session, self.logger)
        all_processes = set()
        for i in range(self.pagInit, self.pagEnd):
            processes = scrapyprocesses.download_page(i)
            all_processes = all_processes.union(processes)
        self.save_processos(all_processes)
        self.total += len(all_processes)
        end = datetime.now()
        print("Demorou {}s para fazer download das paginas".format((end - start).total_seconds()))
