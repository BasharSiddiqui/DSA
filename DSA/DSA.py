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
folder2 = [f for f in os.listdir(directory2) if f.endswith(".json")]
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
        if myuwuobject.filename in folder2:
            return [myuwuobject.lexicon, myuwuobject.inv_index, myuwuobject.fwd_index]
        f = os.path.join(myuwuobject.directory, myuwuobject.filename) 
        with open(f, 'r') as File:
            data = json.load(File)
            # x = 0  
            for i in data:
                lexx = set()
                inv = {}
                fwd = {}
                # print(x)
                # x+=1
                i["doc_ID"] = str(myuwuobject.i) + "-" + str(j)
                j += 1
                i["title"] = wordpunct_tokenize(i["title"])
                i["title"] = [lemmatizer.lemmatize(x.lower()) for x in i["title"] if (x.isalnum() and x.lower() not in Stopwords)]
                i["content"] = wordpunct_tokenize(i["content"])
                i["content"] = [lemmatizer.lemmatize(x.lower()) for x in i["content"] if (x.isalnum() and x.lower() not in Stopwords)]
                # Add the words from the title and content fields to the lexicon
                fwd[i["doc_ID"]] =fwd.get(i["doc_ID"], []) + sorted([word for word in i["content"]])
                lexx.update(i["title"])
                lexx.update(i["content"])
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
    with open(os.path.join(path, "Lexicon.json"), 'r') as File:
        lexicon = json.load(File)
    with open(os.path.join(path, "Inv_index.json"), 'r') as File:
        inv_index = json.load(File)
    with open(os.path.join(path, "Fwd_index.json"), 'r') as File:
        fwd_index = json.load(File)
    lexicon = eval(lexicon)
    lexicon = set(lexicon)
    inv_index = eval(inv_index)
    fwd_index = eval(fwd_index)
    objects = [] 
    workers = cpu_count()-1
    if workers == 0:
        workers = 1
    p = Pool(workers)
    for i in range(len(folder)): 
        objects.append(ProcessFile(folder[i], directory, directory2, i))
    chunk = ceil(len(objects)/workers)
    proc = p.imap_unordered(ProcessFile.run, objects, chunksize = chunk) 
    for p in proc: 
        for i in p[0]:
            lexicon.update(i)
        for i in p[1]:
            for key,value in i.items():
                inv_index[key] = inv_index.get(key, []) + value
        for j in p[2]:
            fwd_index.update(j)
    lexicon = list(lexicon)
    inv_index = dict(sorted(inv_index.items()))
    fwd_index = dict(sorted(fwd_index.items()))
    to_write = json.dumps(lexicon)
    with open (os.path.join(path, "Lexicon.json"), 'w') as L:
        json.dump(to_write, L)
    to_write = json.dumps(inv_index)
    with open (os.path.join(path, "Inv_index.json"), 'w') as I: 
        json.dump(to_write, I)
    to_write = json.dumps(fwd_index)
    with open (os.path.join(path, "Fwd_index.json"), 'w') as F: 
        json.dump(to_write, F)
    print(f"Time taken: {datetime.datetime.now() - x1}")
# from collections import defaultdict, Counter
# from concurrent.futures import ProcessPoolExecutor
# import json
# import os
# import datetime
# import numpy as np
# from nltk.corpus import stopwords
# from nltk.tokenize import WordPunctTokenizer
# from nltk.stem.snowball import SnowballStemmer
# import pandas as pd
# import re

# punctuations = re.compile(r'[^\w\s]')
# stop_words = set(stopwords.words('english'))
# tokenizer = WordPunctTokenizer()
# stemmer = SnowballStemmer('english')
# temp = 0


# def json_parser(path1):
#     def temp_parse(x):
#         x = tokenizer.tokenize(punctuations.sub('', x))
#         x = [stemmer.stem(word) for word in x if word.lower() not in stop_words]
#         return x

#     with open(path1, 'r') as f:
#         df = pd.DataFrame(json.load(f))
#     df['content'] = df['content'].apply(temp_parse)
#     unique_tokens = np.unique(token for doc in df['content'].values for token in doc)
#     doc_dict = {row['id']: row['content'] for row in df.to_dict(orient='records')}
#     return unique_tokens, doc_dict


# def inverted_index(path2):
#     unique_tokens, doc_dict = json_parser(path2)
#     global temp
#     temp += len(doc_dict)
#     print(temp)
#     inverted_indexing = {}
#     for doc_id, tokens in doc_dict.items():
#         for token in tokens:
#             if token not in inverted_indexing:
#                 inverted_indexing[token] = {}
#             if doc_id in inverted_indexing[token]:
#                 inverted_indexing[token][doc_id] += 1
#             else:
#                 inverted_indexing[token][doc_id] = 1
#     return inverted_indexing


# def create_inverted_index(path3):
#     with ProcessPoolExecutor() as executor:
#         indexes = list(executor.map(inverted_index, (path3 + x for x in os.listdir(path3))))
#     merged_index = defaultdict(Counter)
#     for index in indexes:
#         for token, doc_counts in index.items():
#             merged_index[token] += doc_counts
#     return merged_index

# #
# def create_inverted_index(path):
#     merged_index = defaultdict(Counter)
#     for file in os.listdir(path):
#         index = inverted_index(path + file)
#         for token, doc_counts in index.items():
#             merged_index[token] += doc_counts
#     return merged_index


# if __name__ == '__main__':
#     # path = "X:\\Dataset\\nela-gt-2021\\newsdata\\"
#     path = "C:\\Users\\ahads\\Uncleaned\\"
#     x1 = datetime.datetime.now()
#     index = create_inverted_index(path)
#     with open('.\\output_test.json', 'w', encoding='utf-8') as fx:
#         json.dump(index, fx)
#     print(temp)
#     print(f"Time taken: {datetime.datetime.now() - x1}")

# if __name__ == '__main__':
#     # path = "X:\\Dataset\\nela-gt-2021\\newsdata\\"
#     path = "C:\\Users\\ahads\\Uncleaned\\"
#     x1 = datetime.datetime.now()
#     # index = create_inverted_index(path)
#     temp = 0
#     for file in os.listdir(path):
#         file1 = open(path + file, "r")
#         file_data = json.loads(file1.read())
#         file1.close()
#         temp += len(file_data)
#         print(temp)
#     print(temp)
#     print(f"Time taken: {datetime.datetime.now() - x1}")