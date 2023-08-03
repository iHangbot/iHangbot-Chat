import torch
from torch import nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import gluonnlp as nlp
import numpy as np
from tqdm import tqdm, tqdm_notebook
import pandas as pd
#KoBERT
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model
#transformer
from transformers import AdamW
from transformers.optimization import get_cosine_schedule_with_warmup
#GPU 설정
device = torch.device("cuda:0")
#bertmodel의 vocabulary
bertmodel, vocab = get_pytorch_kobert_model()

#from google.colab import drive
#drive.mount('/content/drive')

import pandas as pd
chatbot_data = pd.read_excel('C:\\Users\\yechan\\gpt-3\\감성대화말뭉치(최종데이터)_Validation')


len(chatbot_data) #79473
chatbot_data.sample(n=10)