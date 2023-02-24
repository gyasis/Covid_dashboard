# %%

import plotly.express as px
import pandas as pd


# %%
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 30, 40, 50],
    'group': ['A', 'B', 'C', 'D', 'E']
})

# %%
fig = px.line(df, x='x', y='y', color='group', animation_frame='group')


# %%
fig.update_layout(updatemenus=[dict(
    type="buttons",
    showactive=False,
    buttons=[dict(
        label="Sort Alphabetically",
        method="update",
        args=[{"title": "Sorted Alphabetically",
               "yaxis": {"autorange": "reversed"}},
               [dict(
                   args=[{"yaxis.autorange": "reversed"},
                         {"yaxis.categoryorder": "category ascending"}],
                   label="Ascending",
                   method="relayout"
               ),
               dict(
                   args=[{"yaxis.autorange": "reversed"},
                         {"yaxis.categoryorder": "category descending"}],
                   label="Descending",
                   method="relayout"
               )]
        )
    ])
])


# %%
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 30, 40, 50],
    'group': ['A', 'B', 'C', 'D', 'E']
})

fig = px.line(df, x='x', y='y', color='group', animation_frame='group')

fig.update_layout(updatemenus=[dict(
    type="buttons",
    showactive=False,
    buttons=[dict(
        label="Sort Alphabetically",
        method="update",
        args=[{"title": "Sorted Alphabetically",
               "yaxis": {"autorange": "reversed"}},
               [dict(
                   args=[{"yaxis.autorange": "reversed"},
                         {"yaxis.categoryorder": "category ascending"}],
                   label="Ascending",
                   method="relayout"
               ),
               dict(
                   args=[{"yaxis.autorange": "reversed"},
                         {"yaxis.categoryorder": "category descending"}],
                   label="Descending",
                   method="relayout"
               )]
        )]
    )
])

fig.show()

# %%
import torch
from torch.utils.data import Dataset, DataLoader
import re
import torch.nn as nn
import torch.optim as optim
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import re
import multiprocessing
import torch
from tqdm import tqdm_notebook as tqdm
import spacy
from transformers import AutoTokenizer


class GPT2DataLoader(Dataset):
    def __init__(self, data, max_length, tokenizer, device):
        self.data = data
        self.max_length = max_length
        self.tokenizer = tokenizer
        self.device = device

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        text = self.data[index]
        tokenized_text = self.tokenizer.tokenize(text)
        input_ids = self.tokenizer.encode(tokenized_text, add_special_tokens=True)
        
        # Truncate the input_ids to the max_length
        input_ids = input_ids[:self.max_length]
        
        # Pad the input_ids with zeros to reach the max_length
        padding_length = self.max_length - len(input_ids)
        input_ids = input_ids + [0] * padding_length
        
        # Create the attention mask
        attention_mask = [1] * len(input_ids)
        
        # Convert the input_ids, attention_mask, and token_type_ids to tensors and move them to the device
        input_ids = torch.tensor(input_ids).to(self.device)
        attention_mask = torch.tensor(attention_mask).to(self.device)
        token_type_ids = torch.zeros_like(input_ids).to(self.device)
        
        return {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids
        }



# Load the GPT2 tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Set the max length
max_length = 512

# Set the device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Load the GPT2 tokenizer
# nlp = GPT2Tokenizer.from_pretrained("gpt2")


def tokenize_text(df):
    return [tokenizer(text, padding="max_length", truncation=True) for text in df['text']]

# Load the text data into a list
with open('/gdrive/MyDrive/WorksWS_noheader.txt', 'r') as f:
    text_data = [line.strip() for line in f if not re.search(r'\d', line) and len(line.strip()) > 0]

# Create the custom DataLoader
dataloader = DataLoader(GPT2DataLoader(text_data, max_length, tokenizer, device), batch_size=24, shuffle=True, drop_last=True)
