from utils import *
from func import*
from tqdm import tqdm

file = "main.py's output: ('args.dataset'_wo_process.json)"
datas = get_wo_path(file)

for data in tqdm(datas):
    question = data['question']
    path = data['path']
    if  (len(path))==0:
        results = generate_without_explored_paths(question, dataset) #dataset: {cwq,webqsp...}
        save_2_jsonl(question, results, [], file_name=dataset)
        continue
    else:
        with open("temp.jsonl","a") as outfile:
            json_str = json.dumps(data)
            outfile.write(json_str + "\n")
    
 