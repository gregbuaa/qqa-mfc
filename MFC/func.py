from utils import *
from SPARQLWrapper import SPARQLWrapper, JSON
import re
from prompt import *

SPARQLPATH = "your free base api" 


sparql_head2relations = """\nPREFIX ns: <http://rdf.freebase.com/ns/>\nSELECT ?relation\nWHERE {\n  ns:%s ?relation ?x .\n}"""
sparql_head2tail = """PREFIX ns: <http://rdf.freebase.com/ns/>\nSELECT ?Entity\nWHERE {\nns:%s ns:%s ?Entity .\n}""" 
sparql_tail2relations = """\nPREFIX ns: <http://rdf.freebase.com/ns/>\nSELECT ?relation\nWHERE {\n  ?x ?relation ns:%s .\n}"""
sparql_tail2head = """PREFIX ns: <http://rdf.freebase.com/ns/>\nSELECT ?Entity\nWHERE {\n?Entity ns:%s ns:%s .\n}""" 
sparql_id = """PREFIX ns: <http://rdf.freebase.com/ns/>\nSELECT DISTINCT ?tailEntity\nWHERE {\n  {\n    ?entity ns:type.object.name ?tailEntity .\n    FILTER(?entity = ns:%s)\n  }\n  UNION\n  {\n    ?entity <http://www.w3.org/2002/07/owl#sameAs> ?tailEntity .\n    FILTER(?entity = ns:%s)\n  }\n}"""

def execurte_sparql(sparql_query):
    sparql = SPARQLWrapper(SPARQLPATH)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"]

def replace_relation_prefix(triplets):
    return [triplet['relation']['value'].replace("http://rdf.freebase.com/ns/","") for triplet in triplets]

def simplify_question(question, known_facts, topic_entities, args):
    if len(known_facts) == 0:
        known_facts = ["None"]
    
    prompt = simplify_question_prompt_wo_text + "Context: " + ' '.join(known_facts) + "\nComplex Question: " + question + "\nTopic entities: " + '; '.join([f"{entity['entity_name']}" for entity in topic_entities]) + "\nAnalysis: "
    result_txt = run_llm(prompt, args.temperature, args.max_tokens, args.api_keys, args.api_base, args.LLM_type)
    
    pattern = r'{[^{}]*}'
    matches = re.findall(pattern, result_txt)
    if len(matches)==0:
         return False, {}
    
    subquestion_json = {}
    for match in matches:
        try:
            subquestion_json = json.loads(match)
            if 'sub-question' in subquestion_json:
                break
        except Exception as e:
            continue

    if len(subquestion_json) == 0:
        return False, {}
    
    if 'topic-entity' in subquestion_json:
        subquestion_json['entity_id'] = topic_entities[0]['entity_id']
        subquestion_json['topic-entity'] = topic_entities[0]['entity_name']
    else:
        return False, {}
    return True, subquestion_json

def abandon_rels(relation):
    if relation == "type.object.type" or relation == "type.object.name" or relation.startswith("common.") or relation.startswith("freebase.") or "sameAs" in relation:
        return True

def search_question(head_entity_ids, head_entity_name, question, args):
    head_relations = relations_search(head_entity_ids, "head")
    tail_relations = relations_search(head_entity_ids, "tail")

    prompt = search_prune_prompt + "Question: " + question + '\nTopic Entity:'+ head_entity_name + '\nTriplet: [Topic Entity], Relation, [Entity]' + '\nRelations: ' + '; '.join( head_relations) + '\nTriplet: [Entity], Reverse_Relation, [Topic Entity]\nReverse_Relations: ' + '; '.join(tail_relations)  + '\nAnswer: '
    result_text = run_llm(prompt, args.temperature, args.max_tokens, args.api_keys, args.api_base, args.LLM_type)
    
    pattern = r"{[^{}]*}"
    matches = re.findall(pattern, result_text)

    if len(matches)==0:
        return False, []
    subfact_jsons = []
    for match in matches:
        try:
            subfact_json = json.loads(match)
            if 'direct_related' in subfact_json:
                subfact_jsons.append(subfact_json)
        except Exception as e:
            continue
    if len(subfact_jsons) == 0:
        return False, []
    
    for result in subfact_jsons:
        result['head_id'] = head_entity_ids
        result['head_name'] = head_entity_name
        result['question'] = question
        if result['direct_related'] != 'True':
            continue
        if 'reverse' in result['from'].lower():
            entity_set = search_all_entity(result["relation"], head_entity_ids, "tail")
        else:
            entity_set = search_all_entity(result["relation"], head_entity_ids, "head")
        result['entity_set'] = entity_set

        entity_text_prompt = entity_text_generate_prompt + "text: " + result['question'] + result['facts-text'] + "\nAnalyse: "
        text = run_llm(entity_text_prompt, args.temperature, args.max_tokens, args.api_keys, args.api_base, args.LLM_type)
        text = text.split('{')[1]
        text = text.split('}')[0]
        text = '{' + text + '}'
        result['entity_text'] = json.loads(text)['analysis']     
    return True, subfact_jsons

