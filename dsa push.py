from nltk import *
import json 
import os
from nltk.corpus import stopwords
directory = r'E:\nela-gt-2021\newsdata'
directory2 = r'E:\nela-gt-2021\cleanednewsdata'
folder = os.listdir(directory)
for filename in folder:
    f = os.path.join(directory, filename) 
    with open(f, 'r') as File:
        data = json.load(File)
        for i in data:
            i["title"] = wordpunct_tokenize(i["title"])
            i["title"] = [x.lower() for x in i["title"] if (x.isalnum() and x not in stopwords.words('english'))]
            i["content"] = wordpunct_tokenize(i["content"])
            i["content"] = [x.lower() for x in i["content"] if (x.isalnum() and x not in stopwords.words('english'))]
    F = os.path.join(directory2, filename)
    with open (F, 'w') as FiLe:
        json.dump(data, FiLe)