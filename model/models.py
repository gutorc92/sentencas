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
