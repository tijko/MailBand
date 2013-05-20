# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import simplejson
import sqlite3
import smtplib
import os


_ports = {'pop.gmail.com':995,
          'smtp.gmail.com':587,
          'pop3.live.com':995,
          'smtp.live.com':587,
          'pop.aol.com':995,
          'smtp.aol.com':587
         }

_smtp_addr = {'gmail.com':'smtp.gmail.com',
              'msn.com':'smtp.email.live.com',
              'hotmail.com':'smtp.live.com',
              'live.com':'smtp.live.com',
              'aol.com':'smtp.aol.com'
             }            


class Mail_Pool(object):

    def __init__(self):
        self.home_dir = os.environ['HOME']
        if os.path.isfile(self.home_dir + '/.mailband_accounts.txt'):
            with open(self.home_dir + '/.mailband_accounts.txt') as f:
                self.stored_acnts = simplejson.loads(f.read())
        else:
            self.stored_acnts = dict() 

    def mail_box(self):
        self.show_current_accounts()
        if self.stored_acnts:
            accounts = list()
            print '    If you want more than one account selected, separate choices by commas.'
            print '      example: --> 1,3'
            mailbox_choices = raw_input("\nSelect which accounts to use e-mails from?: ")
            for i in list(enumerate(self.stored_acnts.keys(), 1)):
                if str(i[0]) in mailbox_choices.split(','):
                    accounts.append([i[1], self.stored_acnts[i[1]]])
            if not accounts:
                print '\nBad Selection!\n'
                return
            return accounts

    def add_account(self):
        acc_name = raw_input("\nEnter a valid e-mail address: ")
        if '@' not in acc_name or not _smtp_addr.get(acc_name.split('@')[1]):
            print '\nInvalid e-mail account!'
            print '\nMailBand is compatible with:'
            print '    --hotmail\n    --gmail\n    --live\n    --aol\n    --msn\n'   
            return
        passwrd = raw_input("Now, enter that address' password: ")
        self.stored_acnts.update({acc_name:passwrd})
        with open(self.home_dir + '/.mailband_accounts.txt', 'w') as f:
            f.write(simplejson.dumps(self.stored_acnts))
        self.show_current_accounts()
        return

    def remove_account(self):
        self.show_current_accounts()
        if self.stored_acnts:
            print '    If you want more than one account selected, separate choices by commas.'
            print '      example: --> 1,3'
            acnt_name = raw_input("\nSelect the accounts you want to remove: ")
            for acnt_key in list(enumerate(self.stored_acnts.keys(), 1)):
                if str(acnt_key[0]) in acnt_name.split(','):
                    self.stored_acnts.pop(acnt_key[1])
            with open(self.home_dir + '/.mailband_accounts.txt', 'w') as f:
                f.write(simplejson.dumps(self.stored_acnts))
            self.show_current_accounts()
        return
    
    def show_current_accounts(self):
        if self.stored_acnts:
            print "\nYour accounts are ==>"
            for acnt in self.stored_acnts.keys():
                num = self.stored_acnts.keys().index(acnt) + 1
                print "    [%d] %s" % (num, acnt)
            print ''
        else:
            print "\nYou don't have any accounts saved!\n"
            return

    def send_mail(self, boxes):
        for box in boxes:
            addr = box[0].split('@')[1]
            mail_server = _smtp_addr[addr]
            server = smtplib.SMTP(mail_server, _ports[mail_server])
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(box[0], box[1])
            to = raw_input('\nTo: ')
            msg = raw_input('\nEnter message: ')
            server.sendmail(box[0], to, msg)
            print '\nMessage Sent!\n'
        return

    def fetch_stored(self, choices):
        if not os.path.isfile(os.environ['HOME'] + '/.mailband.db'):
            print '\nNo mail saved!\n'
            return
        con = sqlite3.connect(os.environ['HOME'] + '/.mailband.db')
        with con:
            cur = con.cursor()
            for i in choices:
                cur.execute('SELECT * FROM Email WHERE email_account=?', [i[0]])
                emails = cur.fetchall()    
                if emails:
                    email_list = zip(range(1, len(emails) + 1), [email[1] for email in emails])
                    for email in email_list:
                        print "\n    [%d] %s" % (email[0], email[1])
                    read_choice = raw_input("\nSelect the emails to display: ")
                    show = [v for v in email_list if str(v[0]) in read_choice.split(',')]
                    for j in show:
                        for e in emails:
                            if j[1] in e:
                                print "\n[%d] %s" % (j[0], j[1])   
                                print e[2]
            print '-' * 40
        con.close()
        return

    def delete_stored(self, choices):
        if not os.path.isfile(os.environ['HOME'] + '/.mailband.db'):
            print '\nNo mail saved!\n'
            return
        con = sqlite3.connect(os.environ['HOME'] + '/.mailband.db')
        with con:
            cur = con.cursor()
            for i in choices:
                cur.execute('SELECT * FROM Email WHERE email_account=?', [i[0]])
                emails = cur.fetchall()
                if emails:
                    email_list = zip(range(1, len(emails) + 1), [email[1] for email in emails])
                    for email in email_list:                        
                        print "\n    [%d] %s" % (email[0], email[1])
                    delete_choice = raw_input("\nSelect the emails to delete: ")
                    for email in email_list:
                        if str(email[0]) in delete_choice.split(','):
                            cur.execute('DELETE FROM Email WHERE email_title=?', [email[1]])
        con.commit()
        con.close()                
        return
