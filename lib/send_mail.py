#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
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
        frame = LabelFrame(self.root, text="Select Accounts", padx=15, pady=15)
        frame.pack(fill='both', expand=1)
        self.acnts = [acnt for acnt in acnts.items()]
        self.sel = IntVar()
        for acnt in self.acnts:       
            v = self.acnts.index(acnt)
            box = Radiobutton(frame, text=acnt[0], value=v, variable=self.sel)
            box.pack(anchor=W)
        ok_button = Button(self.root, text='ok', command=self.msg_window)
        ok_button.pack()
        cancel_button = Button(self.root, text='cancel', command=self.cancel)
        cancel_button.pack()
        self.root.mainloop()
        
    def mail_session(self, msg):
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
            server.sendmail(acnt[0], recipent, self.msg)
            server.quit()
        except:
            self.msg_fail

    def ok_send(self):
        last_line = self.msg_input.index(END)
        self.msg = self.msg_input.get('1.0', last_line)
        self.recipent = self.entry.get()
        self.mail_session(self.msg)
        self.root.destroy()    

    def cancel(self):
        self.root.destroy()

    def msg_fail_cancel(self):
        self.fail_root.destroy()
        
    def msg_window(self):
        self.cancel()
        self.root = Tk()
        self.root.geometry("500x400+400+275")
        self.frame = Frame(self.root, bd=10)
        self.frame.pack(fill="both", expand=1)
        self.msg_input = Text(self.frame, wrap=WORD) 
        self.msg_input.pack(fill="both", expand=1) 
        self.entry = Entry(self.msg_input)
        self.entry.pack(fill=X, side=BOTTOM)
        self.ok_button = Button(self.root, text="ok", command=self.ok_send)
        self.ok_button.pack()
        self.cancel_button = Button(self.root, text="cancel", 
                                          command=self.cancel)
        self.cancel_button.pack()
        self.root.mainloop()

    @property
    def no_saved_acnts(self):
        self.root = Tk()
        self.root.geometry("275x150+400+275")
        message = Message(self.root, text="No Saved Accounts",
                          bd=4, justify='center', relief='raised')
        message.pack(fill='both', expand=1)
        close_button = Button(message, text='close', height=1, 
                              command=self.cancel, relief='groove')
        close_button.pack(side=BOTTOM, pady=20)
        self.root.mainloop()

    @property
    def msg_fail(self):
        self.fail_root = Tk()
        self.fail_root.geometry("275x150+400+275")
        message = Message(self.fail_root, text="Message Failed!",
                          bd=4, justify='center', relief='raised')
        message.pack(fill='both', expand=1)
        close_button = Button(message, text='close', height=1,
                              command=self.msg_fail_cancel, relief='groove')
        close_button.pack(side=BOTTOM, pady=20)
        self.fail_root.mainloop()

