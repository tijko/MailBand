#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from email.mime.text import MIMEText
import os
import smtplib
import simplejson


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
              'aol.com':'smtp.aol.com'
             }


class SendMail(object):

    def fetch_acnts(self):
        home_dir = os.environ['HOME']
        if os.path.isfile(home_dir + '/.mailband_accounts.txt'):
            with open(home_dir + '/.mailband_accounts.txt') as f:
                stored_acnts = simplejson.loads(f.read())
            if stored_acnts:
                self.choice_window(stored_acnts)
            else:
                self.no_saved_acnts
        else:
            self.no_saved_acnts
            
    def choice_window(self, acnts):
        self.root = Tk()
        self.root.geometry("275x200+400+275")
        frame = LabelFrame(self.root, text="Select an Account")
        frame.grid(row=0, rowspan=2, column=0, columnspan=2, 
                   padx=5, sticky=N+S+E+W)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.acnts = [acnt for acnt in acnts.items()]
        self.sel = IntVar()
        for acnt in self.acnts:       
            v = self.acnts.index(acnt)
            box = Radiobutton(frame, text=acnt[0], value=v, variable=self.sel)
            box.grid(row=v, sticky=W, pady=5)
        ok_button = Button(self.root, text='ok', command=self.msg_window)
        ok_button.grid(row=v + 2, column=0, sticky=S+W, padx=25, pady=10)
        cancel_button = Button(self.root, text='cancel', command=self.cancel)
        cancel_button.grid(row=v + 2, column=1, sticky=S+E, padx=25, pady=10)
        self.root.mainloop()
        
    def mail_session(self, msg):
        msg = MIMEText(msg)
        msg['Subject'] = self.subject
        self.msg = msg
        acnt = self.acnts[self.sel.get()]
        try:
            addr = acnt[0].split('@')[1]
            mail_server = _smtp_addr[addr]
            server = smtplib.SMTP(mail_server, _ports[mail_server])
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(acnt[0], acnt[1])
            recipent = self.recipent
            server.sendmail(acnt[0], recipent, msg.as_string())
            server.quit()
        except:
            self.msg_fail

    def ok_send(self):
        last_line = self.msg_input.index(END)
        self.msg = self.msg_input.get('1.0', last_line)
        self.recipent = self.to.get()
        self.subject = self.subject_entry.get()
        self.mail_session(self.msg)

    def cancel(self):
        self.root.destroy()

    def msg_fail_cancel(self):
        self.fail_root.destroy()
        self.cancel()
        
    def msg_window(self):
        self.cancel()
        self.root = Tk()
        self.root.geometry("500x475+400+275")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.msg_input = Text(self.root, wrap=WORD) 
        self.msg_input.grid(row=2, columnspan=2, sticky=N+S+E+W, padx=10)
        self.to = Entry(self.root)
        self.to.grid(row=0, columnspan=2, sticky=W+E, padx=70)
        self.to_label = Label(self.root, text='To:')
        self.to_label.grid(row=0, sticky=W, padx=10)
        self.subject_entry = Entry(self.root)
        self.subject_entry.grid(row=1, columnspan=2, sticky=W+E, padx=70, pady=10)
        self.subject_label = Label(self.root, text='Subject:')
        self.subject_label.grid(row=1, sticky=W, padx=10)
        self.ok_button = Button(self.root, text="ok", command=self.ok_send)
        self.ok_button.grid(row=3, sticky=S+W, padx=10, pady=10)
        self.cancel_button = Button(self.root, text="cancel", 
                                          command=self.cancel)

        self.cancel_button.grid(row=3, column=1, sticky=S+E, padx=10, pady=10)
        self.msg_input.focus_set()
        self.root.mainloop()

    @property
    def no_saved_acnts(self):
        self.root = Tk()
        self.root.geometry("275x150+400+275")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        message = Message(self.root, text="No Saved Accounts",
                          bd=4, justify='center', relief='raised')
        message.grid(row=0, column=0, columnspan=2, 
                     rowspan=2, sticky=S+N+E+W)
        close_button = Button(self.root, text='close', height=1, 
                              command=self.cancel, relief='groove')
        close_button.grid(row=1, column=1, sticky=S, pady=10, padx=110)
        self.root.mainloop()

    @property
    def msg_fail(self):
        self.fail_root = Tk()
        self.fail_root.geometry("275x150+400+275")
        self.fail_root.grid_rowconfigure(0, weight=1)
        self.fail_root.grid_columnconfigure(0, weight=1)
        message = Message(self.fail_root, text="Message Failed!",
                          bd=4, justify='center', relief='raised')
        message.grid(row=0, column=0, columnspan=2,
                        rowspan=2, sticky=S+N+E+W)
        close_button = Button(self.fail_root, text='close', height=1,
                              command=self.msg_fail_cancel, relief='groove')
        close_button.grid(row=1, column=1, sticky=S, pady=10, padx=110)
        self.fail_root.mainloop()

