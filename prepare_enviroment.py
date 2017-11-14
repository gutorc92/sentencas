# -*- coding: utf-8 -*-
import os
from settings import Settings
from downloadsentences import DownloadSetence
import platform
import urllib.request
import zipfile

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
    d = DownloadSetence()
    d.download_pdf_sentencas()

