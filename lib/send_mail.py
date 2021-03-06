#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from email.mime.text import MIMEText
import os
import time
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
                self.msg_win('none_saved')
        else:
            self.msg_win('none_saved')
            
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
        
    def mail_session(self):
        if self.save.get():
            self.save_message()
        msg = MIMEText(self.msg)
        msg['Subject'] = self.subject
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
            self.msg_win('fail')
            return
        self.msg_input.delete('0.0', END)
        self.to.delete(0, END)
        self.subject_entry.delete(0, END)
        self.msg_win('sent')

    def save_message(self):
        with open(os.getcwd() + '/.sent_mail', 'a') as f:
            f.write("=" * 5 + (' %s ' % time.ctime()) + "=" * 5 + '\n')
            f.write("To: %s\n" % self.recipent)
            f.write("Subject: %s\n" % self.subject)
            f.write(self.msg + '\n')

    def ok_send(self):
        last_line = self.msg_input.index(END)
        self.msg = self.msg_input.get('1.0', last_line)
        self.recipent = self.to.get()
        self.subject = self.subject_entry.get()
        self.mail_session()

    def cancel(self):
        self.root.destroy()

    def msg_win_close(self):
        self.msg_win_root.destroy()

    def msg_window(self):
        self.cancel()
        self.root = Tk()
        self.root.geometry("500x525+400+75")
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
        self.save = IntVar()
        self.save_mail = Checkbutton(self.root, text='Save Email', variable=self.save)
        self.save_mail.grid(row=3, sticky=W, padx=10, pady=10)
        self.ok_button = Button(self.root, text="ok", command=self.ok_send)
        self.ok_button.grid(row=4, sticky=S+W, padx=10, pady=10)
        self.cancel_button = Button(self.root, text="close", 
                                          command=self.cancel)
        self.cancel_button.grid(row=4, column=1, sticky=S+E, padx=10, pady=10)
        self.to.focus_set()
        self.root.mainloop()

    def msg_win(self, alert):
        self.msg_win_root = Tk()
        self.msg_win_root.geometry("275x150+400+275")
        self.msg_win_root.grid_rowconfigure(0, weight=1)
        self.msg_win_root.grid_columnconfigure(0, weight=1)
        if alert == 'none_saved':
            text_msg = "No Saved Accounts"
        elif alert == 'fail':
            text_msg = "Message Failed!"
        else:
            text_msg = "Message Sent!"			
        message = Message(self.msg_win_root, text=text_msg,
                          bd=4, justify='center', relief='raised')
        message.grid(row=0, column=0, columnspan=2, 
                     rowspan=2, sticky=S+N+E+W)
        close_button = Button(self.msg_win_root, text='close', height=1, 
                              command=self.msg_win_close, relief='groove')
        close_button.grid(row=1, column=1, sticky=S, pady=10, padx=110)
        self.msg_win_root.mainloop()
