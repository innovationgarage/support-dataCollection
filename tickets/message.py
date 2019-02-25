import string
import re
from nltk.corpus import stopwords
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk import ngrams
from collections import Counter

class message(object):
    def __init__(self, content, stop_words=set()):
        self.content = content
        self.clean = content.lower()
        english_stop_words = set(stopwords.words('english'))
        norwegian_stop_words = set(stopwords.words('norwegian'))
        self.stop_words = english_stop_words.union(norwegian_stop_words)
        self.add_stop_words(stop_words)
        self.cleanup()
        self.message = self.remove_previous_emails()
        
    @property
    def dict(self):
        return set(self.words)

    def add_stop_words(self, stop_words):
        self.stop_words = self.stop_words.union(set(stop_words))
        
    def select_words(self):
        self.clean = re.split(r'\W+', self.clean)
        
    def remove_emails(self):
        self.clean = re.sub('([a-zA-Z0-9_.+-]*@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', '', self.clean)

    def remove_timestamps(self):
        self.clean = re.sub('\d{4}-\d{2}-\d{2}', '', self.clean)
        self.clean = re.sub('\d{2}:\d{2}:\d{2}', '', self.clean)
        
    def remove_numbers(self):
        self.clean = re.sub(r'\d+', '', self.clean)
        
    def remove_stopwords(self):
        self.words = [w for w in self.words if not w in self.stop_words]
        
    def split_into_sentences(self, msg):
        self.sentences = sent_tokenize(msg)
        return self.sentences

    def split_into_words(self, msg):
        tokens = word_tokenize(msg)
        self.words = [word for word in tokens if word.isalpha()]
        return self.words

    def split_into_ngrams(self, n):
        Ngrams = ngrams(self.words, n)
        return Ngrams

    def get_top_ngrams(self, n, ntop=10):
        Ngrams = self.split_into_ngrams(n)
        ngram_count = Counter()
        for ngram in Ngrams:
            ngram_count[ngram] += 1
        return ngram_count.most_common(ntop)
        
    def stem_words(self, words):
        porter = PorterStemmer()
        self.stems = [porter.stem(word) for word in words]
        return self.stems

    def cleanup(self):
        self.clean = re.sub('\n+', ' ', self.clean.lower())
        self.clean = re.sub(' +', ' ', self.clean)
        self.remove_emails()
        self.remove_timestamps()
        self.remove_numbers()
        self.split_into_sentences(self.clean)
        self.split_into_words(self.clean)
        self.remove_stopwords()
        
    def get_top_words(self, n=10):
        word_count = Counter()
        for word in self.words:
            word_count[word] += 1
        self.topwords = word_count.most_common(n)
        return self.topwords

    def remove_previous_emails(self):
        self.message = self.clean.split('-original message-')[0]
        return self.message

    def remove_email_header(self):
        pass
