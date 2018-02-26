import json
from pymongo import MongoClient
from settings import Settings

class Process(json.JSONEncoder):

    def __init__(self):
        self._id = ""
        self.npu_process = ""
        self.classe_process = ""
        self.assunto = ""
        self.judge = ""
        self.foro = ""
        self.comarca = ""
        self.vara = ""
        self.date = ""
        self.abstract = ""
        self.nr_sp = ""


    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.npu_process, self.classe_process, self.assunto, self.judge,  self.foro,  self.comarca, self.vara, self.date, self.nr_sp)

    def set(self, pos, value):
        dict = {0: 'npu_process', 1: 'classe_process', 2: 'assunto', 3:'judge',  4: 'foro',  5: 'comarca', 6: 'vara', 7: 'date', 8: 'abstract', 9 : 'nr_sp' }
        if pos in dict:
            self.__setattr__(dict[pos], value)

    def update(self, mprocesses):
        r = mprocesses.update_one({'_id': self._id},{'$set': self.__dict__}, upsert=False)
        return r.modified_count

    def find_one(self, mprocesses, value):
        document = mprocesses.find_one({'npu_process': value })
        return self.make_process(document)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def make_process(self, document):
        v = Process()
        v._id = document['_id']
        v.npu_process = document['npu_process']
        v.classe_process = document['classe_process']
        v.assunto = document['assunto']
        v.judge = document['judge']
        v.foro = document['foro']
        v.comarca = document['comarca']
        v.vara = document['vara']
        v.date = document['date']
        v.abstract = document['abstract']
        v.nr_sp = document['nr_sp']
        return v

    @staticmethod
    def all(mprocesses):
        cursor = mprocesses.find({})
        all_processes = []
        for document in cursor:
            v = Process()
            v._id = document['_id']
            v.npu_process = document['npu_process']
            v.classe_process = document['classe_process']
            v.assunto = document['assunto']
            v.judge = document['judge']
            v.foro = document['foro']
            v.comarca = document['comarca']
            v.vara = document['vara']
            v.date = document['date']
            v.abstract = document['abstract']
            v.nr_sp = document['nr_sp']
            all_processes.append(v)
        return all_processes

class Mongo():

    def __init__(self):
        settings = Settings()
        print(settings.mongo)
        self.client = MongoClient(settings.mongo)
        self.db = self.client.process_database

    def get_processes(self):
        return self.db.processes        

    def get_varas(self):
        return self.db.varas
    
class Varas():

    def __init__(self, nr_code, state = None, done = None):
        self.nr_code = nr_code
        self.state = 'SP' if state is None else state
        self.done = False if done is None else done
        self._id = None


    def __str__(self):
        return "%s, %s, %s" % (self.nr_code, self.state, self.done)

    def get_dict(self, full=False):
        if full is False:
            return {'nr_code': self.nr_code, 'done': self.done, 'state': self.state}
        else:
            return {'_id': self._id, 'nr_code': self.nr_code, 'done': self.done, 'state': self.state}

    def insert(self, mvaras):
        self._id = mvaras.insert_one(self.get_dict()).inserted_id
        return self._id

    def update(self, mvaras):
        r = mvaras.update_one({'_id': self._id},{'$set': self.get_dict()}, upsert=False)
        return r.modified_count

    def get_url(self):
        url_begin = "http://esaj.tjsp.jus.br/cjpg/pesquisar.do?conversationId=&dadosConsulta.pesquisaLivre=&tipoNumero=UNIFICADO&numeroDigitoAnoUnificado=&foroNumeroUnificado=&dadosConsulta.nuProcesso=&dadosConsulta.nuProcessoAntigo=&classeTreeSelection.values=&classeTreeSelection.text=&assuntoTreeSelection.values=&assuntoTreeSelection.text=&agenteSelectedEntitiesList=&contadoragente=0&contadorMaioragente=0&cdAgente=&nmAgente=&dadosConsulta.dtInicio=&dadosConsulta.dtFim=&varasTreeSelection.values="
        url_end = "&varasTreeSelection.text=2+Registros+selecionados&dadosConsulta.ordenacao=DESC"
    #for var1, var2 in zip(text[0:997], text[997:]):
        return url_begin + self.nr_code + url_end

    @staticmethod
    def all(mvaras):
        cursor = mvaras.find({})
        all_varas = []
        for document in cursor:
            v = Varas(document['nr_code'], document['state'], document['done'])
            v._id = document['_id']
            all_varas.append(v)
        return all_varas 
           
        

def create_process(key, values):
    p = Process()
    for k, v in zip(key, values):
        #print(k, v)
        p.__setattr__(k, v)
    return p



