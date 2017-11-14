# -*- coding: utf-8 -*-
import os
from settings import Settings

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


if __name__ == "__main__":
    create_directory()

