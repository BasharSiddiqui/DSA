import nltk 
import json 
import os
directory = r'E:\nela-gt-2021\newsdata'
folder = os.listdir(directory)
for i in range(0,3):
    filename = folder[i]
    f = os.path.join(directory, filename) 
    with open(f, 'r') as File:
        data = json.load(File)
        for i in data:
            print(i["title"])