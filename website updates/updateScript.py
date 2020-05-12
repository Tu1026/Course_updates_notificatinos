# Import requests (to download the page)
import requests

# Import BeautifulSoup (to parse what we download)
from bs4 import BeautifulSoup

# Import Time (to add a delay between the times the scape runs)
import time

from urllib.request import urlopen

# Import smtplib (to allow us to email)
import smtplib

import win32api
from notify_run import Notify

# This is a pretty simple script. The script downloads the homepage of VentureBeat, and if it finds some text, emails me.
# If it does not find some text, it waits 60 seconds and downloads the homepage again.
notify = Notify()
print(notify.register())
# while this is true (it is true by default),
while True:
    # set the url as VentureBeat,
    url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=BIOL&course=234&section=921"
    # set the headers like we are a browser,
    html = urlopen(url).read()
    # download the homepage
    # parse the downloaded homepage and grab all text, then,
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    text_list = text.split()
    print("updating")
    word_looking_for = "Registered:100"
    

    # if the number of times the word "Google" occurs on the page is less than 1,
    if word_looking_for in text_list:
        # wait 60 seconds,
        time.sleep(60)
        # continue with the script,
        continue
        
    # but if the word "Google" occurs any other number of times,
    else:
        full_text = soup.find_all("Registered:100")
        notify.send("register for course now")
        win32api.MessageBox(0, 'BIOL234', 'Course registeration')
        
        break