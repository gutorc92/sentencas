# -*- coding: utf-8 -*-
import os
import sys
import platform
import urllib.request
import zipfile
from settings import Settings
from downloadsentences import DownloadSetence
from download_numero_processos import Extract_Numbers
from datetime import datetime
if platform.system() == "Windows":
    import win32com.client as win32
from traceback import print_exc
import time
import random
from networking import ProxedHTTPRequester, _TaskManager
from urlstjsp import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def os_path(file_win, file_linux):
    setencas_dir = os.path.dirname(os.path.realpath(__file__))
    if platform.system() == "Linux":
        path_file = os.path.join(setencas_dir, file_linux)
    else:
        path_file = os.path.join(setencas_dir, file_win)
    return path_file

def create_driver():
    path_phantom = os_path("phantomjs.exe", "phantomjs")
    if os.path.exists(path_phantom):
        return webdriver.PhantomJS()

    path_chromedriver = os_path("chromedriver.exe", "chromedriver" )
    if os.path.exists(path_chromedriver):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--start-maximized");
        chrome_options.add_argument("useAutomationExtension=false")
        return webdriver.Chrome(path_chromedriver, chrome_options=chrome_options)

def send_email(list_ex):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'gutorc@hotmail.com'
    mail.Subject = 'Dados coletados do Tj SP'
    mail.Body = 'Os dados coletados seguem em anexo'

    zipf = zipfile.ZipFile("C:\\Users\\b15599226\\Documents\\dados.zip", 'w', zipfile.ZIP_DEFLATED)
    for p in list_ex:
        for files_path in p.arquivos:
            if os.path.exists(os.path.join(p.s.path, "numero_processos", files_path)):
                zipf.write(os.path.join(p.s.path, "numero_processos", files_path))
        if os.path.exists(os.path.join(p.s.path, "numero_processos",p.log_file)):
            zipf.write(os.path.join(p.s.path, "numero_processos",p.log_file))

    zipf.close()
    mail.Attachments.Add("C:\\Users\\b15599226\\Documents\\dados.zip")
    mail.Send()

def create_directory():
    s = Settings()
    s.extract_settings()
    if os.path.isdir(s.path):
        if not os.path.isdir(os.path.join(s.path, "estatistica")):
            os.makedirs(os.path.join(s.path, "estatistica"))
        if not os.path.isdir(os.path.join(s.path, "numero_processos")):
            os.makedirs(os.path.join(s.path, "numero_processos"))
        if not os.path.isdir(os.path.join(s.path, "textos")):
            os.makedirs(os.path.join(s.path, "textos"))
        if not os.path.isdir(os.path.join(s.path, "log")):
            os.makedirs(os.path.join(s.path, "log"))


def download_chrome_driver():
    setencas_dir = os.path.dirname(os.path.realpath(__file__))
    if platform.system() == "Linux":
        link_download = "https://chromedriver.storage.googleapis.com/2.33/chromedriver_linux64.zip"
        chromedriver_file = os.path.join(setencas_dir, "chromedriver")
    else:
        chromedriver_file = os.path.join(setencas_dir, "chromedriver.exe")
        link_download = "https://chromedriver.storage.googleapis.com/2.33/chromedriver_win32.zip"

    if not os.path.exists(chromedriver_file):
        chromedriver_zip = os.path.join(setencas_dir, "chromedriver.zip")
        urllib.request.urlretrieve(link_download, chromedriver_zip)
        zip_ref = zipfile.ZipFile(chromedriver_zip, 'r')
        zip_ref.extractall(setencas_dir)
        zip_ref.close()
        os.remove(chromedriver_zip)

def download_phantomjs():
    setencas_dir = os.path.dirname(os.path.realpath(__file__))
    if platform.system() == "Linux":
        link_download = "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2"
        path_file = os.path.join(setencas_dir, "phantomjs")
    else:
        path_file = os.path.join(setencas_dir, "phantomjs.exe")
        link_download = "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-windows.zip"

    if not os.path.exists(path_file):
        phantomjs_zip = os.path.join(setencas_dir, "phantomjs.zip")
        urllib.request.urlretrieve(link_download, phantomjs_zip)
        zip_ref = zipfile.ZipFile(phantomjs_zip, 'r')
        zip_ref.extractall(setencas_dir)
        zip_ref.close()
        os.remove(phantomjs_zip)


def count_number_of_process(settings, option):
    if option ==  'backup':
        save_files = True
    else:
        save_files = False
    list_files = os.listdir(os.path.join(settings.path, "numero_processos"))
    process = set()
    for file_path in list_files:
        with open(os.path.join(settings.path, "numero_processos", file_path), "r") as f:
            for line in f.readlines():
                process.add(line.replace("\n", ""))


    print(len(process))
    if save_files:
        file_name = "backup_" + datetime.now().strftime("%d%m%Y_%H_%M_%S")
        with open(os.path.join(settings.path, "numero_processos", file_name), "w") as f:
            for number in process:
                f.write(number)
                f.write("\n")

def download_processes_numbers(settings):
    for key, vara in dic_urls.items():
        try:
            if not vara['done']:
                print(vara['name'])
                logger = settings.createLogFile("log_extracted_numbers_")
                logger.info("Vara %s" % vara['name'])
                total = 0
                start = datetime.now();
                for x in range(vara['init'], nr_paginas(vara['nr_registros']), 30):
                    print(x)
                    session = ProxedHTTPRequester()
                    ex = Extract_Numbers(x, x+30, session, vara['url'], logger)
                    ex.download()
                    total += ex.total
                    del ex
                    session.close()
                    del session
                print("Total", total)
                end = datetime.now()
                print("Demorou {} minutos para rodar a vara de {}".format((end-start).total_seconds()/60, vara['name']))
                logger.info("Demorou {} minutos para rodar a vara de {}".format((end-start).total_seconds()/60, vara['name']))
                #time.sleep(3600)
        except KeyboardInterrupt:
            session.close()
            session.end()
            sys.exit()

def download_setence():
    driver = None
    try:
        driver  = create_driver()
        driver.implicitly_wait(10)
        d = DownloadSetence(driver, None)
        d.download_pdf_sentencas()
    except Exception as e:
        print(e)
    finally:
        driver.close() if driver is not None else ''

if __name__ == "__main__":
    settings = Settings()
    if len(sys.argv) > 1:
        task = sys.argv[1]
        option = sys.argv[2] if len(sys.argv) > 2 else ""
    else:
        task = "--help"
    if "-d" in task:
        download_processes_numbers(settings)
    elif "-g" in task:
        count_number_of_process(settings, option)
    elif "-s" in task:
        download_setence()
    else:
        print("-d para baixar numero de processos")
        print("-g para contar o numero de processos")
        print("-s para baixar as sentencas")
        print("--help para ajuda")
