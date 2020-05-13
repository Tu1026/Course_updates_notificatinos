"""Monitors the given course and send update when a spot frees up

    Usage: change the url to the course, chagne the word looking for to however, many people is registered in the class
    , subscribe to the printed website to recieve notification
"""


from bs4 import BeautifulSoup
import time
from urllib.request import urlopen
import win32api
from notify_run import Notify
import smtplib
from cryptography.fernet import Fernet
from configparser import ConfigParser 




#get information from user
course = input("what course are you looking for?")
noti_email = input("what is your email that you want to get notificaition at?")

#Creates the notify channel
notify = Notify()
print(notify.register() + "go to this website for notification")
## Encrypt my email data
key = b'GV2cvMW4av8mR1o8G7OPrf1eSjGHPrR4-MoWBb76QmI='
cipher_suite = Fernet(key)
ciphered_text = b'gAAAAABeu3gEGRvWoRnyY1L90Hg_XcrLg_S-9pBE1j20MWrogxt2_0a8f1kEKDl77fn_qCVT4RuFWW-ZD-nh-f6R_See6d7kQg=='
uncipher_text = (cipher_suite.decrypt(ciphered_text)) 
print(uncipher_text)
## Keeps looping through the website until a spot is open
while True:
    url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=BIOL&course=234&section=921"
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    text_list = text.split()
    print("updating")
    word_looking_for = "Registered:100"
    

    # if the amount of people registered has not changed keep looping
    if word_looking_for in text_list:
        # wait 60 seconds,
        time.sleep(60)
        # continue with the script,
        continue
        
    # if the amout of people registered has changed do a pop up and send a notificaiton on the website
    else:
        full_text = soup.find_all("Registered:100")
        notify.send("register for course now")
        win32api.MessageBox(0, 'BIOL234', 'Course registeration')
        try:
            send_email()
        except:
            print("something went wrong with emailing stuff")
        break


#Reference from https://stackabuse.com/how-to-send-emails-with-gmail-using-python/
def send_email():
    """send email to the person who wishes to recieve notification
    """
    # log into server account to send message
    config = ConfigParser()
    config.read('config.ini')
    username = config.get("email", "username")
    password = config.get("email", "password")
    sent_from = username
    to = [noti_email]
    subject = 'Course registeration for ' + course
    body = 'The course you want has a seat open!!'
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    server = smtplib.SMTP_SSL(username, 465)
    server.ehlo()
    server.login(username, password)
    server.sendmail(sent_from, to, email_text)
    server.close()