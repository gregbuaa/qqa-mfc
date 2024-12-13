cot_prompt = """First I give you some examples, you study the way the example answers the question, and then you answer the question in relation to the description I give you of that way.

Here are the examples:

Q: What state is home to the university that is represented in sports by George Washington Colonials men's basketball?
A: First, the education institution has a sports team named George Washington Colonials men's basketball in is George Washington University , Second, George Washington University is in Washington D.C. The answer is {Washington, D.C.}.

Q: Who lists Pramatha Chaudhuri as an influence and wrote Jana Gana Mana?
A: First, Bharoto Bhagyo Bidhata wrote Jana Gana Mana. Second, Bharoto Bhagyo Bidhata lists Pramatha Chaudhuri as an influence. The answer is {Bharoto Bhagyo Bidhata}.

Q: Who was the artist nominated for an award for You Drive Me Crazy?
A: First, the artist nominated for an award for You Drive Me Crazy is Britney Spears. The answer is {Jason Allen Alexander}.

You need to think step by step and answer the question below. First you need to give your reasoning steps. And then give your the most concise answer behind the reasoning steps in the form 'The answer is {your answer}'.You just need to answer one.
Here is the question:
"""

simplify_question_prompt = """You will be provided with some Context and a complex Question that may contain one or more topic entities.
The Context contains the previous questions and their corresponding known facts.
You should analyse whether the Context contains the sufficient facts to answer the complex Question.
If not, please generate a simpler sub-question that we can answer it first.
The sub-question must be centred around only one topic entity that we need to explore new facts, and cannot be the same or similar to the historical question in the Context.
The content included with [] is known content, and your simplification of the problem is not asking questions about them, but treating them as known content. Please provide the answer step by step.
Here are three examples for you to learn from. Please give your answer strictly as instructed in the examples without any additional information.

#Here is the Example 1:
Context: None
Complex Question: Which country in europe has the largest land area?
Topic entities: Europe
Analysis: To solve this complex question, we should first determine that which countries belong to Europe. Then, we should determine which countries has the largest land area. Therefore, the JSON format of the sub-question is,
{
"sub-question": "which countries belong to Europe?",
"topic-entity": "Europe",
"sufficient": "False"
}

#Here is the Example 2:
Context: Q: Which artists were influenced by Eugene Delacroix? Known Facts: Artists influenced by Eugene Delacroix are [X]. [X] represents the name of a person who is an artist    Q: Which artists influenced Jackson Pollock? Known Facts: Jackson Pollock was influenced by the artist [Y]. [Y] represent an artist.
Complex Question: Which artist influenced by Eugene Delacroix had later affects on Jackson Pollock's work?
Topic entities: [Y]
Analysis: We already know the artists influenced by Eugene Delacroix is ([X])) and the artist who influenced Jackson Pollock is ([Y]). The result can be determined by finding the intersection of the two sets without requiring additional facts. Therefore, the Context are sufficient to answer the question. the JSON format of the sub-question is,
{
"sufficient": "True"
}

#Here is the Example 3:
Context: Q: What university did romney graduated from? Known Facts: Mitt Romney graduated from [Z], and [Z] represents an institution.
Complex Question: What university did romney graduated from?
Topic entities: [Z]
Analysis: We have known that Mitt Romney graduates from [Z]. To solve this complex question, we still should determine that which the sef of institutions [Z] belongs to the university. Therefore, the JSON format of the sub-question is,
{
"sub-question": " Which the sef of [X] belongs to the university?",
"topic-entity": "[Z]",
"sufficient": "False"
}

Here is the task that you need to do:
"""

