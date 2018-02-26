import scrapy
from bs4 import BeautifulSoup
from model.models import Varas, Mongo
import re

def number_of_results(div_resultaos):
    table = div_resultaos.find('table')
    # table_body = table.find('tbody')
    if table is not None:
        data = []
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        str_r = data[0][0]
        str_r2 = re.sub('[\\n\\t]', ' ', str_r)
        str_r2 = re.sub(' +', ' ', str_r2)
        r = re.match("Resultados (\d+) a (\d+) de (\d+)", str_r2)
        if r is not None:
            return int(r.group(3))
        else:
            return 1
    else:
        return 1


class SentencasSpider(scrapy.Spider):
    name = "sentencas"

    def start_requests(self):
        self.mongo = Mongo()
        varas = Varas.all(self.mongo.get_varas())
        urls = [ v.get_url() for v in varas if v.done is False] 
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = BeautifulSoup(response.text, "html.parser")
        resultados = page.find('div', {'id': 'resultados'})
        if resultados is not None:
            nr_results = number_of_results(resultados)        
            print(nr_results)
