#
# Created by Maksim Eremeev (eremeev@nyu.edu)
#

from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import torch

class Core:
    def __init__(self, path_to_model, log):
        """
         :param path_to_model: path to the pre-trained checkpoint
         :param log: writable log file descriptior (from twisted)
         """
        self.model = GPT2LMHeadModel.from_pretrained('distilgpt2')

        self.model.load_state_dict(torch.load(path_to_model))
        self.tokenizer = GPT2TokenizerFast.from_pretrained('distilgpt2')
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.log = log

        self.mapping = ['age', 'education', 'job', 'sex', 'sign']

    def run(self, action, text):
        """
         :param action: ignored
         :param text: set of features provided by users, empty string if no features were provided
         """
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

            return {'data': output, 'errors': []}
        except:
            self.log.failure('')
            return {'data': [], 'errors': ['worker error']}

