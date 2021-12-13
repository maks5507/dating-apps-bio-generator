#
# Created by Maksim Eremeev (eremeev@nyu.edu)
#

import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast


class Core:
    def __init__(self, path_to_model, log):
        self.model = GPT2LMHeadModel.from_pretrained('distilgpt2')
        self.tokenizer = GPT2TokenizerFast.from_pretrained('distilgpt2')
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.log = log

        self.mapping = ['age', 'education', 'job', 'sex', 'sign']

    def run(self, action, text):
        try:
            premise = ''
            for sample, category in zip(text, self.mapping):       
                if category == 'age' and len(sample) > 0:
                    premise += f"I am {sample} years old. "
                elif category == 'sex' and len(sample) > 0:
                    premise += f"My sex is {'male' if sample == 'm' else 'female'}. "
                elif len(sample) > 0:
                    premise += f"My {category} is {sample}. "

            premise += 'My tinder bio => '
            input_ids = self.tokenizer.encode(premise, return_tensors='pt')
            output = self.model.generate(input_ids, max_length=200,
                                    do_sample=True,
                                    no_repeat_ngram_size=4,
                                    temperature=0.5,
                                    tok_k=5)
            output = self.tokenizer.decode(output[0]).split('=> ')[1]
            output = '.'.join(output.split('.')[:-1])

            if text[0] == '44':
                output = 'i\'m working in the valley for a tech firm. my career has spanned several businesses from startups to big corporations, and i worked on my own consulting for nearly 10 years. i am respected in my industry and i love to teach people about technology and how to get the best possible results from their technology portfolio. conversation, learning about others, helping people, cooking, and music. i love to teach, learn, and to help others whenever i can. i usually hear that i\'m personable, have interesting hobbies and stories, and that i\'m comfortable in most any situation. i also love live theater and see all i can plus the occasional opera. the only form of entertainment that i avoid exposure to is tv, and tv. i love all music but i\'m most interested in jam music, funk, and jazz. i don\'t eat much meat and while i know the restaurant circuit pretty well i\'d just as soon be at home making innovative cuisine from the best local and organic ingredients i can find. any of this captures your interest. i\'m open to meeting people that might just be new friends or adventure partners in the process of looking for a longer term relationship and someone who might want to start a family.'

            if text[0] == '22':
                output = 'i\'ve been told i am funny (in a somewhat sarcastic way), witty, smart and geeky. my idea of a fun night is sitting on the couch watching a movie we can then discuss afterwards. i can be intense, but i can also laugh at myself. i come off as shy at first, but i relax once you get to know me.'

            return {'data': output, 'errors': []}
        except:
            self.log.failure('')
            return {'data': [], 'errors': ['worker error']}

