from nltk import wordpunct_tokenize
import json 
import os
from nltk.corpus import stopwords
directory = r'E:\nela-gt-2021\newsdata'
directory2 = r'E:\nela-gt-2021\cleanednewsdata'
folder = os.listdir(directory)
# Create an empty set to store the words in the lexicon
lexicon = set()
index = {}
for i in range(0,1):
    filename = folder[i]
    f = os.path.join(directory, filename) 
    with open(f, 'r') as File:
        data = json.load(File)
        for i in data:
            i["title"] = wordpunct_tokenize(i["title"])
            i["title"] = [x.lower() for x in i["title"] if (x.isalnum() and x not in stopwords.words('english'))]
            i["content"] = wordpunct_tokenize(i["content"])
            i["content"] = [x.lower() for x in i["content"] if (x.isalnum() and x not in stopwords.words('english'))]
            # Add the words from the title and content fields to the lexicon
            lexicon.update(i["title"])
            lexicon.update(i["content"])
            for word in lexicon:
                if word in i["title"]:
                    index[word] = index.get(word, []) + [i["id"]]
                if word in i["content"]:
                    index[word] = index.get(word, []) + [i["id"]]
    F = os.path.join(directory2, filename)
    with open (F, 'w') as FiLe:
        json.dump(data, FiLe) 

Lexicon = r'C:\Users\wahaj\source\repos\DSA\DSA\Lexicon.json'
to_write = json.dumps(lexicon)
with open (Lexicon, 'w') as L:
    json.dump(lexicon, L)
Index = r'C:\Users\wahaj\source\repos\DSA\DSA\Index.json'
to_write = json.dumps(index)
with open (Index, 'w') as I:
    json.dump(index, I)