import json
import os.path

for file in os.listdir("tickets"):
    if not file.endswith(".json"): continue
    orgid = file[:-len(".json")]
    file = "tickets/" + file
    with open(file) as f:
        data = json.load(f)
        for ticket in data[0]:
            ticketpath = "txt/%s/%s" % (orgid, ticket["id"])
            if not os.path.exists(ticketpath):
                os.makedirs(ticketpath)
            with open("%s/subject" % (ticketpath,), "w") as of:
                of.write(ticket["subject"].encode("utf-8"))
            with open("%s/description" % (ticketpath,), "w") as of:
                of.write(ticket["description"].encode("utf-8"))
            commentsfile = "comments/%s/%s.json" % (orgid, ticket["id"])
            if os.path.exists(commentsfile):
                with open(commentsfile) as cf:
                    comments = json.load(cf)
                if not os.path.exists("%s/comments" % (ticketpath,)):
                    os.makedirs("%s/comments" % (ticketpath,))
                for idx, comment in enumerate(comments[0]):
                    with open("%s/comments/%s" % (ticketpath, idx), "w") as of:
                        of.write(comment["plain_body"].encode("utf-8"))

                    


        
