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
                    default="gpt-3.5-turbo", help="base LLM model.")
parser.add_argument("--api_keys", type=str,
                    default="your api key", help="if the LLM_type is gpt-3.5-turbo, gpt-4 or GLM, you need add your own openai/GLM api keys.")
parser.add_argument("--api_base", type=str,
                    default="your api base", help="if the LLM_type is Llama, you need give the api base.")
parser.add_argument("--max_length", type=int,
                        default=256, help="the max length of LLMs output.")

args = parser.parse_args()

def save_answer(question,path,answer,count,file_name):
    dict = {"question":question, "path": path, "answer": answer, "count": count}
    with open(file_name,"a") as outfile:
        json_str = json.dumps(dict)
        outfile.write(json_str + "\n")

w_datas = get_wo_path('./temp.json')

for w_data in tqdm(w_datas):
    question = w_data['question']
    path = w_data['path']
    count = w_data['count']
    prompt = get_answer_prompt + 'Question: ' + question + '\nTriplets Texts: ' + '\n'.join(path) + '\nAnswer: '
    answers = run_llm(prompt,args.temperature, args.max_tokens, args.api_keys, args.api_base, args.LLM_type)
    save_answer(question,path,answers,count,"./answer.jsonl")
    