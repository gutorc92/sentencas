# -*- coding: utf-8 -*-
import os
import platform
import sys
from datetime import datetime
import urllib.request
import zipfile
from settings import Settings





if __name__ == "__main__":
    if len(sys.argv) > 1 and str(sys.argv[1]) == 'backup':
        save_files = True
    else:
        save_files = False
    s = Settings()
    list_files = os.listdir(os.path.join(s.path, "numero_processos"))
    process = set()
    for file_path in list_files:
        with open(os.path.join(s.path, "numero_processos", file_path), "r") as f:
            for line in f.readlines():
                process.add(line.replace("\n", ""))


    print(len(process))
    if save_files:
        file_name = "backup_" + datetime.now().strftime("%d%m%Y_%H_%M")
        with open(os.path.join(s.path, "numero_processos", file_name), "w") as f:
            for number in process:
                f.write(number)
                f.write("\n")
