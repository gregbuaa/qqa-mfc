from func import *
from tqdm import tqdm

file = "main.py's output: ('args.dataset'_wo_process.json)"
wo_datas = get_wo_path(file)

for wo_data in tqdm(wo_datas):
    question = wo_data['question']
    print(question)
    paths = wo_data['path']
    qcount = wo_data['count']
    triplets_texts = []
    entity = {}
    count = 1
    for path in paths:
        triplet_text = ""
        for ids in path['entity_set']:
            entity[ids] = f'[Entity{count}]'
        entity_text = path['entity_text'].replace('[Entity]',entity[path['entity_set'][0]])
        triplet = get_triplet(path,entity)
        entity_labels = ids2labels(path['entity_set'])
        count += 1
        triplet_text += triplet + '; ' + entity_text + ' '
        if len(entity_labels) == 0:
            continue
        else:
            triplet_text += entity[path['entity_set'][0]] + '\'s set: [' + ', '.join(entity_labels)+']'
        triplets_texts.append(triplet_text)
    save_2_w_process(question,triplets_texts,qcount,'cwq')

