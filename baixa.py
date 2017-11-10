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




def save_setenca(processo, text):
    with codecs.open(os.path.join("textos",processo), "a", "utf-8") as handle:
        handle.write(text)

def download_processo(driver, linha, dados):
    lista_proc = linha.split("-")
    url = "https://esaj.tjsp.jus.br/cjpg/obterArquivo.do?cdProcesso="+lista_proc[0]+"&cdForo="+lista_proc[1]+"&nmAlias="+lista_proc[2]+"&cdDocumento="+lista_proc[3];
    #url = "https://esaj.tjsp.jus.br/pastadigital/abrirDocumentoEdt.do?cdProcesso=" + lista_proc[0] + "&cdForo=" + lista_proc[1]  + "&cdDocumento=" + lista_proc[3] + "&cdServico=800000&tpOrigem=2&flOrigem=P" + "&nmAlias=" + lista_proc[2] + "&ticket=s95oU%2F6j2impvuoV56F%2BRMo7DbaRQP0ciU9v3jTQY9CCy4IUZbNOKN4F0xYudKlvIAHSFUjX2HxkuQU8oYyb8ZElur%2Bk8m8uHYKEq9vnBjyqSA7flGRkiQ6YRolbKx3277mS6nqXFZxQPDba6iCPt3r7oew3B8EbW56T3zxsh%2Fexz2e1C43WMCjtepVZo0wBaji6MJ%2F%2FHPnVKIC4ALLlMA%3D%3D"
    print(url)
    file_name = ".".join([lista_proc[0], "txt"])
    print(file_name)
    driver.get(url);
    time.sleep(4)
    try:
        WebDriverWait(driver, 30).until(
            EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_tag_name('iframe'))
        )
    except:
        logging.debug("Cannot wait for frame")
    try:
        num_pages = driver.find_element_by_id("numPages").text.replace("de ", "")
        num_pages = num_pages.replace("of ", "")
        num_pages = int(num_pages)
        print(num_pages)
        page_container = driver.find_element_by_id("pageContainer%d" % num_pages)
        page_container.location_once_scrolled_into_view()
    except WebDriverException:
        logging.debug("cannto scroll: %s url: %s" % (file_name, url))
    time.sleep(1)
    try:
        #actions = ActionChains(driver)
        #actions.move_to_element(page_container).perform()
        dados.write(lista_proc[0] + "," + str(num_pages) + "\n")
        if num_pages > 1:
            logging.info("file name: %s url: %s" % (file_name, url))
        elements = driver.find_elements_by_class_name("textLayer")
        if num_pages != len(elements):
            logging.debug("num pages differente from elements for file: %s" % file_name)
        for element in elements:
            if len(element.text) == 0:
                logging.debug("element without characters for file: %s" % file_name)
            save_setenca(file_name, element.text)
        #print(element.text)
    except NoSuchElementException:
        logging.debug("Text layer nao encontrada para a url: %s", str(url))

def read_todos_processos():
    arquivos_numero_processos = os.listdir("numero_processos")
    processos = set()
    for file_path in arquivos_numero_processos:
        with open(os.path.join("numero_processos", file_path),"r") as handle:
            for line in handle.readlines():
                processos.add(line)

    return processos

def download_pdf_sentencas():
    dados = open("setencas.csv","w")
    driver = create_driver()
    processos = read_todos_processos()
    for line in processos:
        download_processo(driver, line, dados)
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
    log_file = "log" + str(start)
    logging.basicConfig(filename=log_file, format='%(levelname)s:%(message)s', level=logging.INFO)
    download_pdf_sentencas()
