import string
from underthesea import word_tokenize
import re

from app.preprocess.standarized_vietnamese import chuan_hoa_dau_cau_tieng_viet
from app.preprocess.teencode import handle_teencode
from app.preprocess.stopwords import handle_stopword

def remove_punctuation(w):
    return w not in string.punctuation

def lower_case(w):
    return w.lower()

def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Chuan hoa tu keo dai (Need fix)
def standardize_stretched_words(text):
    return re.sub(r'(\D)\1+', r'\1', text)

# Xoa tu co do dai lon hon 7
def remove_words_over_length_7(text):
    w_split = text.split(' ')    
    return ' '.join([word for word in w_split if word.__len__() <= 7])

# remove white space, \n, \t, \r, \v
def remove_whitespace(text):
    return re.sub(r'\s+', ' ', text.strip())


def preprocessing(text):
    sentence = remove_emoji(text)
    sentence = remove_whitespace(sentence)
    sentence = handle_teencode(sentence)
    sentence = standardize_stretched_words(sentence)
    sentence = remove_words_over_length_7(sentence)
    sentence = chuan_hoa_dau_cau_tieng_viet(sentence)

    tokens = word_tokenize(sentence)
    tokens = list(map(lower_case, tokens))
    tokens = list(filter(remove_punctuation, tokens))
    tokens = list(filter(handle_stopword, tokens))


    return ' '.join(tokens)