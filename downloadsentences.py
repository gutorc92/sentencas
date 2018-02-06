# -*- coding: utf-8 -*-
import os
import logging
import time
import platform
import codecs
from settings import Settings
from scrapypage import ScrapySentence
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DownloadSetence(object):

    def __init__(self, webDriver, processNumbers, debug=False):
        self.s = Settings()
        self.driver = webDriver
        self.create_log_file()
        self.processNumbers = processNumbers
        self.debug = debug
        self.scrapysentence = ScrapySentence(webDriver, debug)

    def create_log_file(self):
        log_file = "log_" + datetime.now().strftime("%d%m%Y_%H_%M")
        self.log_file = os.path.join(self.s.path, "log", log_file)
        logging.basicConfig(filename=self.log_file, format='%(levelname)s:%(message)s', level=logging.INFO)

    def create_estatisca_file(self):
        estatistica_file = "sentences" + datetime.now().strftime("%d%m%Y_%M_%H")
        estatistica_file = os.path.join(self.s.path, "estatistica", estatistica_file)
        estatistica_file = ".".join([estatistica_file, "csv"])
        return estatistica_file


    def file_name(self, processo):
        return processo.replace("-","_").replace("\n","")

    def processo_name(self, processo):
        return processo.replace("_","-")

    def complete_file_name(self, processo):
        return self.get_file_path("textos",".".join([self.file_name(processo), "txt"]))

    def save_setence(self, processo, text):
        with codecs.open(self.complete_file_name(processo), "w", "utf-8") as handle:
            handle.write(text)


    def download_processo(self, driver, linha, dados):
        text, num_pages = self.scrapysentence.download_page(linha)
        if not self.debug:
            dados.write(self.file_name(linha) + "," + str(num_pages) + "\n")  
            self.save_setence(linha, text) 
                
       



    def get_file_path(self, path, *args):
        path_all = os.path.join(self.s.path, path)
        for p in list(args):
            path_all = os.path.join(path_all, p)
        return path_all

    def read_all_processes(self):
        arquivos_numero_processos = os.listdir(self.get_file_path("numero_processos"))
        processos = set()
        for file_path in arquivos_numero_processos:
            with open(self.get_file_path("numero_processos", file_path),"r") as handle:
                for line in handle.readlines():
                    processos.add(line.replace("\n",""))

        return processos

    def read_process(self):
        processos = set()
        for file_path in self.processNumbers:
            with open(self.get_file_path("numero_processos", file_path),"r") as handle:
                for line in handle.readlines():
                    processos.add(line.replace("\n",""))

        return processos

    def read_setencas_csv(self):
        dir_files = os.listdir(self.get_file_path("estatistica"))
        print(dir_files)
        processos = set()
        for file_path in dir_files:
            with open(self.get_file_path("estatistica", file_path), "r") as handle:
                for line in handle.readlines():
                    values = line.split(sep=",")
                    processos.add(self.processo_name(values[0]))
        return processos

    def download_pdf_sentencas(self):
        dados = None
        try:
            process = self.read_process() if self.processNumbers is not None else  self.read_all_processes()
            print(process)
            dados = open(self.create_estatisca_file(), "w")
            for line in process:
                self.download_processo(self.driver, line, dados)
        except Exception as e:
            logging.exception("Main loop brokes with exception")
        finally:
            dados.close()


    def download_pdf_sentences_test(self):
        dados = None
        try:
            process = self.processNumbers 
            print(process)
            for line in process:
                if self.debug:
                     print(line)
                self.download_processo(self.driver, line, None)
        except Exception as e:
            logging.exception("Main loop of download sentences brokes with exception")

    
    
