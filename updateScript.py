"""Monitors the given course and send update when a spot frees up

    Usage: change the url to the course, chagne the word looking for to however, many people is registered in the class
    , subscribe to the printed website to recieve notification
"""


from bs4 import BeautifulSoup
import time
from urllib.request import urlopen
import ctypes
import smtplib
from dotenv import load_dotenv
import os
import winsound
import discord
import datetime
import gc


load_dotenv()

# def send_fb_message(words: str, uid: str):
#     """print the given string one word at a time to fb friend
#         Args: 
#             a string that contain multiple words, the uid of the fb friend
#             user input: username and password
#     """
#     username = str(input("Username: ")) 
#     client = fbchat.Client(username, getpass()) 
#     for word in words:
#         client.send(fbchat.models.Message(word),
#                 uid)
#         time.sleep(1)
#     client.logout()

## Personalized for myself
# def send_fb_message(word: str):
#     """print the given string one word at a time to fb friend
#         Args: 
#             a string that contain multiple words, the uid of the fb friend
#             user input: username and password
#     """
#     uid = os.getenv("uid")
#     username_fb = os.getenv("username2") 
#     passwrod_fb = os.getenv("password1")
#     client = fbchat.Client(username_fb, passwrod_fb)
#     client.send(fbchat.models.Message(word), uid)
#     client.logout()

def send_discord_message(word):
    TOKEN = os.getenv('DISCORD_TOKEN')
    client = discord.Client()

    @client.event
    async def on_ready():
        await client.get_channel(736117723322646528).send(f'Register for {word}RIGHT NOW!!!!!!!!!!!')
        await client.get_channel(736117723322646528).send(f'Register for {word}RIGHT NOW!!!!!!!!!!!')
        await client.get_channel(736117723322646528).send(f'Register for {word}RIGHT NOW!!!!!!!!!!!')
        await client.get_channel(736117723322646528).send(f'Register for {word}RIGHT NOW!!!!!!!!!!!')
        await client.get_channel(736117723322646528).send(f'Register for {word}RIGHT NOW!!!!!!!!!!!')
        await client.close()
       

    client.run(TOKEN)


#Reference from https://stackabuse.com/how-to-send-emails-with-gmail-using-python/
def send_email(username, password):
    """send email to the person who wishes to recieve notification
    """
    sent_from = username
    to = [noti_email]
    subject = 'Course registeration for ' + course
    body = 'The course you want has a seat open!!'
    message ='Subject: {}\n\n{}'.format(subject, body)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(username, password)
    server.sendmail(sent_from, to, message)
    server.close()

def update_loop():
## Keeps looping through the website until a spot is open
    while True:
        try: 
            text = soup.get_text()
            text_list = text.split()
            word_looking_for = "Registered:" + registered
            t = datetime.datetime.today()
            # if the amount of people registered has not changed keep looping
        except:
            time.sleep(10) 
            update_loop()
           
        if word_looking_for in text_list:
            # wait 10 seconds,
            print("No seats avaliable yet updating in 10 seconds")
            time.sleep(10)
            if t.hour >= 2 and t.hour <= 4:
                time_sleep = datetime.timedelta(hours=2, minutes=20)
                print(f'sleeping right now till 4.20 AM for{time_sleep.total_seconds()} seconds to avoid scheduled maintenence')
                time.sleep(time_sleep.total_seconds())
                t = datetime.datetime.today()
                print(f'waking up at time {t}') 
            # continue with the script,
            del text, text_list, word_looking_for, t
            gc.collect()
            continue
            
        # if the amout of people registered has changed do a pop up and send a notificaiton on the website
        else:
            # notify.send("register for " + course + " NOW")
            try:
                # log into server account to send message
                # config = ConfigParser()
                # config.read('config.ini')
                username = os.getenv("username1")
                password = os.getenv("password")
                # username = config.get("email", "username")
                # password = config.get("email", "password")
                # send_fb_message("register for " + course + "NOWWWWWWW")
                send_discord_message(course)
                send_email(username, password)
                print("email notificaiton sent")
            except:
                print("something went wrong with emailing stuff or FB stuff")
            ctypes.windll.user32.MessageBoxW(0, course, 'Spot is now open for', course)
            winsound.MessageBeep()
            break

#get information from user
course = input("what course are you looking for?")
noti_email = input("what is your email that you want to get notificaition at?")
url = input("What is the 'section' specific url that you want to get in" +
"(ex: https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=BIOL&course=234&section=921)?")
registered = input("How many people are registered in this section so far(only enter number ex: 100)?")
html = urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")
update_loop()

## Create notification channel
# notify = Notify()
# print(notify.register())
# print("go to this website if you want push notificaiton from browser")