search_prune_prompt = """You will be given a Question that contains a key topic entity.
I collect the triplets from knowledge graph that are formatted as ([Topic Entity], Relation, [Entity]), or its reverse ([Entity], Reverse_Relation, [Topic Entity]).
Please rate the triplets that contributes to the Question and [Topic Entity] and given the top-3 most relevant triplets.
And then please analysis whether each triplet is directly related to solve the question step by step.
If yes, please describe the triplet using natural language which must contains [Topic Entity] and [Entity].
There is an example for you to study. Please give the answer following the instruction of example strictly, and doesn't need any addition information.

#Here is the example:
Question: Who played the Character Dorothy in a film?
Topic Entity: Character Dorothy
Triplet: [Topic Entity], Relation, [Entity]
Relations: common.topic.article; fictional_universe.fictional_character.character_created_by; film.film_character.portrayed_in_films; book.book_character.appears_in_book
Triplet: [Entity], Reverse_Relation, [Topic Entity]
Reverse_Relations: film.performance.character; theater.theater_role.role; book.book.characters; tv.regular_tv_appearance.character; theater.play.characters; media_common.quotation.spoken_by_character
Answer: 
Triplet 1: [Entity], film.performance.character, Character Dorothy
This triplet connects the performances (and thus the actors) to the character Dorothy. This makes it straightforward to identify who played Dorothy in various performances. We have known the facts that The actor [Entity] played the character Dorothy based on this triple. The result is formatted as JSON format,
{
"facts-text": "The actor [Entity] played the character Dorothy.",
"relation": "film.performance.character",
"from": "Reverse_Relation",
"direct_related": "True",
"entity": "[Entity]"
}
Triple 2: Character Dorothy, film.film_character.portrayed_in_films, [Entity]
This triple  connects the character Dorothy to the films in which she has been portrayed. From these films, one can easily find the actors who played her. We have known the facts that the character Dorothy was played by the actor [Entity] based on this triple. The result is formatted as JSON format,
{
"facts-text": "The character Dorothy was played by the actor [Entity].",
"relation": "film.film_character.portrayed_in_films",
"from": "Relation",
"direct_related": "True",
"entity": "[Entity]"
}
Triple 3: Character Dorothy,  fictional_universe.fictional_character.character_created_by, [Entity]
This triple is less directly related to the specific question of who played Dorothy in a film. The result is formatted as JSON format,
{
"relation": "fictional_universe.fictional_character.character_created_by",
"from": "Relation",
"direct_related": "False"
}

Here is the task:
"""

entity_text_generate_prompt = """You will be given a text. Please help me to analyse and generate what type of entity [Entity] belongs to.
Here are three examples for you to learn from. Please give your answer strictly as instructed in the examples without any additional information.

#Here is the Example 1:
text: Which artists were influenced by Eugene Delacroix? Artists influenced by Eugene Delacroix are [Entity].
Analyse: {"analysis": "[Entity] represents an artist."}

#Here is the Example 2:
text: What university did romney graduated from? Mitt Romney graduated from [Entity].
Analyse: {"analysis": "[Entity] represents a university."}

#Here is the Example 3:
text: Who played the Character Dorothy in a film? The actor [Entity] played the character Dorothy.
Analyse: {"analysis": "[Entity] represents an actor."}

Here is the task:
"""

get_answer_prompt = """You will be given a question and some Triplets Texts. Triplets Text is some information related to the question, you need to use this information and combine it with your own knowledge to answer the question in the manner of the few examples I will give you below.
Here are two examples for you to learn from. Please give your answer strictly as instructed in the examples without any additional information.
You can make reasonable assumptions about some of the [Entity] in the triplets texts that are useful for the question, thus increasing the accuracy of your answer to the question.

#Here is the example1:
Question: Which location is the country of birth for Steve Nash and also serves as the setting for How She move?
Triplets Texts: (Steve Nash,people.person.place_of_birth,[Entity1]); [Entity1] represents a country. [Entity1]'s set: [Johannesburg]
([Entity1],film.film_location.featured_in_films,[Entity2]); [Entity2] represents a film. [Entity2]'s set: [District 9, Invictus, The Bang Bang Club]
([Entity2],film.film.country,[Entity3]); [Entity3] represents a country. [Entity3]'s set: [United States of America, New Zealand, Canada, South Africa]
Answer: Steve Nash is Canadian. He was born in South Africa but grew up and spent most of his life in Canada. Therefore, [Entity1] is Canada. The film "How She Move" is set in Canada. Therefore, [Entity2] is Canada. So the answer of the question is {Canada}.

#Here is the example2:
Question: what language the country where Rapa Nui Language is spoken speak?
Triplets Texts: (Rapa Nui Language,language.human_language.main_country,[Entity1]); [Entity1] represents a country. [Entity1]'s set: [Chile]
(Rapa Nui Language,language.human_language.countries_spoken_in,[Entity2]); [Entity2] represents a country. [Entity2]'s set: [Chile]
([Entity2],location.country.languages_spoken,[Entity3]); [Entity3] represents a language. [Entity3]'s set: [Spanish Language, Mapudungun Language, Rapa Nui Language, Puquina Language, Aymara language]
Answer: Rapa Nui Language is mainly spoken in Chile.So [Entity1] is Chile. The primary language spoken in Chile is Spanish. Therefore, [Entity3] is Spanish Language. So the answer to the question is {Spanish Language}.
"""

