
# Data

Data is saved in the `okcupid_{train, val, test}.pkl` pickle dumps. 

Loading the data:

```python
import pickle
train = pickle.load(open(okcupid_train, 'rb'))
```



# Fine-tuning

The sample fine-tuning script is given in the gpt2_training.py and preprocess.py scripts. These scripts preprocess the data and run the training job for finetuning GPT-2. 

The GPTDataset is built in gptdataset.py, it forms batches for training and sets up the GPT Tokenizer.



# Guidelines for using the sample GPT-2 fine-tuning script on Greene

Getting a GPU on Greene

`srun --nodes=1 --tasks-per-node=1 --cpus-per-task=4 --mem=64GB --time=12:00:00 --gres=gpu:1 --pty /bin/bash`



Launching jupyter notebook instance:

```
conda activate nmt
jupyter notebook --ip 0.0.0.0 --port 8965
```



You will see the output like this after executing the lines above:

```
To access the notebook, open this file in a browser:
        file:///home/mae9785/.local/share/jupyter/runtime/nbserver-4110553-open.html
    Or copy and paste one of these URLs:
        http://gr048.nyu.cluster:8965/?token=c7ef5118af35991d3b57a6df4bf5b9918d6763a426713153
     or http://127.0.0.1:8966/?token=c7ef5118af35991d3b57a6df4bf5b9918d6763a426713153
```



To forward the port use the following command in another terminal window:

`ssh -L 8965:gr048.nyu.cluster:8965 mae9785@greene.hpc.nyu.edu`



Then, you jupyter notebook is available at `http://localhost:8965`





