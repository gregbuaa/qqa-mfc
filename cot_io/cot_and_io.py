from utils_IC import *
from tqdm import tqdm
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
parser.add_argument("--dataset", type=str,
                    default="cwq", help="choose the dataset.")
parser.add_argument("--max_length", type=int,
                    default=256, help="the max length of LLMs output.")
parser.add_argument("--answer_type", type=str,
                    default="COT", help="COT/IO")

args = parser.parse_args()


datas = get_wo_path(f'../{args.dataset}.json')


for data in tqdm(datas):
    org_question = data['question']
    results = generate_without_explored_paths(org_question, args)
    save_COT_IO(org_question, results, f"../{args.answer_type}.jsonl")

 

