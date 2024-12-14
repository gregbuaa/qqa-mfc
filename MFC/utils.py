import json
from prompt import*
from openai import OpenAI
import time

def prepare_dataset(dataset_name):
    if dataset_name == 'cwq':
        with open('../data/cwq.json',encoding='utf-8') as f:
            datas = json.load(f)
        question_string = 'machine_question'
    elif dataset_name == 'webqsp':
        with open('../data/WebQSP.json',encoding='utf-8') as f:
            datas = json.load(f)
        question_string = 'RawQuestion'
    elif dataset_name == 'grailqa':
        with open('../data/grailqa.json',encoding='utf-8') as f:
            datas = json.load(f)
        question_string = 'question'
    elif dataset_name == 'simpleqa':
        with open('../data/SimpleQA.json',encoding='utf-8') as f:
            datas = json.load(f)    
        question_string = 'question'
    elif dataset_name == 'my_datas:':
        with open('../data/CWQ-QQA.json',encoding='utf-8') as f:
            datas = json.load(f)    
        question_string = 'question'
    else:
        print("dataset not found, you should pick from {cwq, webqsp, grailqa, simpleqa, our_datas}.")
        exit(-1)
    return datas, question_string

def generate_without_explored_paths(question, args):
    prompt = cot_prompt + "\n\nQ: " + question + "\nA:"
    response = run_llm(prompt, args.temperature, args.max_length, args.api_keys, args.api_base, args.LLM_type)
    return response


def run_llm(prompt, temperature, max_tokens, api_keys, api_base= "", engine="glm4"):
    messages = [{"role":"system","content":"You are an AI assistant that helps people find information."}]
    message_prompt = {"role":"user","content":prompt}
    messages.append(message_prompt)

    if "llama" in engine.lower():
       client = OpenAI(
           api_key='EMPTY',
           base_url=api_base
       )
    elif "gpt" in engine.lower():
        client = OpenAI(
           api_key=api_keys,
           base_url=api_base
       )
    elif 'glm' in engine.lower():
        client = OpenAI(
            api_key=api_keys,
            base_url="glm api")
    f = 0
    while(f == 0):
        try:
            completion = client.chat.completions.create(
                model=engine,
                messages = messages,
                temperature=temperature
            )
            result = completion.choices[0].message.content
            f = 1
        except Exception as e:
            print(e)
            print(engine + " error, retry")
            time.sleep(2)    
    return result

def save_2_jsonl(question, answer, cluster_chain_of_entities, file_name):
    dict = {"question":question, "results": answer, "reasoning_chains": cluster_chain_of_entities}
    with open("{}.jsonl".format(file_name), "a") as outfile:
        json_str = json.dumps(dict)
        outfile.write(json_str + "\n")


