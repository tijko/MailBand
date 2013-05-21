#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import poplib
import smtplib
import sqlite3
import os
from BeautifulSoup import BeautifulSoup


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
                    email = session.top(i, 30000)[1]   
                    soup = BeautifulSoup(' '.join(email))
                    msg = soup.text
                    front = msg.find('From: ')
                    back = msg.find('Content-Type:')
                    if back == -1 or back < front or back > front + 101:
                        back = front + 100
                    title = title_parse(msg[front:back])
                    if title:
                        print '\n[%d]    %s' % (i, title)
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
        for email in selection:
            try:
                cur = con.cursor()
                cur.execute("SELECT * FROM Email")
                mail = session.top(email, 10000)[1]
                soup = BeautifulSoup(' '.join(mail))
                msg = soup.text
                front = msg.find('From: ')
                back = msg.find('Content-Type:')
                if back == -1 or back < front or back > front + 101:
                    back = front + 100
                title = title_parse(msg[front:back])
                email_body = session.retr(email)[1]
                email_body = ' '.join(email_body)
                cur.execute("INSERT INTO Email VALUES(?,?,?)", (account,
                                                                title,
                                                                email_body))
                print '\nMessage %s saved!' % title 
            except poplib.error_proto:
                print '\nBad Selection! --> %s\n' % email
                pass 
    con.commit()
    con.close()
    return                

def read_account_mail(session, selection):
    for email in selection:
        try:
            email_body = session.retr(email)
            soup = BeautifulSoup(' '.join(email_body[1]))
            print "Message [%s]\n" % email
            print soup.text + '\n'
        except poplib.error_proto:
            print '\nBad Selection! --> %s\n' % email
            pass
    return

def delete_account_mail(session, selection):
    print "\nAre you sure you want to DELETE messages ==> %s" % (str(selection))
    while True:
        answer = raw_input("(y or n): ") 
        if answer.lower() == 'y' or answer.lower() == 'n':
            break
    if answer.lower() == 'y':
        for email in selection:
            try:
                session.dele(email)
                print '\nMessage Deleted!\n'
            except poplib.error_proto:
                print '\nBad Selection! --> %s\n' % email
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
