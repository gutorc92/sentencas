# -*- coding: utf-8 -*-
import os
import sys
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
import re
import codecs
from networking import ProxedHTTPRequester
import codecs
import re
from urlstjsp import *


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
        return webdriver.PhantomJS(path_phantom)

    path_chromedriver = os_path("chromedriver.exe", "chromedriver" )
    if os.path.exists(path_chromedriver):
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-maximized");
        chrome_options.add_argument("useAutomationExtension=false")
        return webdriver.Chrome(path_chromedriver, chrome_options=chrome_options)



def numberoftest():
    return ["E6Z0CAQQN0000-510-PG5CAMP-47950266", "EB0000AHC0000-515-PG5SJCA-52940188"]





if __name__ == "__main__":
    try:
        driver  = create_driver() 
        d = DownloadSetence(driver, numberoftest(), debug=True)
        d.download_pdf_sentences_test()
    finally:
        driver.close()
