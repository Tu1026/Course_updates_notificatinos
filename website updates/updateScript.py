"""Monitors the given course and send update when a spot frees up

    Usage: change the url to the course, chagne the word looking for to however, many people is registered in the class
    , subscribe to the printed website to recieve notification
"""


from bs4 import BeautifulSoup
import time
from urllib.request import urlopen
import win32api
from notify_run import Notify

#Creates the notify channel
notify = Notify()
print(notify.register())
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
        break