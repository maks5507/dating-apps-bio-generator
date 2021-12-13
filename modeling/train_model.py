from transformers import GPT2LMHeadModel, GPT2TokenizerFast
from modeling.gpt_dataset import GPTDataset
import pickle
from tqdm.auto import tqdm
import torch
import os
import torch.optim as optim


class Trainer:
    def __init__(self, train_data, valid_data, batch_size, pretrained_checkpoint=None):
        """
         :param train_data: pickle dump of training set
         :param valid_data: pickle dump of validation set
         :param batch_size: minibatch size used for training
         :param pretrained_checkpoint (optional): path to the partitially trained model
         """
        self.train = pickle.load(open(train_data, 'rb'))
        self.val = pickle.load(open(valid_data, 'rb'))

        self.model = GPT2LMHeadModel.from_pretrained('distilgpt2')
        if pretrained_checkpoint is not None:
            self.model.load_state_dict(torch.load(pretrained_checkpoint))

        self.tokenizer = GPT2TokenizerFast.from_pretrained('distilgpt2')
        self.tokenizer.pad_token = self.tokenizer.eos_token

        self.train_dataset = GPTDataset(self.train, batch_size, self.tokenizer)
        self.val_dataset = GPTDataset(self.val, batch_size, self.tokenizer)

    @staticmethod
    def train_loop(model, optimizer, scheduler, train_dataset, device, epoch=5,
                   val_dataset=None, save_model_at_end=False, output_dir='./'):
        """
         :param model: model on the correct device
         :param optimizer: torch optimizer instance
         :param scheduler: learning rate scheduler instance
         :param train_dataset: train dataset instance of the GPTDataset class
         :param val_dataset: validation dataset instance of the GPTDataset class
         :param epoch: number of epoch to train the model for
         :param save_model_at_end: whether to save the model at the end of training
         :param output_dir: path to the directory where model will be saved
         """
        train_losses = []
        val_losses = []

        for t in tqdm(range(epoch)):
            batches = 0
            model.train()
            total_loss = 0
            for batch_idx, x in tqdm(list(enumerate(train_dataset))):
                batches += 1
                x = x.to(device)

                output = model(**x, labels=x['input_ids'])

                loss = output[0]
                total_loss += loss.sum().detach().item()

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                scheduler.step()

                train_losses += [total_loss / batches]

            if val_dataset is not None:
                model.eval()
                with torch.no_grad():
                    total_loss = 0
                    batches = 0
                    for batch_idx, x in enumerate(val_dataset):
                        batches += 1
                        x = x.to(device)

                        output = model(**x, labels=x['input_ids'])
                        loss = output[0]
                        total_loss += loss.sum().detach().item()

                    val_losses += [total_loss / batches]

            print("[EPOCH]: %i, [TRAIN LOSS]: %.6f" % (t, train_losses[-1]))
            if val_dataset is not None:
                print("[EPOCH]: %i, [VAL LOSS]: %.6f" % (t, val_losses[-1]))
            if save_model_at_end:
                torch.save(model.state_dict(), os.path.join(output_dir, "gpt2model.pt"))
        return model, train_losses,

    def run(self, device, learning_rate, sch_gamma, sch_step_size):
        self.model.to(device)
        optimizer = optim.AdamW(self.model.parameters(), lr=learning_rate)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, gamma=sch_gamma, step_size=sch_step_size)
        return self.train_loop(model=self.model, optimizer=optimizer,
                               scheduler=scheduler,
                               train_dataset=self.train_dataset,
                               device=device, epoch=50, val_dataset=self.val_dataset,
                               save_model_at_end=True)
