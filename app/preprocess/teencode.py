import pandas as pd

teencode_dict = dict(pd.read_csv('app/preprocess/assets/teencode.txt', delimiter = '\t').values)

def handle_teencode(text):
    w_split = text.split(' ')    
    return ' '.join([teencode_dict[word] if teencode_dict.__contains__(word) else word for word in w_split])
