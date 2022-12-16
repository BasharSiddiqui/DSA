import json
import os
from math import ceil
from nltk import word_tokenize
from nltk.corpus import stopwords
from multiprocessing import Pool, cpu_count, Value
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer()
Stopwords = stopwords.words("english")
path = os.getcwd()
directory = os.path.join(path, "Uncleaned")
directory2 =os.path.join(path, "Cleaned")
folder2 = os.listdir(directory2)
folder = os.listdir(directory)
class ProcessFile:
    counter = Value('i', 0, lock = True)
    def __init__(myuwuobject, filename, directory, directory2):
        myuwuobject.filename = filename
        myuwuobject.directory = directory
        myuwuobject.directory2 = directory2
        myuwuobject.lexicon = set()
        myuwuobject.inv_index = {}
    def run(myuwuobject):
        if myuwuobject.filename in folder2:
            return myuwuobject
        f = os.path.join(myuwuobject.directory, myuwuobject.filename) 
        with open(f, 'r') as File:
            data = json.load(File)
            for i in data:        
                i["title"] = word_tokenize(i["title"])
                i["title"] = [lemmatizer.lemmatize(x.lower()) for x in i["title"] if (x.isalnum() and x not in Stopwords)]
                i["content"] = word_tokenize(i["content"])
                i["content"] = [lemmatizer.lemmatize(x.lower()) for x in i["content"] if (x.isalnum() and x not in Stopwords)]
                # Add the words from the title and content fields to the lexicon
                myuwuobject.lexicon.update(i["title"])
                myuwuobject.lexicon.update(i["content"])
                i["doc_id"] = ProcessFile.counter.value
                ProcessFile.counter.value += 1
                print(i["doc_id"])
                for word in myuwuobject.lexicon:
                    if word in i["title"]:
                        myuwuobject.inv_index[word] = myuwuobject.inv_index.get(word, []) + [i["doc_id"]]
                    elif word in i["content"]:
                        myuwuobject.inv_index[word] = myuwuobject.inv_index.get(word, []) + [i["doc_id"]]
        F = os.path.join(myuwuobject.directory2, myuwuobject.filename)
        with open (F, 'w') as FiLe:
            json.dump(data, FiLe)
        return myuwuobject
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
    p = Pool(workers)
    for i in range(0,10): 
        objects.append(ProcessFile(folder[i], directory, directory2))
    chunk = ceil(len(objects)/workers)
    proc = p.imap_unordered(ProcessFile.run, objects)
    for obj in proc:
        lexicon.update(obj.lexicon)
        inv_index.update(obj.inv_index)    
    lexicon = list(lexicon)
    to_write = json.dumps(lexicon)
    with open (os.path.join(path, "Lexicon.json"), 'w') as L:
        json.dump(to_write, L)
    to_write = json.dumps(inv_index)
    with open (os.path.join(path, "Inv_index.json"), 'w') as I: 
        json.dump(to_write, I)