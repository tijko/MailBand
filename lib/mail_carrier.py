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

_smtp_addr = {'gmail.com':'smtp.gmail.com',
              'msn.com':'smtp.email.live.com',
              'hotmail.com':'smtp.live.com',
              'live.com':'smtp.live.com',
              'aol.com':'smtp.aol.com'
             }

_ports = {'pop.gmail.com':995,
          'smtp.gmail.com':587,
          'pop3.live.com':995,
          'smtp.live.com':587,
          'pop.aol.com':995,
          'smtp.aol.com':587
         }


class Carrier(object):
    
    @classmethod
    def deliver(self, address, action): 
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
                if session.stat()[0] < 1:
                    break
                for i in xrange(1, session.stat()[0] + 1):
                    email = session.top(i, 30000)[1]   
                    soup = BeautifulSoup(' '.join(email))
                    msg = soup.text
                    front = msg.find('From: ')
                    back = msg.find('Content-Type:')
                    if back == -1 or back < front or back > front + 101:
                        back = front + 100
                    title = self.title_parse(msg[front:back])
                    if title:
                        print '\n[%d]    %s' % (i, title)
                    else:
                        pass
                selection = raw_input('\nSelect your e-mail numbers: ')
                if action == 'write':
                    self.save_local(session, addr[0], selection.split(','))
                    print '\nMail saved!\n'
                if action == 'read':
                    self.read_account_mail(session, selection.split(','))
                if action == 'delete':
                    self.delete_account_mail(session, selection.split(','))
                session.quit()                               
            except poplib.error_proto:
                print '\nUsername or Password Error ==> %s\n' % addr[0]
                pass
        return

    @classmethod
    def save_local(self, session, account, selection):
        if not os.path.isfile(os.environ['HOME'] + '/.mailband.db'):
            self.create_database()
        con = sqlite3.connect(os.environ['HOME'] + '/.mailband.db')
        with con:
            for email in selection:
                cur = con.cursor()
                cur.execute("SELECT * FROM Email")
                num_mail = len(cur.fetchall()) + 1
                mail = session.top(email, 10000)[1]
                soup = BeautifulSoup(' '.join(mail))
                msg = soup.text
                front = msg.find('From: ')
                back = msg.find('Content-Type:')
                if back == -1 or back < front or back > front + 101:
                    back = front + 100
                title = self.title_parse(msg[front:back])
                email_body = session.retr(email)[1]
                email_body = ' '.join(email_body)
                cur.execute("INSERT INTO Email VALUES(?,?,?,?)", (num_mail,
                                                                account,
                                                                title,
                                                                email_body))
        con.commit()
        con.close()
        return                

    @classmethod
    def read_account_mail(self, session, selection):
        for email in selection:
            email_body = session.retr(email)
            soup = BeautifulSoup(' '.join(email_body[1]))
            print "Message %s\n" % email
            print soup.text + '\n'
        return

    @classmethod    
    def delete_account_mail(self, session, selection):
        print "\nAre you sure you want to DELETE messages ==> %s" % (str(selection))
        while True:
            answer = raw_input("(y or n): ") 
            if answer.lower() == 'y' or answer.lower() == 'n':
                break
        if answer.lower() == 'y':
            for email in selection:
                session.dele(email)
            print "\nMessages Deleted!\n" 
        return

    @classmethod
    def title_parse(self, title):
        title = title.replace('MIME-Version: 1.0', '')
        title = title.replace('In-Reply-To:', '')
        title = title.replace('Message-ID:', '')
        # reference rm?
        return title

    @staticmethod
    def create_database():
        con = sqlite3.connect(os.environ['HOME'] + '/.mailband.db')
        with con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS Email(email_id INTEGER,
                                                            email_account TEXT,
                                                            email_title TEXT, 
                                                            email_text TEXT)""")
        con.commit()
        con.close()
        return
