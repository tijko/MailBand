#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import poplib
import smtplib
import sqlite3
import os
import email


_pop_addr = {'gmail.com':'pop.gmail.com',
             'msn.com':'pop3.live.com',
             'hotmail.com':'pop3.live.com',
             'live.com':'pop3.live.com',
             'aol.com':'pop.aol.com'
            }


def build_messages(session, total_messages):
    inbox = dict()
    for message in xrange(1, total_messages + 1):
        raw_data = session.retr(message)[1]
        raw_email = '\n'.join(raw_data)
        email_data = email.message_from_string(raw_email)
        sender = email_data['From']
        subject = email_data['Subject']
        body = ''
        for part in email_data.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload()
        inbox[sender] = {subject:body}
    return inbox
        

def deliver(address, action): 
    for addr in address:
        accnt_name, server_suffix = addr[0].split('@')
        server = _pop_addr[server_suffix]
        session = poplib.POP3_SSL(server)
        try:
            if server_suffix == 'gmail.com':
                session.user(accnt_name)
                session.pass_(addr[1])
            else:
                session.user(addr[0])
                session.pass_(addr[1])   
            total_messages = session.stat()[0]         
            print 'Emails %d for: %s' % (total_messages, addr[0])
            if total_messages:
                messages = build_messages(session, total_messages)
                tagged_messages = list(enumerate(messages, 1))
                for msg_num, sender in tagged_messages:
                    print '\n[%d]    %s' % (msg_num, sender)
                selection = raw_input('\nSelect your e-mail numbers: ')
                mail_selection = dict()
                for choice in selection.split(','):
                    if (choice.isdigit() and 
                        any(i[0] == int(choice) for i in tagged_messages)):
                        for msg in tagged_messages:
                            if msg[0] == int(choice):
                                mail_selection[msg[1]] = messages[msg[1]]
                                break
                if mail_selection:
                    if action == 'write':
                        save_local(addr[0], mail_selection)
                    elif action == 'read':
                        read_account_mail(mail_selection)
                    elif action == 'delete':
                        delete_account_mail(session, mail_selection) #XXX tagged_messsages
                session.quit()                               
        except poplib.error_proto:
            print '\nUsername or Password Error ==> %s\n' % addr[0]
            pass
    return

def save_local(account, selection):
    if not os.path.isfile(os.environ['HOME'] + '/.mailband.db'):
        create_database()
    con = sqlite3.connect(os.environ['HOME'] + '/.mailband.db')
    with con:
        for msg in selection:
            for title in selection[msg]:
                cur = con.cursor()
                cur.execute("SELECT * FROM Email")
                load = selection[msg][title]                            
                cur.execute("INSERT INTO Email VALUES(?,?,?)", (account,
                                                                title,
                                                                load))
            print '\nMessage %s saved!' % title 
    return                

def read_account_mail(selection):
    for msg in selection:
        for subject in selection[msg]:
            print "Message [%s]\n" % subject
            print selection[msg][subject]
    return

def delete_account_mail(session, selection):
    print "\nAre you sure you want to DELETE messages ==> %s" % str(selection)
    while True:
        answer = raw_input("(y or n): ") 
        if answer.lower() == 'y' or answer.lower() == 'n':
            break
    if answer.lower() == 'y':
        for msg in selection:
            try:
                session.dele(msg)
                print '\nMessage Deleted!\n'
            except poplib.error_proto:
                print '\nBad Selection! --> %d\n' % msg
                pass
    return

def create_database():
    con = sqlite3.connect(os.environ['HOME'] + '/.mailband.db')
    with con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Email(email_account TEXT,
                                                        email_title TEXT, 
                                                        email_text TEXT)""")
    os.chmod(os.environ['HOME'] + '/.mailband.db', 111)
    return
