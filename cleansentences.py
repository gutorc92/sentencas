# -*- coding: utf-8 -*-
import os
import logging
import time
import platform
import codecs
from settings import Settings
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CleanSentence(object):

    def __init__(self, file):
        self.s = Settings()
        self.s.extract_settings()
        self.file = file
        self.text = ""

    def remove_tribunal(self):
        pass

    def read_file(self):
        with codecs.open(self.file, "r") as handle :
            self.text = handle.read()








