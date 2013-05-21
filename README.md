MailBand
========

MailBand is an email utility to help manage multiple accounts.  It is able to 
read and write emails from your desktop and you can also back-up all of your
emails into a database stored on your local device.

MailBand is compatible with: hotmail, live, gmail, msn, aol.
If you want it to work with yahoo and lycos these services are about $20/yr.

#### usage
    
In order to use MailBand, you will need to be running under root access.  The files
created (accounts file and mail database) will be root-protected, no one other than 
root can read or write to these.

You can get a list of options by calling `main.py` in MailBands path with `-h` as an
option.

    sudo python main.py -h

    usage: main.py [-h] [-a | -c | -r | -R | -F | -D | -d | -s | -w]

    MailBand is an utility to help manage multiple e-mail accounts. MailBand is
    capable of reading and writing emails from your shell. MailBand can back-up
    all your emails locally on your storage device. MailBand is compatible with:
    -hotmail -live -gmail -aol -msn

    optional arguments:
      -h, --help           show this help message and exit
      -a, --add_acnt       add an e-mail account
      -c, --show_acnts     list current email accounts
      -r, --remove_acnt    remove an e-mail account
      -R, --read           show all e-mails in accounts
      -F, --fetch_stored   show all e-mail currently stored locally
      -D, --delete_stored  delete selected e-mails from local storage
      -d, --delete         delete selected e-mails
      -s, --send           send an e-mail from selected account
      -w, --write          write selected e-mails to local storage


By using the `-a` argument you can add an email account to the list of saved accounts.

    sudo python main.py -a

    Enter a valid e-mail address: foouser@gmail.com
    Now, enter that address' password: foopass

    Your accounts are ==>
        [1] foofoo@gmail.com
        [2] bazbaz@aol.com
        [3] baz@hotmail.com
        [4] foouser@gmail.com
        [5] foobar@gmail.com

Just enter a valid account information at the prompts and the data will be saved to a
dotfile in your home directory.
