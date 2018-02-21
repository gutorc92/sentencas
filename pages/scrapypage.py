# -*- coding: utf-8 -*-
import os
import logging
import time
import platform
import codecs
import re
from settings import Settings
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests as req
from bs4 import BeautifulSoup
from model.models import Process

class ScrapySentence(object):

    def __init__(self, webDriver, logger, debug=False):
        self.s = Settings()
        self.driver = webDriver
        self.debug = debug
        self.logger = logger

    def create_url(self, processo):
        lista_proc = processo.split("-")
        url = "https://esaj.tjsp.jus.br/cjpg/obterArquivo.do?cdProcesso=" + lista_proc[0] + "&cdForo=" + lista_proc[
            1] + "&nmAlias=" + lista_proc[2] + "&cdDocumento=" + lista_proc[3];
        return url


    def extract_left_px(self, attribute):
        if attribute.find("rotate") == -1:
            rotate =  False
        else:
            rotate =  True
        try:
            left = float(attribute.split(";")[0].split(":")[1].lstrip().replace("px",""))
        except:
            self.logger.exception("Cannot find left on style %s" % attribute)
            left = -1
        return left, rotate

        

    def extract_num_pages(self, element):
        nr_pages = 1
        num_pages = element.text.replace("de ", "")
        num_pages = num_pages.replace("of ", "")
        try:
            nr_pages = int(num_pages)
        except ValueError:
            self.logger.info("Cannot convert page number.")
        return nr_pages

    
    def switch_to_frame(self, driver, processo, url):
        try:
            WebDriverWait(driver, 30).until(
                EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_tag_name('iframe'))
            )
        except:
            self.logger.info("Cannot wait for frame")
        try:
            num_pages = self.extract_num_pages(driver.find_element_by_id("numPages"))
            if num_pages > 1:
                page_container = driver.find_element_by_id("pageContainer%d" % num_pages)
                page_container.location_once_scrolled_into_view()
            return num_pages
        except WebDriverException:
            self.logger.exception("cannot scroll: %s url: %s" % (processo, url))
        except:
            self.logger.exception("cannot scroll: %s url: %s" % (processo, url))
        return 1

    def extract_text_divs(self, divs):
        line = ""
        size_left = -1
        text = ""
        for div in divs:
            size_div_actual, rotate = self.extract_left_px(div.get_attribute('style'))
            if not rotate:
                if size_left >= size_div_actual:
                    text += line + "\r\n"
                    line = ""
                line += div.text + " "
                size_left = size_div_actual
        return text

    def download_page(self, process_number):
        url = self.create_url(process_number)
        self.driver.get(url);
        time.sleep(11)
        text = ""
        num_pages = self.switch_to_frame(self.driver, process_number, url)
        try:
            elements = self.driver.find_elements_by_class_name("textLayer")
            for element in elements:
                divs = element.find_elements_by_tag_name("div")
                text = self.extract_text_divs(divs)
            print(text) if self.debug else 0
        except NoSuchElementException:
            self.logger.info("Text layer nao encontrada para a url: %s", str(url))
        return text, num_pages


class ScrapyNrProcess:

    def __init__(self, session, logging):
        self.session = session
        self.logger = logging

    def extract_link(self, table):
        link_tag = table.find("a")
        if link_tag is not None:
            return link_tag['name']
        else:
            return ""

    def read_table(self, element):
        data = []
        link = ''
        table = element.find('table')
        # table_body = table.find('tbody')
        if table is not None:
            link = self.extract_link(table)
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
        return  data, link

    def extract_process_object(self, data):
        p = Process()
        for i, info in enumerate(data, 0):
            info = info[0] if len(info) == 1 else info
            #print(i, info) if i == 8 else print()
            
            if i == 0 or i == 8:
                p.set(i,info)
            else:
                p.set(i, info.split("\n")[1].replace('\t', ''))

        return p

    def extract_process(self, response):
        page = BeautifulSoup(response.content, "html.parser")
        div = page.find("div", {"id": "divDadosResultado"})
        if div is None:
            self.logger.info("Nao encontrou a div de dados")
            return set()

        trs = div.find_all("tr", {'class':'fundocinza1'})
        processes = []
        for tr in trs:
            data_, link = self.read_table(tr)
            p = self.extract_process_object(data_)
            p.set(9, link)
            processes.append(p)
        return processes



    def download_page(self, page):
            url_t = "http://esaj.tjsp.jus.br/cjpg/trocarDePagina.do?pagina=" + str(page) + "&conversationId="
            self.logger.info("Pagina %s", str(page))
            response = self.session.get(url_t)
            if response.status_code == req.codes.ok:
                return self.extract_process(response)
            else:
                self.logger.info("A url nao pode ser encontrada: %s", str(url_t))
                return set()
