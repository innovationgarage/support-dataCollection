import requests
import json
from credentials import credentials
import os

def requests_get(*arg, **kw):
    while True:
        try:
            response = requests.get(*arg, **kw)
        except Exception as e:
            print(e)
            time.sleep(5)
        else:
            if response.status_code == 200:
                return response
            if response.status_code == 401:
                raise Exception(response.content)
            print("Error %s. Sleeping 5s" % (r.status_code,))
            time.sleep(5)
            
def get_ticket(ticketid, cred=credentials):
    url = '{}/tickets/{}.json'.format(cred['url'], ticketid)
    response = requests_get(url, auth=(cred['user'], cred['pwd']))
    return response.json()
    
def get_all_orgs(cred=credentials):
    url = '{}/organizations.json'.format(cred['url'])
    response = requests_get(url, auth=(cred['user'], cred['pwd']))
    return response.json()

def get_org_tickets(orgid, url='', cred=credentials):
    if not url:
        url = '{}/organizations/{}/tickets.json'.format(cred['url'], orgid)
    response = requests_get(url, auth=(cred['user'], cred['pwd']))
    return response.json()

def get_ticket_comments(ticketid, url='', cred=credentials):
    if not url:
        url = '{}/tickets/{}/comments.json'.format(cred['url'], ticketid)
    response = requests_get(url, auth=(cred['user'], cred['pwd']))
    return response.json()
    
def get_all_tickets(tickets_path='tickets/', cred=credentials):
    if not os.path.exists(tickets_path):
        os.makedirs(tickets_path)

    all_orgs = get_all_orgs()
    orgs = [x['id'] for x in all_orgs['organizations']]
    for orgid in orgs:
        org_tickets = '{}.json'.format(orgid)
        print(orgid)
        tickets = []
        resp = get_org_tickets(orgid)
        #fix pagination!
        tickets.append(resp['tickets'])
        while resp['next_page']:
            print(resp['next_page'])
            resp = get_org_tickets(orgid, resp['next_page'])
            tickets.append(resp['tickets'])
            
        with open(os.path.join(tickets_path, org_tickets), 'w') as fout:
            json.dump(tickets, fout)
            fout.write("\n")
    print('All tickets are exported!')

def get_all_comments(comments_path='comments/', tickets_path='tickets/', cred=credentials):
    for filename in os.listdir(tickets_path):
        orgid = filename.split('.json')[0]
        orgpath = os.path.join(comments_path, orgid)
        print(orgpath)
        if not os.path.exists(orgpath):
            os.makedirs(orgpath)
        with open(os.path.join(tickets_path, filename)) as f:
            tickets = json.load(f)
        ticket_ids = [ticket['id'] for ticket in tickets[0]]
        for ticketid in ticket_ids:
            print(ticketid)
            ticket_comments = '{}.json'.format(ticketid)
            comments = []
            resp = get_ticket_comments(ticketid)
            comments.append(resp['comments'])
            while resp['next_page']:
                print(resp['next_page'])
                resp = get_ticket_comments(ticketid, resp['next_page'])
                comments.append(resp['comments'])
            with open(os.path.join(orgpath, ticket_comments), 'w') as fout:
                json.dump(comments, fout)
                fout.write("\n")
        print('All comments are exported!')


if __name__ == "__main__":
    get_all_tickets()
    get_all_comments()
