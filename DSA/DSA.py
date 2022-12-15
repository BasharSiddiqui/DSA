import json
import os
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from multiprocessing import Pool
import threading
Stopwords = stopwords.words("english")
class ProcessFile:
    def __init__(myuwuobject, filename, directory, directory2):
        super().__init__()
        myuwuobject.filename = filename
        myuwuobject.directory = directory
        myuwuobject.directory2 = directory2
        myuwuobject.lexicon = set()
        myuwuobject.index = {}

    def run(myuwuobject):
        f = os.path.join(myuwuobject.directory, myuwuobject.filename) 
        with open(f, 'r') as File:
            data = json.load(File)
            for i in data:
                i["title"] = wordpunct_tokenize(i["title"])
                i["title"] = [x.lower() for x in i["title"] if (x.isalnum() and x not in Stopwords)]
                i["content"] = wordpunct_tokenize(i["content"])
                i["content"] = [x.lower() for x in i["content"] if (x.isalnum() and x not in Stopwords)]
                # Add the words from the title and content fields to the lexicon
                myuwuobject.lexicon.update(i["title"])
                myuwuobject.lexicon.update(i["content"])
                for word in myuwuobject.lexicon:
                    if word in i["title"]:
                        myuwuobject.index[word] = myuwuobject.index.get(word, []) + [i["id"]]
                    if word in i["content"]:
                        myuwuobject.index[word] = myuwuobject.index.get(word, []) + [i["id"]]
        F = os.path.join(myuwuobject.directory2, myuwuobject.filename)
        with open (F, 'w') as FiLe:
            json.dump(data, FiLe)

directory = r'E:\nela-gt-2021\newsdata'
directory2 = r'E:\nela-gt-2021\cleanednewsdata'
folder = os.listdir(directory)
lexicon = set()
index = {}
# Create a thread for each file in the folder
if __name__ == '__main__':

    files = list(filename for filename in folder)
    objects = [] 
    procs = []
    p = Pool()
    for i in range(0,2): 
        objects.append(ProcessFile(folder[i], directory, directory2))
        t = threading.Thread(target = ProcessFile.run, args = (objects[i],))
        t.start()
    print("hello")
    proc = p.map(ProcessFile.run, objects)
    for obj in objects:
        lexicon.update(obj.lexicon)
        index.update(obj.index)
    Lexicon = r'C:\Users\wahaj\source\repos\DSA\DSA\Lexicon.json'
    lexicon = list(lexicon)
    to_write = json.dumps(lexicon)
    with open (Lexicon, 'w') as L:
        json.dump(lexicon, L)
    Index = r'C:\Users\wahaj\source\repos\DSA\DSA\Index.json'
    to_write = json.dumps(index)
    with open (Index, 'w') as I: 
        json.dump(index, I)