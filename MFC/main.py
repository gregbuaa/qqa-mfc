from utils import *
from func import *
import argparse
from tqdm import tqdm
import json
import re


parser = argparse.ArgumentParser()
parser.add_argument("--dataset", type=str,
                    default="cwq", help="choose the dataset.")
parser.add_argument("--max_length", type=int,
                    default=256, help="the max length of LLMs output.")
parser.add_argument("--max_depth", type=int,
                    default=3, help="the max depth of iteration.")
parser.add_argument("--topk", type=int,
                    default=3, help="the top-K relations.")
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

args = parser.parse_args()

datas, question_string = prepare_dataset(args.dataset)

print(f"Start Running on {args.dataset} dataset.")
for data in tqdm(datas):
    org_question = data[question_string]
    print("\nQuestion:",org_question)
    topic_entity = data['topic_entity']
    print("topic_entity:",topic_entity)

    if len(topic_entity) == 0: 
        results = generate_without_explored_paths(org_question, args)
        save_2_jsonl(org_question, results, [], args.dataset)
        continue

    question_quenue = []
    for entity in topic_entity:
        all_topic_entity = []
        all_topic_entity.append({'entity_id': entity, 'entity_name': topic_entity[entity]})
        question_quenue.append({
            'question': org_question,
            'known_facts': [],
            'topic_entity': all_topic_entity,
            'triplets': []
        })

    count, all_paths = answer_question(org_question, question_quenue, args)
    print('all_paths:', all_paths)
    if len(all_paths) == 0:
        results = generate_without_explored_paths(org_question, args)
        save_2_jsonl(org_question, results, [], args.dataset)
        continue
    else:
        save_2_wo_process(org_question,all_paths,args.dataset,count)