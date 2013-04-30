# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
from lib.mail_commands import Mail_Pool
from lib.mail_carrier import deliver 


def options():
    parser = argparse.ArgumentParser(description='''MailBand is an utility to help manage multiple e-mail accounts.  
                                                    MailBand is capable of reading and writing emails from your shell.
                                                    MailBand can back-up all your emails locally on your storage device.  
                                                    MailBand is compatible with: -hotmail -live -gmail -aol -msn''')
    p = parser.add_mutually_exclusive_group()
    p.add_argument('-a', '--add_acnt', help='add an e-mail account', action='store_true')
    p.add_argument('-c', '--show_acnts', help='list current email accounts', action='store_true')
    p.add_argument('-r', '--remove_acnt', help='remove an e-mail account', action='store_true')
    p.add_argument('-R', '--read', help='show all e-mails in accounts', action='store_true')
    p.add_argument('-F', '--fetch_stored', help='show all e-mail currently stored locally', action='store_true')
    p.add_argument('-D', '--delete_stored', help='delete selected e-mails from local storage', action='store_true')
    p.add_argument('-d', '--delete', help='delete selected e-mails', action='store_true')
    p.add_argument('-s', '--send', help='send an e-mail from selected account', action='store_true')
    p.add_argument('-w', '--write', help='write selected e-mails to local storage', action='store_true')
    parse = parser.parse_args()
    return parse

def main(opt):
    pool = Mail_Pool()
    if opt.add_acnt:
        pool.add_account()
    elif opt.remove_acnt:
        pool.remove_account()
    elif opt.show_acnts:
        pool.show_current_accounts()
    else:
        choices = pool.mail_box()
        if opt.read:
            deliver(choices, 'read')
        if opt.delete:
            deliver(choices, 'delete')
        if opt.send:
            pool.send_mail(choices)
        if opt.write:
            deliver(choices, 'write')
        if opt.fetch_stored:
            pool.fetch_stored(choices)
        if opt.delete_stored:
            return

if __name__ == '__main__':
    opt = options()
    main(opt)
