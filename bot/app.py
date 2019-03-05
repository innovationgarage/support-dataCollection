from flask import Flask
from flask import request
app = Flask(__name__)

from zenpy import Zenpy
from credentials import creds
from message import message

def parse_ticket(ticketid, zenpy_client):
    ticket = zenpy_client.tickets(id=ticketid)
    ticket_message = message(ticket.description)
    ticket_body = ticket_message.parsed
    ticket_message.clean = ticket_body
    ticket_message.remove_emails()
    ticket_message.remove_timestamps()
    ticket_message.remove_numbers()
    return ticket, ticket_message

def isAccountCreation(body):
    #FIXME! (too simplistic)
    if ("create" in body) and (("account" in body) or ("accounts" in body)):
        return True

def respond_with_form(ticketid, zenpy_client):
    macroid = 360004925359
    macro_result = zenpy_client.tickets.show_macro_effect(ticketid, macroid)
    # Update the ticket to actually change the ticket.
    zenpy_client.tickets.update(macro_result.ticket)
    new_ticket = zenpy_client.tickets(id=ticketid)
    return new_ticket

@app.route("/trigger")
def supportbot():
    zenpy_client = Zenpy(**creds)
    url_parameters = request.args
    ticketid = request.args['id']
#    ticketid = 5 #51145
    
    ticket, ticket_message = parse_ticket(ticketid, zenpy_client)
    ticket_body = ticket_message.clean
    if isAccountCreation(ticket_body):
        print("Nomnomnom...")
        print(ticket.status)
        ticket = respond_with_form(ticketid, zenpy_client)
        print(ticket.status)
        return "I am handling ticket #{} /SupportBot".format(ticketid)
    else:
        return "Pass on ticket #{}. Not my cup of tea! /SupportBot".format(ticketid)

if __name__ == '__main__':
#    app.run()
    app.run('0.0.0.0', 1987)
