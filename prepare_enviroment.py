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
import win32com.client as win32


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
        if os.path.exists(p.log_file):
            zipf.write(p.log_file)

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


if __name__ == "__main__":
    create_directory()
    download_chrome_driver()
    try:
        driver = create_driver()
        ex = Extract_Numbers(15, 2, 4, driver)
        ex.run()
        ex.join()
        range_n = 100
        x = list(range(0, 1000))
        pagin = [t * range_n for t in x]
        pagout = [t - 1 for t in pagin[1:]]
        pagout.append(pagin[-1] + range_n)
        list_ex = []
        for id, pagi, pago in zip(x, pagin, pagout):
             print(id, pagi, pago)
             ex = Extract_Numbers(id, pagi, pago, driver)
             list_ex.append(ex)

        start = datetime.now()
        for p in list_ex:
             p.run()

        for p in list_ex:
             p.join()
        end = datetime.now()
        print("Took {}s to run download with Threads".format((end - start).total_seconds()))
        send_email(list_ex)
    except:
        print("fodeu")
    finally:
        driver.close()



