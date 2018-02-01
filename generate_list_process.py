# -*- coding: utf-8 -*-
import os
import platform
import urllib.request
import zipfile
from settings import Settings
from downloadsentences import DownloadSetence





if __name__ == "__main__":
    s = Settings()
    list_files = os.listdir(os.path.join(s.path, "numero_processos"))
    process = set()
    for file_path in list_files:
        with open(os.path.join(s.path, "numero_processos", file_path), "r") as f:
            for line in f.readlines():
                process.add(line.replace("\n", ""))

    print(len(process))