get_path_prompt = """You will be given a question, topic entities and the answer of the question. You will also be given triplets texts which are related to the question.
You should expand, modify or delete the triplets texts with your own knowledge. At last, the output is a triplet Path starting with the topic entities that are useful for answering the question.The question can be answered based on the triplet path.
Each triplet element in a triplet path is of the form (h,r,t). You just need to output the triplet path in {}, with each triplet element split by ';'.
Here are two examples for you to learn from. Please give your answer strictly as instructed in the examples without any additional information.

#Here is the example1:
Question: what is the predominant religion in the religious leader is Ovadia Yosef?
topic entities: Ovadia Yosef
the answer of the question: Ovadia Yosef is associated with Judaism, specifically Haredi Judaism. Therefore, [Entity1] is Haredi Judaism. Haredi Judaism is a part of the broader category of Abrahamic religions, which includes Judaism. Thus, [Entity3] is Abrahamic religions. The predominant religion associated with Ovadia Yosef is Judaism. So the answer to the question is {Judaism}.
triplets texts: (Ovadia Yosef,people.person.religion,[Entity1]); [Entity1] represents a religion. [Entity1]'s set: [Judaism, Haredi Judaism]
([Entity1],religion.religion.includes,[Entity2]); [Entity2] represents a religion. [Entity2]'s set: [Reform Judaism, Modern Orthodox Judaism, Jewish Renewal, Hasidic Judaism, Reconstructionist Judaism, Conservative Judaism, Orthodox Judaism, Sephardic law and customs, Haredi Judaism, Karaite Judaism, Rabbinic Judaism, Gitit]
([Entity1],religion.religion.is_part_of,[Entity3]); [Entity3] represents a religion. [Entity3]'s set: [Abrahamic religions]
([Entity3],religion.religion.includes,[Entity4]); [Entity4] represents a religion. [Entity4]'s set: [Islam, Christianity, Judaism]
([Entity3],religion.religion.beliefs,[Entity5]); [Entity5] represents a religion. [Entity5]'s set: [End time]
triplet path: {(Ovadia Yosef, people.person.religion, Haredi Judaism);(Haredi Judaism, religion.religion.is_part_of, Judaism);(Judaism, religion.religion.is_part_of, Abrahamic religions);}

#Here is the example2:
Question: when is the last time the the team has a team moscot named Lou Seal won the world series?
topic entities: Lou Seal
the answer of the question: The team with the mascot named Lou Seal is the San Francisco Giants. The last time the San Francisco Giants won the World Series was in 2014. Therefore, the answer to the question is {2014}.
triplets texts: (Lou Seal,sports.mascot.team,[Entity1]); [Entity1] represents a sports team. [Entity1]'s set: [San Francisco Giants]
triplet path: {(Lou Seal, sports.mascot.team, San Francisco Giants); (San Francisco Giants, sports.sports_team.championships, 2014)}
"""

get_no_answer_prompt = """You will be given a question and some Triplets Texts. Triplets Text is some information related to the question, you need to use this information and combine it with your own knowledge to answer the question in the manner of the few examples I will give you below.
The question might not align with the facts, meaning there may not be a correct answer in itself. You should analyse with the triplets texts and your own knowledge, and then judge whether the question is right which means the question itself has the answer. 
If the question does not have answer, you should first analyse and answer {No Answer} in hte end. Otherwise, answer the question.
Here are two examples for you to learn from. Please give your answer strictly as instructed in the examples without any additional information.
You can make reasonable assumptions about some of the [Entity] in the triplets texts that are useful for the question, thus increasing the accuracy of your answer to the question.

#Here is the example1:
Question: Which location is the country of birth for Steve Nash and also serves as the setting for How She move?
Triplets Texts: (Steve Nash,people.person.place_of_birth,[Entity1]); [Entity1] represents a country. [Entity1]'s set: [Johannesburg]
([Entity1],film.film_location.featured_in_films,[Entity2]); [Entity2] represents a film. [Entity2]'s set: [District 9, Invictus, The Bang Bang Club]
([Entity2],film.film.country,[Entity3]); [Entity3] represents a country. [Entity3]'s set: [United States of America, New Zealand, Canada, South Africa]
Answer: Steve Nash is Canadian. He was born in South Africa but grew up and spent most of his life in Canada. Therefore, [Entity1] is Canada. The film "How She Move" is set in Canada. Therefore, [Entity2] is Canada. So the answer of the question is {Canada}.

#Here is the example2:
Question:   What is the country where Rapa Nui Language and Chinese are both spoken?
Triplets Texts: (Rapa Nui Language,language.human_language.main_country,[Entity1]); [Entity1] represents a country. [Entity1]'s set: [Chile]
(Rapa Nui Language,language.human_language.countries_spoken_in,[Entity2]); [Entity2] represents a country. [Entity2]'s set: [Chile]
(Chinese,language.human_language.main_country,[Entity3]); [Entity3] represents a country. [Entity3]'s set: [China]
Answer: Rapa Nui Language is mainly spoken in Chile.So [Entity1] is Chile. Chinese is mainly spoken in China. So [Entity3] is China. So the country where speaks Rapa Nui Language does not speak Chinese. The question is wrong. {No Answer}.
"""



