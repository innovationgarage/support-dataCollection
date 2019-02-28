import json
import msgpack
import os.path

with open("fields.json") as f:
    fields = json.load(f)

fields = {field["id"]: field["title"] for field in fields["ticket_fields"]}

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
            fields[field["id"]]: field["value"]
            for field in ticket["custom_fields"]}

with open("all_tickets_fields.msgpack", "wb") as f:
    msgpack.dump(results, f)                   
        
