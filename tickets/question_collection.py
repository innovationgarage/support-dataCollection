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
from message import message
import pickle
import EFZP as zp

tickets_path = 'tickets/'
comments_path = 'comments/'
agents_path = 'agents.json'

with open(agents_path) as f:
    users = json.load(f)

agents = {}
for user in users['users']:
    agents[user['id']] = user['name']
    
email_tickets = []
incoming_messages = []
parsed_questions = []

for org_ticket_file in os.listdir(tickets_path):
    with open(os.path.join(tickets_path, org_ticket_file)) as f:
        org_tickets = json.load(f)[0]
        for ticket in org_tickets:
            if not(ticket['submitter_id'] in agents.keys()) and not(ticket['requester_id'] in agents.keys()) and not(ticket['assignee_id']==116046629912):
                email_tickets.append(ticket)
                msg = message(ticket['description'])
                email = zp.parse(msg.message)
                incoming_messages.append(msg)
                parsed_questions.append({ticket['id']:email['body']})

with open('incoming_messages.pkl', 'wb') as fout:
    pickle.dump(incoming_messages, fout, pickle.HIGHEST_PROTOCOL)

with open('parsed_questions.pkl', 'wb') as fout:
    pickle.dump(parsed_questions, fout, pickle.HIGHEST_PROTOCOL)

df = pd.DataFrame(data={'id': [list(d.keys())[0] for d in parsed_questions], 'comment': [list(d.values())[0] for d in parsed_questions]})    
df['len'] = df['comment'].apply(lambda x: len(x))
df['release'] = df['comment'].apply(lambda x: True if "release" in x else False)
df['password'] = df['comment'].apply(lambda x: True if "password" in x else False)
df['account'] = df['comment'].apply(lambda x: True if "account" in x else False)

df = df.loc[df['len']>15]
df = df.loc[df['len']<708]

"""
What info do we need?/what recipe should they follow?
* release attachment- same as unblock? (why are these not assigne to dualogbot?)
* create account
* reset password
"""
