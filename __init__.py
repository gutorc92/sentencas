# -*- coding: utf-8 -*-
import os
import logging
import time
import platform
import codecs
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_url(processo):
    lista_proc = processo.split("-")
    url = "https://esaj.tjsp.jus.br/cjpg/obterArquivo.do?cdProcesso=" + lista_proc[0] + "&cdForo=" + lista_proc[
        1] + "&nmAlias=" + lista_proc[2] + "&cdDocumento=" + lista_proc[3];
    return url

def file_name(processo):
    return processo.replace("-","_").replace("\n","")

def processo_name(processo):
    return processo.replace("_","-")

def complete_file_name(processo):
    return os.path.join("textos",".".join([file_name(processo), "txt"]))

def save_setenca(processo, text):
    with codecs.open(complete_file_name(processo), "a", "utf-8") as handle:
        handle.write(text)

def extract_num_pages(element):
    nr_pages = 1
    num_pages = element.text.replace("de ", "")
    num_pages = num_pages.replace("of ", "")
    try:
        nr_pages = int(num_pages)
    except ValueError:
        logging.info("Cannot convert page number.")
    return nr_pages

def download_processo(driver, linha, dados):
    url = create_url(linha)
    driver.get(url);
    time.sleep(4)
    try:
        WebDriverWait(driver, 30).until(
            EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_tag_name('iframe'))
        )
    except:
        logging.info("Cannot wait for frame")
    num_pages = switch_to_frame(driver, linha, url)
    time.sleep(1)
    try:
        dados.write(file_name(linha) + "," + str(num_pages) + "\n")
        elements = driver.find_elements_by_class_name("textLayer")
        for element in elements:
            if len(element.text) == 0:
                logging.info("element without characters for file: %s" % file_name(linha))
            save_setenca(linha, element.text)
    except NoSuchElementException:
        logging.info("Text layer nao encontrada para a url: %s", str(url))


def switch_to_frame(driver, processo, url):
    try:
        num_pages = extract_num_pages(driver.find_element_by_id("numPages"))
        if num_pages > 1:
            page_container = driver.find_element_by_id("pageContainer%d" % num_pages)
            page_container.location_once_scrolled_into_view()
    except WebDriverException:
        logging.info("cannot scroll: %s url: %s" % (file_name(processo), url))
    return num_pages


def read_todos_processos():
    arquivos_numero_processos = os.listdir("numero_processos")
    processos = set()
    for file_path in arquivos_numero_processos:
        with open(os.path.join("numero_processos", file_path),"r") as handle:
            for line in handle.readlines():
                processos.add(line.replace("\n",""))

    return processos

def read_setencas_csv():
    dir_files = os.listdir("estatistica")
    print(dir_files)
    processos = set()
    for file_path in dir_files:
        with open(os.path.join("estatistica", file_path), "r") as handle:
            for line in handle.readlines():
                values = line.split(sep=",")
                processos.add(processo_name(values[0]))
    return processos

def download_pdf_sentencas():
    dados = None
    driver = create_driver()
    try:
        processos_to_read = read_todos_processos()
        processos_readed = read_setencas_csv()
        dados = open("estatistica/setencas.csv", "w")
        processos = processos_to_read - processos_readed
        print(processos)
        for line in processos:
            download_processo(driver, line, dados)
    except Exception as e:
        logging.info("Main loop brokes with exception: " + str(e))
    finally:
        driver.quit()
        dados.close()


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized");
    chrome_options.add_argument("useAutomationExtension=false")
    if platform.system() == "Linux":
        chromedriver = "chromedriver"
    else:
        chromedriver = "chromedriver.exe"
    
    chromedriver = os.path.join(os.path.dirname(os.path.realpath(__file__)), chromedriver)
    driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
    return driver


if __name__ == "__main__":
    start = datetime.now()
    log_file = "log" + start.strftime("%d%m%Y_%M_%H")
    log_file = os.path.join("log", log_file)
    logging.basicConfig(filename=log_file, format='%(levelname)s:%(message)s', level=logging.INFO)
    download_pdf_sentencas()