def search_all_entity(relation, head_entity_ids, direction):
    all_entities = []
    if direction == "head":
        sparql_extract_head =  sparql_head2tail % (head_entity_ids, relation)
    else:
        sparql_extract_head =  sparql_tail2head % (head_entity_ids, relation)
    head_entity_search = execurte_sparql(sparql_extract_head)
    for item in head_entity_search:
        all_entities.append(item['Entity']['value'].replace("http://rdf.freebase.com/ns/",""))
    return all_entities

def relations_search(entity_id, direction="head"):
    sparql_relations = sparql_head2relations if direction == "head" else sparql_tail2relations
    head_relations = []
    sparql_extract_head =  sparql_relations % (entity_id)
    head_relation_search = execurte_sparql(sparql_extract_head)
    head_relation_search = replace_relation_prefix(head_relation_search)
    for relation in head_relation_search:
        if not abandon_rels(relation):
            if relation not in head_relations:
                head_relations.append(relation)
    return head_relations

def answer_question(orginal_question, question_queue, args):
    has_explore_entity = []
    current_count = 0
    all_path = []
    path = []
    max_current = args.max_depth * len(question_queue)

    while len(question_queue) > 0:
        if current_count > max_current:
                break
        
        current_count += 1
        print("\ncurrent_count:" ,current_count)
        current_question = question_queue.pop(0)
        print("current_question:", current_question['question'])

        cur_topic_entities = current_question['topic_entity']
        print("current_topic_entity:", cur_topic_entities)
        
        if cur_topic_entities[0]['entity_id'] in has_explore_entity:
            current_count -= 1
            continue
        
        cur_known_facts = current_question['known_facts']
        print("current_facts:", cur_known_facts)

        all_path.append(current_question)
        simplify_sign, subquestion_json = simplify_question(orginal_question, cur_known_facts, cur_topic_entities, args)
        has_explore_entity.append(cur_topic_entities[0]['entity_id'])
        if simplify_sign:
            if 'sufficient' in subquestion_json and subquestion_json['sufficient'].lower() == 'true':
                break
            head_entity_name = subquestion_json['topic-entity']
            head_entity_ids = subquestion_json['entity_id']
            search_sign, subfacts_json = search_question(head_entity_ids,head_entity_name,subquestion_json['sub-question'], args)
            
            if search_sign:
                for subfacts in subfacts_json:
                    if subfacts['direct_related'] != 'True':
                        continue
                    if len(subfacts['entity_set'])==0:
                        continue
                    if len(subfacts['entity_set']) > 15:
                        continue
                    if subfacts['entity_set'][0] in has_explore_entity:
                        continue
                    else:
                        path.append(subfacts)
                        next_question = orginal_question
                        next_known_facts = cur_known_facts
                        replace_entity = '[' + subfacts['entity_set'][0] + ']'
                        next_known_facts.append('Q:' + subfacts['question'].replace('[Entity]',replace_entity) + ' Known Facts: ' + subfacts['facts-text'].replace('[Entity]',replace_entity) + subfacts['entity_text'].replace('[Entity]',replace_entity))
                        next_topic_entity = []
                        next_topic_entity.append({'entity_id': subfacts['entity_set'][0], 'entity_name': '[' + subfacts['entity_set'][0] + ']'})
                        question_queue.append({
                            'question': next_question,
                            'known_facts': next_known_facts,
                            'topic_entity': next_topic_entity,
                            'triplets': []
                        })
    return current_count ,path

def save_2_wo_process(question,path,file_name,count):
    dict = {"question":question, "path": path, "count": count}
    with open("{}_wo_process.jsonl".format(file_name),"a") as outfile:
        json_str = json.dumps(dict)
        outfile.write(json_str + "\n")

def save_2_w_process(question,path,count,file_name):
    dict = {"question":question, "path": path, "count": count}
    with open("{}_w_process.jsonl".format(file_name),"a") as outfile:
        json_str = json.dumps(dict)
        outfile.write(json_str + "\n")

def get_wo_path(filename):
    with open(filename,encoding='utf-8') as f:
        wo_datas = json.load(f)
    return wo_datas

def id2entity_name_or_type(entity_id):
    sparql_query = sparql_id % (entity_id, entity_id)
    sparql = SPARQLWrapper(SPARQLPATH)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    if len(results["results"]["bindings"])==0:
        return "UnName_Entity"
    else:
        return results["results"]["bindings"][0]['tailEntity']['value']

def ids2labels(id_lists):
    result = []
    for id_list in id_lists:
        search_result = id2entity_name_or_type(id_list)
        if search_result != 'UnName_Entity':
            result.append(search_result)
    return result

def get_triplet(path,entity):
    if path['from'] == 'Relation':
        if '[' in path['head_name']:
            triplet = f"({entity[path['head_id']]},{path['relation']},{entity[path['entity_set'][0]]})"
        else:
            triplet = f"({path['head_name']},{path['relation']},{entity[path['entity_set'][0]]})"
    else:
        if '[' in path['head_name']:
            triplet = f"({entity[path['entity_set'][0]]},{path['relation']},{entity[path['head_id']]})"
        else:
            triplet = f"({entity[path['entity_set'][0]]},{path['relation']},{path['head_name']})"
    return triplet



