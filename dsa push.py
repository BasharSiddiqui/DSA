import json
from nltk import SnowballStemmer
from nltk import word_tokenize
# with open("C:/Users/ahads/Documents/GitHub/DSA/buzzfeed.json",'r') as buzzfile:
#     data = json.load(buzzfile)
# print(data)
# list_ = nltk.sent_tokenize(buzzfile)
# print(list_)

example = "It is very important to be pythonly while you are pythonizing with python. All pythoners have pythoned poorly at least once."
words = word_tokenize(example)
ss = SnowballStemmer("english")

w = [ss.stem(i) for i in words]
print (w)