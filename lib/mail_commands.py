# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import simplejson
from mail_carrier import Carrier
import sqlite3
import os


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
        if '@' not in acc_name or not _pop_addr.get(acc_name.split('@')[1]):
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
            for acnt in list(enumerate(self.stored_acnts.keys(), 1)):
                if str(acnt[0]) in acnt_name:
                    self.stored_acnts.pop(acnt[1])
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

    def delete_stored(self):
        return

    def send_mail(self):
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
                for email in emails:
                    print "\n    [%d] %s" % (email[0], email[2])
                read_choice = raw_input("\nSelect the emails to display: ")
                show = [v for v in emails if str(v[0]) in read_choice.split(',')]
                for j in show:
                    print "\n[%d] %s" % (j[0], j[2])   
                    print j[3]
        con.close()
        print ''
        return



