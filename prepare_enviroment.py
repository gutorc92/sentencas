# -*- coding: utf-8 -*-
import os
import platform
import urllib.request
import zipfile
from settings import Settings
from downloadsentences import DownloadSetence
from download_numero_processos import Extract_Numbers
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium import webdriver
if platform.system() == "Windows":
    import win32com.client as win32
from traceback import print_exc
import time
import random
<<<<<<< HEAD
import re
import codecs
=======
from networking import ProxedHTTPRequester
>>>>>>> Usando tor


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

def createThreads(init, end, range_n):
    driver = None
    try:
        start = datetime.now()
        # ex = Extract_Numbers(21, 1, 1000000, driver)
        # ex.run()
        # ex.join()
        x = list(range(init, end))
        pagin = [t * range_n for t in x]
        pagout = [t - 1 for t in pagin[1:]]
        pagout.append(pagin[-1] + range_n)
        list_ex = []
        for id, pagi, pago in zip(x, pagin, pagout):
             print(id, pagi, pago)
             ex = Extract_Numbers(id, pagi, pago, driver)
             list_ex.append(ex)

        #start = datetime.now()
        for p in list_ex:
             p.run()

        for p in list_ex:
             p.join()
        end = datetime.now()
        print("Took {}s to run download with Threads".format((end - start).total_seconds()))
        if platform.system() == "Windows":
            send_email(list_ex)
    except:
        print("fodeu")
        print_exc()
    # finally:
    #     driver.close()



if __name__ == "__main__":
    settings = Settings()
    for x in range(int(settings.endt), int(settings.init), -40):
        try:
            ex = Extract_Numbers(1, x-39, x, None)
            ex.download()
            del ex
            time_sleep = random.randint(30,200)
            time.sleep(time_sleep)
        except KeyboardInterrupt:
            last_file = settings.getLastFile()
            text = ""
            with codecs.open(os.path.join(dir, last_file), "r", "utf-8") as handle:
                text = handle.read()
            pagina = re.findall("Pagina (\d+)", text)[-1]
            print(pagina)
            settings.replace_setting("endt:", pagina)
            
            
=
