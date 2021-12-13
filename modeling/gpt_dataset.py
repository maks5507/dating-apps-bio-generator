import torch


class GPTDataset(torch.utils.data.Dataset):
    def __init__(self, dataset, batch_size, tokenizer):
        """
         :param dataset: path to csv file with data
         :param batch_size: mini-batch size used for training
         :param tokenizer: GPT-2 tokenizer instance from transformers
         """
        self.tokenizer = tokenizer
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.dataset = dataset
        self.batch_size = batch_size

        self.batches = []

        for i in range(int(len(self.dataset) / batch_size)):
            batch = self.dataset[i * self.batch_size: (i + 1) * self.batch_size]
            self.batches += [self.tokenizer(batch, padding=True, truncation=True, return_tensors="pt")]

    def __getitem__(self, index):
        return self.batches[index]

    def __len__(self):
        return len(self.batches)
