import requests
import json
import os
import string
import re
from nltk.corpus import stopwords
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from collections import Counter

tickets_path = 'tickets/'
comments_path = 'comments/'

class message(object):
    def __init__(self, content):
        self.content = content
        self.clean = content.lower()
        english_stop_words = set(stopwords.words('english'))
        norwegian_stop_words = set(stopwords.words('norwegian'))
        self.stop_words = english_stop_words.union(norwegian_stop_words)

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

    def split_into_words(self, msg):
        tokens = word_tokenize(msg)
        self.words = [word for word in tokens if word.isalpha()]

    def stem_words(self, words):
        porter = PorterStemmer()
        self.stems = [porter.stem(word) for word in words]

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

        
        

        
def read_all_comments(comments_path):
    comments = []
    subdirs = os.listdir(comments_path)
    for subdir in subdirs:
        for ticketfile in os.listdir(os.path.join(comments_path, subdir)):
            with open(os.path.join(comments_path, subdir, ticketfile)) as f:
                data = json.load(f)
                comments.append([t['body'] for t in data[0]])
        
    return comments

def read_ticket_descriptions(tickets_path):
    descriptions = []
    for org_ticket_file in os.listdir(tickets_path):
        with open(os.path.join(tickets_path, org_ticket_file)) as f:
            org_tickets = json.load(f)[0]
            for ticket in org_tickets:
                descriptions.append(ticket['description'])
    return descriptions

def read_ticket_subjects(tickets_path):
    subjects = []
    for org_ticket_file in os.listdir(tickets_path):
        with open(os.path.join(tickets_path, org_ticket_file)) as f:
            org_tickets = json.load(f)[0]
            for ticket in org_tickets:
                subjects.append(ticket['subject'])
    return subjects

def count_words_in_cmts(comment_list):
    word_count = Counter()
    for comment in comment_list:
        comment.sort()
        for word in comment:
            word_count[word] += 1
    return word_count

    
# msg = message("The 5 bigg%)=&%&est countries by population in 2017 are China, India, United ?!!!!!States, Indonesia, an///%&d Brazil.")
# print(msg.content)
# msg.remove_emails()
# msg.remove_punctuation()
# print(msg.clean)
# msg.remove_numbers()
# print(msg.clean)

#all_comments  = read_all_comments(comments_path)
all_descriptions = read_ticket_descriptions(tickets_path)

# all_subjects = read_ticket_subjects(tickets_path)
# all_subject_words = [[x for x in subject.lower().split()] for subject in all_subjects]
# word_count = count_words_in_cmts(all_subject_words)
# print(word_count.most_common(100))
