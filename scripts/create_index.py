
import numpy as np
import faiss
import requests
from io import StringIO
import pandas as pd

import json
   
# Opening JSON file
f = open('data.json',)
   
# returns JSON object as 
# a dictionary
data = json.load(f)

# prepare data

pinPath = r"../../chronopin/scripts/backup/seedPins.json"
data = pd.read_json(pinPath)
print(data)

# data = pd.read_csv(StringIO(text), sep='\t')
# data.head()



sentences = data['sentence_A'].tolist()
sentences[:5]

# create index
nlist = 100
m = 8
k = 4
quantizer = faiss.IndexFlatL2(d)  # this remains the same
index = faiss.IndexIVFPQ(quantizer, d, nlist, m, 8)
                                  # 8 specifies that each sub-vector is encoded as 8 bits
index.train(xb)
index.add(xb)
D, I = index.search(xb[:5], k) # sanity check
print(I)
print(D)
index.nprobe = 10              # make comparable with experiment above
D, I = index.search(xq, k)     # search
print(I[-5:])