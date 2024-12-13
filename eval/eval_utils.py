import json
import re


def prepare_dataset_for_eval(dataset_name):
    if dataset_name == 'cwq':
        with open('../data/cwq.json',encoding='utf-8') as f:
            datas = json.load(f)
        question_string = 'machine_question'
    elif dataset_name == 'webqsp':
        with open('../data/WebQSP.json',encoding='utf-8') as f:
            datas = json.load(f)
        question_string = 'RawQuestion'
    elif dataset_name == 'graliqa':
        with open('../data/graliqa.json',encoding='utf-8') as f:
            datas = json.load(f)
        question_string = 'question'
    elif dataset_name == 'simpleqa':
        with open('../data/SimpleQA.json',encoding='utf-8') as f:
            datas = json.load(f)    
        question_string = 'question'
    elif dataset_name == 'our_datas:':
        with open('../data/CWQ-QQA.json',encoding='utf-8') as f:
            datas = json.load(f)    
        question_string = 'question'
    else:
        print("dataset not found, you should pick from {cwq, webqsp, grailqa, simpleqa, our_datas}.")
        exit(-1)
    return datas, question_string

def output_answer(output_file,answer_type,model):
    with open(f"../test/Result/{output_file}_{answer_type}_{model}.json", encoding='utf-8') as f:
        output_datas = json.load(f)
    return output_datas

def output_an(file):
    with open(file, encoding='utf-8') as f:
        output_datas = json.load(f)
    return output_datas