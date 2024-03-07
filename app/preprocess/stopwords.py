number = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
chars = ["a", "b", "c", "d", "đ", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o"]

with open('app/preprocess/assets/vietnamese_stopwords.txt', 'r') as file:
    stop_word_arr = file.read()

stop_word = number + chars + stop_word_arr.split('\n')

def handle_stopword(w):
    return w not in stop_word