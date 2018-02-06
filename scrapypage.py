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

class ScrapySentence(object):

    def __init__(self, webDriver, debug=False):
        self.s = Settings()
        self.driver = webDriver
        self.create_log_file()
        self.debug = debug

    def create_log_file(self):
        name = "log_sentences_" + datetime.now().strftime("%d%m%Y_%H_%M")
        self.log_file = "log_sentences_" + datetime.now().strftime("%d%m%Y_%H_%M") + ".txt"
        self.logger = self.s.createLogFile(name, self.log_file)

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
            self.logger.exception("cannot scroll: %s url: %s" % (self.file_name(processo), url))
        except:
            self.logger.exception("cannot scroll: %s url: %s" % (self.file_name(processo), url))
        return 1

    def extract_text_divs(self, divs):
        line = ""
        size_left = -1
        text = ""
        for div in divs:
            size_div_actual, rotate = self.extract_left_px(div.get_attribute('style'))
            if not rotate:
                if size_left >= size_div_actual:
                    text += line + "\n"
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
            print(text) if self.debug else print('cu') 
        except NoSuchElementException:
            self.logger.info("Text layer nao encontrada para a url: %s", str(url))
        return text, num_pages


