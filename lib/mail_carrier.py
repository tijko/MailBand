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
            # give option of, say 10 newest or 10 oldest?
            print 'Emails %d for: %s' % (session.stat()[0], addr[0])
            if session.stat()[0] > 0:
                for i in xrange(1, session.stat()[0] + 1):
                    email_data = email.message_from_string('\n'.join(session.retr(i)[1]))   
                    sender = email_data['From']                     
                    if sender:
                        print '\n[%d]    %s' % (i, sender)
                    else:
                        pass
                selection = raw_input('\nSelect your e-mail numbers: ')
                # check if all are numbers
                if action == 'write':
                    save_local(session, addr[0], selection.split(','))
                if action == 'read':
                    read_account_mail(session, selection.split(','))
                if action == 'delete':
                    delete_account_mail(session, selection.split(','))
                session.quit()                               
        except poplib.error_proto:
            print '\nUsername or Password Error ==> %s\n' % addr[0]
            pass
    return

def save_local(session, account, selection):
    if not os.path.isfile(os.environ['HOME'] + '/.mailband.db'):
        create_database()
    con = sqlite3.connect(os.environ['HOME'] + '/.mailband.db')
    with con:
        for msg in selection:
            try:
                cur = con.cursor()
                cur.execute("SELECT * FROM Email")
                email_data = session.retr(msg)[1]
                email_data = email.message_from_string('\n'.join(email_data))
                account = email_data['To']
                title = email_data['Subject']
                for part in email_data.walk():
                    if email_data.get_content_type() == 'text/plain':
                        load = part.get_payload()
                        cur.execute("INSERT INTO Email VALUES(?,?,?)", (account,
                                                                        title,
                                                                        load))
                        print '\nMessage %s saved!' % title 
            except poplib.error_proto:
                print '\nBad Selection! --> %s\n' % msg
                pass 
    con.commit()
    con.close()
    return                

def read_account_mail(session, selection):
    for msg in selection:
        try:
            email_data = session.retr(msg)
            email_data = email.message_from_string('\n'.join(email_data[1]))
            print "Message [%s]\n" % email_data['Subject']
            for part in email_data.walk():
                if part.get_content_type() == 'text/plain':
                    for line in part.get_payload().split('\n'):
                        print line
        except poplib.error_proto:
            print '\nBad Selection! --> %s\n' % msg
            pass
    return

def delete_account_mail(session, selection):
    print "\nAre you sure you want to DELETE messages ==> %s" % (str(selection))
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
                print '\nBad Selection! --> %s\n' % msg
                pass
    return

def title_parse(title):
    title = title.replace('MIME-Version: 1.0', '')
    title = title.replace('In-Reply-To:', '')
    title = title.replace('Message-ID:', '')
    # reference rm?
    return title

def create_database():
    con = sqlite3.connect(os.environ['HOME'] + '/.mailband.db')
    with con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Email(email_account TEXT,
                                                        email_title TEXT, 
                                                        email_text TEXT)""")
    con.commit()
    con.close()
    os.chmod(os.environ['HOME'] + '/.mailband.db', 111)
    return
