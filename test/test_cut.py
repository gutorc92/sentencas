# -*- coding: utf-8 -*-
import os
import json
import codecs
from model.models import create_process
from settings import Settings
def jdefault(o):
            return o.__dict__

def get_files():
    s = Settings()
    dir_ = s.join('jsons')
    files_names = os.listdir(dir_)
    files_names = [os.path.join(dir_, f) for f in files_names if f.endswith(".json")]
    return files_names

def get_processes(file_name):
    dir_ = os.path.dirname(os.path.abspath(__file__))
    processes = []
    print(file_name)
    with codecs.open(os.path.join(dir_,file_name), "r","utf-8") as handle:
        text = handle.read()
        x = json.loads(text, object_hook=lambda d: create_process(d.keys(), d.values()))
        for p in x:
            processes.append(p)
    return processes

def getting_data_subject(attr = 'assunto'):
    files_names = get_files()
    agrouped = {}
    for file_name in files_names:
        print(file_name)
        with codecs.open(file_name, "r","utf-8") as handle:
            processes = json.loads(handle.read(), object_hook=lambda d: create_process(d.keys(), d.values()))
            for p in processes:
                if hasattr(p, attr):
                    group = getattr(p, attr)
                    if group in agrouped:
                        agrouped[group]['valor'] += 1
                        agrouped[group]['list_docs'].append(p.abstract)
                        agrouped[group]['list_target'].append(group)
                    else:
                        agrouped[group] = {}
                        agrouped[group]['valor'] = 1
                        agrouped[group]['list_docs'] = [p.abstract]
                        agrouped[group]['list_target'] = [group]
    keys_to_delete = [] 
    for k, v in agrouped.items():
        try:
            if v is None:
                print(k)
                keys_to_delete.append(k)
            if 'valor' not in v:
                print(k)
                keys_to_delete.append(k)
        except:
            keys_to_delete.append(k)
    for key in keys_to_delete:
        del agrouped[key]
    return agrouped

def getting_data_all(cut=300, attr = 'assunto'):
    files_names = get_files()
    agrouped = {}
    for file_name in files_names:
        print(file_name)
        with codecs.open(file_name, "r", "utf-8") as handle:
            processes = json.loads(handle.read(), object_hook=lambda d: create_process(d.keys(), d.values()))
            for p in processes:
                if hasattr(p, attr):
                    group = getattr(p, attr)
                    if group in agrouped:
                        agrouped[group]['valor'] += 1
                        agrouped[group]['list_docs'].append(p.abstract)
                        agrouped[group]['list_target'].append(group)
                    else:
                        agrouped[group] = {}
                        agrouped[group]['valor'] = 1
                        agrouped[group]['list_docs'] = [p.abstract]
                        agrouped[group]['list_target'] = [group]
    l_class = []
    keys_to_delete = []
    for k, v in agrouped.items():
        if 'valor' not in v:
            print('nao tem valor', k)
            keys_to_delete.append(k)
        elif len(k) < 3:
            keys_to_delete.append(k)
        else:
            if v['valor'] >= cut:
                l_class.append(k)
            else:
                keys_to_delete.append(k)

    for key in keys_to_delete:
        del agrouped[key]
    return  l_class, agrouped

def cut_data(assuntos, cut=100):
    l_docs = []
    l_target = []
    i = 0
    for k, v in assuntos.items():
        if v['valor'] > cut:
            i += 1
            l_docs = l_docs + v['list_docs'][0:cut]
            l_target = l_target + v['list_target'][0:cut]
    print(i)
    print(len(l_docs), len(l_target))
    return l_docs, l_target


def getting_data():
    files_names = get_files() 
    assuntos = {}
    for file_name in files_names:
        print(file_name)
        with codecs.open(file_name, "r","utf-8") as handle:
            text = handle.read()
        x = json.loads(text, object_hook=lambda d: create_process(d.keys(), d.values()))
        for p in x:
            #print(p.assunto)
            assunto = p.assunto.strip()
            if assunto in assuntos:
                assuntos[assunto]['valor'] += 1
                assuntos[assunto]['list_docs'].append(p.abstract)
                assuntos[assunto]['list_target'].append(assunto)
            else:
                assuntos[assunto] = {}
                assuntos[assunto]['valor'] = 1
                assuntos[assunto]['list_docs'] = [p.abstract]
                assuntos[assunto]['list_target'] = [assunto]
    l_docs = []
    l_target = []
    i = 0
    cut = 500
    for k, v in sorted(assuntos.items(), key=lambda x: x[0][0], reverse=True):
        if v['valor'] > cut:
            i += 1
            l_docs = l_docs + v['list_docs'][0:cut]
            l_target = l_target + v['list_target'][0:cut]
    print(i)
    print(len(l_docs), len(l_target))
    return l_docs, l_target

def count_data():
    dir_ = os.path.dirname(os.path.abspath(__file__))
    files_names = get_files() 
    total = 0
    for file_name in files_names:
        print(file_name)
        with codecs.open(os.path.join(dir_,file_name), "r","utf-8") as handle:
            text = handle.read()
        x = json.loads(text, object_hook=lambda d: create_process(d.keys(), d.values()))
        total = total + len(x)
    return total

if __name__ == "__main__":
    print(count_data())
    
