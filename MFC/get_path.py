from func import*
from tqdm import tqdm
from prompt import*
from utils import*
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--temperature", type=int,
                    default=0.1, help="the temperature")
parser.add_argument("--max_tokens", type=int,
                    default=1024, help="the max length of LLMs output.")
parser.add_argument("--LLM_type", type=str,
                    default="gpt3.5-turbo", help="base LLM model.")
parser.add_argument("--api_keys", type=str,
                    default="your api key", help="if the LLM_type is gpt-3.5-turbo, gpt-4 or GLM, you need add your own openai/GLM api keys.")
parser.add_argument("--api_base", type=str,
                    default="your api base", help="if the LLM_type is Llama, you need give the api base.")
parser.add_argument("--max_length", type=int,
                        default=256, help="the max length of LLMs output.")

args = parser.parse_args()

def save_answer(question,path,answer,result,count, file_name):
    dict = {"question":question, "path": path, "answer": answer, "complete_path": result, "count": count}
    with open(file_name,"a") as outfile:
        json_str = json.dumps(dict)
        outfile.write(json_str + "\n")

out_file = "get_answer's output:answer.json"
ins_file = "dataset: args.dataset.json"
outs = get_wo_path(out_file)
ins = get_wo_path(ins_file)

for out in tqdm(outs):
    question = out['question']
    path = out['path']
    answer = out['answer']
    count = out['count']
    s = [i for i in ins if i['question']== question][0]
    if s['correctness'] == '0':
        continue
    entities = list(s["topic_entity"].values())
    prompt = get_path_prompt + '\nHere is the task:\nQuestion: ' + question + '\ntopic entities: ' + '; '.join(entities) + '\nthe answer of the question: ' + answer + '\ntriplets texts: ' + '\n'.join(path) + '\ntriplet path: '
    results = run_llm(prompt,args.temperature, args.max_tokens, args.api_keys, args.api_base, args.LLM_type)
    save_answer(question,path,answer,results,count, "./path.jsonl")
    