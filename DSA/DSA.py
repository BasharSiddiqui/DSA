import json
import datetime
import os
from math import ceil
from nltk import wordpunct_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from multiprocessing import Pool, cpu_count

lemmatizer = WordNetLemmatizer()
Stopwords = stopwords.words("english")
path = os.getcwd()
directory = os.path.join(path, "Uncleaned")
directory2 =os.path.join(path, "Cleaned")
folder = [f for f in os.listdir(directory) if f.endswith(".json")]

class ProcessFile:
    def __init__(myuwuobject, filename, directory, directory2, index):
        myuwuobject.filename = filename
        myuwuobject.directory = directory
        myuwuobject.directory2 = directory2
        myuwuobject.lexicon = []
        myuwuobject.inv_index = []
        myuwuobject.i = index
        myuwuobject.fwd_index = []
    def run(myuwuobject):
        j = 0
        f = os.path.join(myuwuobject.directory, myuwuobject.filename) 
        with open(f, 'r') as File:
            data = json.load(File) 
            for i in data:
                lexx = set()
                inv = {}
                fwd = {}
                i["doc_ID"] = str(myuwuobject.i) + "-" + str(j)
                j += 1
                i["title"] = wordpunct_tokenize(i["title"])
                i["title"] = [lemmatizer.lemmatize(x.lower()) for x in i["title"] if (x.isalnum() and x.lower() not in Stopwords)]
                i["content"] = wordpunct_tokenize(i["content"])
                i["content"] = [lemmatizer.lemmatize(x.lower()) for x in i["content"] if (x.isalnum() and x.lower() not in Stopwords)]
                # Add the words from the title and content fields to the lexicon
                fwd[i["doc_ID"]] =fwd.get(i["doc_ID"], []) + sorted([word for word in (i["title"]+i["content"])])
                lexx.update(i["title"]+i["content"])
                for word in lexx:
                    inv[word] = inv.get(word, []) + [i["doc_ID"]]   
                myuwuobject.lexicon.append(lexx)
                myuwuobject.fwd_index.append(fwd)
                myuwuobject.inv_index.append(inv)
        F = os.path.join(myuwuobject.directory2, myuwuobject.filename)
        with open (F, 'w') as FiLe:
            json.dump(data, FiLe)
        return [myuwuobject.lexicon, myuwuobject.inv_index, myuwuobject.fwd_index]
#Main
if __name__ == '__main__':
    x1 = datetime.datetime.now()
    lexicon = set()
    inv_index = {}
    fwd_index = {}
    objects = [] 
    workers = cpu_count()-1
    if workers == 0:
        workers = 1
    p = Pool(workers)
    for i in range(len(folder)): 
        objects.append(ProcessFile(folder[i], directory, directory2, i))
    chunk = ceil(len(objects)/workers)
    proc = p.imap_unordered(ProcessFile.run, objects, chunk)
    p.close()
    p.join()
    for p in proc: 
        for i in p[0]:
            lexicon.update(i)
        for i in p[1]: 
            for key, value in i.items():
                inv_index.setdefault(key, []).append(value[0])
        for j in p[2]:
            fwd_index.update(j)
    lexicon = list(sorted(lexicon))
    inv_index = dict(sorted(inv_index.items()))
    fwd_index = dict(sorted(fwd_index.items()))
    with open (os.path.join(path, "Lexicon.json"), 'w') as L:
        json.dump(lexicon, L)
    with open (os.path.join(path, "Inv_index.json"), 'w') as I: 
        json.dump(inv_index, I)
    with open (os.path.join(path, "Fwd_index.json"), 'w') as F: 
        json.dump(fwd_index, F)
    print(f"Time taken: {datetime.datetime.now() - x1}")