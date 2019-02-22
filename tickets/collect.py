import json
import msgpack
import os.path

results = {}
for file in os.listdir("tickets"):
    print file
    if not file.endswith(".json"): continue
    orgid = int(file[:-len(".json")])
    file = "tickets/" + file
    with open(file) as f:
        tickets = json.load(f)
        
    if orgid not in results: results[orgid] = {}
    for ticket in tickets[0]:
        results[orgid][ticket["id"]] = {
            u"subject": ticket["subject"],
            u"description": ticket["description"],
            u"comments": []
        }
        commentsfile = "comments/%s/%s.json" % (orgid, ticket["id"])
        if os.path.exists(commentsfile):
            print "  " + commentsfile
            with open(commentsfile) as cf:
                comments = json.load(cf)
            results[orgid][ticket["id"]][u"comments"] = [comment["plain_body"] for comment in comments[0]]

with open("all_tickets_and_comments.msgpack", "wb") as f:
    msgpack.dump(results, f)                   
        
