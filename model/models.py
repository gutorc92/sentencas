import json

class Process(json.JSONEncoder):

    def __init__(self):
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

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class Varas():

    def __init__(self, nr_code, state = None, done = None):
        self.nr_code = nr_code
        self.state = 'SP' if state is None else state
        self.done = False if done is None else done


    def __str__(self):
        return "%s, %s, %s" % (self.nr_code, self.state, self.done)

    def insert(self, mvaras):
        varas_id = mvaras.insert_one({'nr_code': self.nr_code, 'done': self.done, 'state': self.state}).inserted_id
        return varas_id

    @staticmethod
    def all(mvaras):
        cursor = mvaras.find({})
        all_varas = []
        for document in cursor:
            v = Varas(document['nr_code'], document['state'], document['done'])
            all_varas.append(v)
        return all_varas 
           
        

def create_process(key, values):
    p = Process()
    for k, v in zip(key, values):
        #print(k, v)
        p.__setattr__(k, v)
    return p



