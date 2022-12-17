import json
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
folder2 = os.listdir(directory2)

folder = os.listdir(directory)    
class ProcessFile:
    def __init__(myuwuobject, filename, directory, directory2, index):
        myuwuobject.filename = filename
        myuwuobject.directory = directory
        myuwuobject.directory2 = directory2
        myuwuobject.lexicon = set()
        myuwuobject.inv_index = {}
        myuwuobject.i = index
    def run(myuwuobject):
        j = 0
        if myuwuobject.filename in folder2:
            return [myuwuobject.lexicon, myuwuobject.inv_index]
        f = os.path.join(myuwuobject.directory, myuwuobject.filename) 
        with open(f, 'r') as File:
            data = json.load(File)
            for i in data:  
                i["doc_ID"] = str(myuwuobject.i) + "-" + str(j)
                j += 1
                i["title"] = wordpunct_tokenize(i["title"])
                i["title"] = [lemmatizer.lemmatize(x.lower()) for x in i["title"] if (x.isalnum() and x.lower() not in Stopwords)]
                i["content"] = wordpunct_tokenize(i["content"])
                i["content"] = [lemmatizer.lemmatize(x.lower()) for x in i["content"] if (x.isalnum() and x.lower() not in Stopwords)]
                # Add the words from the title and content fields to the lexicon
                myuwuobject.lexicon.update(i["title"])
                myuwuobject.lexicon.update(i["content"])
                for word in myuwuobject.lexicon:
                    if word in i["title"]:
                        myuwuobject.inv_index[word] = myuwuobject.inv_index.get(word, []) + [i["doc_ID"]]
                    elif word in i["content"]:
                        myuwuobject.inv_index[word] = myuwuobject.inv_index.get(word, []) + [i["doc_ID"]]
        F = os.path.join(myuwuobject.directory2, myuwuobject.filename)
        with open (F, 'w') as FiLe:
            json.dump(data, FiLe)
        return [myuwuobject.lexicon, myuwuobject.inv_index]
#Main
if __name__ == '__main__':
    with open(os.path.join(path, "Lexicon.json"), 'r') as File:
        lexicon = json.load(File)
    with open(os.path.join(path, "Inv_index.json"), 'r') as File:
        inv_index = json.load(File)
    lexicon = eval(lexicon)
    lexicon = set(lexicon)
    inv_index = eval(inv_index)
    objects = [] 
    workers = cpu_count()-1
    if workers == 0:
        workers = 1
    p = Pool(workers)
    for i in range(0,4): 
        objects.append(ProcessFile(folder[i], directory, directory2, i))
    chunk = ceil(len(objects)/workers)
    proc = p.imap_unordered(ProcessFile.run, objects, chunksize = chunk) 
    for p in proc: 
        lexicon.update(p[0])
        inv_index.update(p[1])
    lexicon = list(lexicon)
    to_write = json.dumps(lexicon)
    with open (os.path.join(path, "Lexicon.json"), 'w') as L:
        json.dump(to_write, L)
    to_write = json.dumps(inv_index)
    with open (os.path.join(path, "Inv_index.json"), 'w') as I: 
        json.dump(to_write, I)