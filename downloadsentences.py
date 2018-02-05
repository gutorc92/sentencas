# -*- coding: utf-8 -*-
import os
import logging
import time
import platform
import codecs
from settings import Settings
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

    def create_log_file(self):
        log_file = "log_" + datetime.now().strftime("%d%m%Y_%H_%M")
        self.log_file = os.path.join(self.s.path, "log", log_file)
        logging.basicConfig(filename=self.log_file, format='%(levelname)s:%(message)s', level=logging.INFO)

    def create_estatisca_file(self):
        estatistica_file = "sentences" + datetime.now().strftime("%d%m%Y_%M_%H")
        estatistica_file = os.path.join(self.s.path, "estatistica", estatistica_file)
        estatistica_file = ".".join([estatistica_file, "csv"])
        return estatistica_file

    def create_url(self, processo):
        lista_proc = processo.split("-")
        url = "https://esaj.tjsp.jus.br/cjpg/obterArquivo.do?cdProcesso=" + lista_proc[0] + "&cdForo=" + lista_proc[
            1] + "&nmAlias=" + lista_proc[2] + "&cdDocumento=" + lista_proc[3];
        return url

    def file_name(self, processo):
        return processo.replace("-","_").replace("\n","")

    def processo_name(self, processo):
        return processo.replace("_","-")

    def complete_file_name(self, processo):
        return self.get_file_path("textos",".".join([self.file_name(processo), "txt"]))

    def save_setence(self, processo, text):
        with codecs.open(self.complete_file_name(processo), "w", "utf-8") as handle:
            handle.write(text)

    def extract_left_px(self, attribute):
        if attribute.find("rotate") == -1:
            rotate =  False
        else:
            rotate =  True
        try:
            left = float(attribute.split(";")[0].split(":")[1].lstrip().replace("px",""))
        except:
            logging.exception("Cannot find left on style %s" % attribute)
            left = -1
        return left, rotate

        

    def extract_num_pages(self, element):
        nr_pages = 1
        num_pages = element.text.replace("de ", "")
        num_pages = num_pages.replace("of ", "")
        try:
            nr_pages = int(num_pages)
        except ValueError:
            logging.info("Cannot convert page number.")
        return nr_pages

    def download_processo(self, driver, linha, dados):
        print(self.debug)
        url = self.create_url(linha)
        driver.get(url);
        time.sleep(4)
        try:
            WebDriverWait(driver, 30).until(
                EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_tag_name('iframe'))
            )
        except:
            logging.info("Cannot wait for frame")
        num_pages = self.switch_to_frame(driver, linha, url)
        time.sleep(1)
        try:
            if not self.debug:
                dados.write(self.file_name(linha) + "," + str(num_pages) + "\n")  
            elements = driver.find_elements_by_class_name("textLayer")
            text = ""
            for element in elements:
                divs = element.find_elements_by_tag_name("div")
                line = ""
                size_left = -1
                for div in divs:
                    #print(div.get_attribute('style')) 
                    size_div_actual, rotate = self.extract_left_px(div.get_attribute('style'))
                    if not rotate:
                        if size_left >= size_div_actual:
                            text += line + "\n"
                            line = ""
                        line += div.text + " "
                            
                        size_left = size_div_actual
            if self.debug:
                print(text)
            else:
                self.save_setence(linha, text) 
                
        except NoSuchElementException:
            logging.info("Text layer nao encontrada para a url: %s", str(url))


    def switch_to_frame(self, driver, processo, url):
        try:
            num_pages = self.extract_num_pages(driver.find_element_by_id("numPages"))
            if num_pages > 1:
                page_container = driver.find_element_by_id("pageContainer%d" % num_pages)
                page_container.location_once_scrolled_into_view()
            return num_pages
        except WebDriverException:
            logging.exception("cannot scroll: %s url: %s" % (self.file_name(processo), url))
        except:
            logging.exception("cannot scroll: %s url: %s" % (self.file_name(processo), url))
        return 1

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

    
    
