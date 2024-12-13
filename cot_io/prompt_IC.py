#cot
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



#IO
IO_prompt = """First I give you three examples, you study the way the example answers the question, and then you answer the question in relation to the description I give you of that way.

Here are the examples:
Q: What state is home to the university that is represented in sports by George Washington Colonials men's basketball?
A: {Washington, D.C.}.

Q: Who lists Pramatha Chaudhuri as an influence and wrote Jana Gana Mana?
A: {Bharoto Bhagyo Bidhata}.

Q: Who was the artist nominated for an award for You Drive Me Crazy?
A: {Jason Allen Alexander}.

You just need to  give your the most concise answer in the form '{your answer}'.You just need to answer one.
Here is the question:
"""
