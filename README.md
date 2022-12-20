# DSA
This program is used to process a set of JSON files in the Uncleaned directory, clean them up by lemmatizing the words and removing stopwords, and then store the cleaned up versions in the Cleaned directory. It also creates three data structures: a lexicon, an inverted index, and a forward index.

The lexicon is a set of unique words found in the JSON files. The inverted index is a dictionary where the keys are words in the lexicon, and the values are lists of document IDs for documents that contain those words. The forward index is a dictionary where the keys are document IDs, and the values are lists of words in those documents, sorted in alphabetical order.

The script first reads in these three data structures from the Lexicon.json, Inv_index.json, and Fwd_index.json files, if they exist. It then creates a ProcessFile object for each JSON file in the Uncleaned directory, and stores these objects in a list called objects.

The script then uses the Pool class from the multiprocessing module to create a pool of worker processes, and uses the map method to apply the run method of each ProcessFile object to the list of objects. This allows the processing of the JSON files to be parallelized across multiple CPU cores.

Finally, the script saves the updated versions of the lexicon, inverted index, and forward index to the Lexicon.json, Inv_index.json, and Fwd_index.json files, respectively.
