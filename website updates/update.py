import vlc  # needed for the music feature
import hashlib
import os
import time
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from pushover import init, Client  # push notifications on your phone
# set the path of the music if u use the feature
# make sure to set up pushover on your phone before u use it


def check_for_update():

    if(os.path.isfile("website.txt")):

        req = Request(url)
        try:
            response = urlopen(req)
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines
                  for phrase in line.split(" "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        file = open("website_new.txt", "w")
        file.write(text)
        file.close()
        hasher = hashlib.md5()
        with open('website_new.txt', 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        global new_md5sum
        new_md5sum = hasher.hexdigest()
    else:

        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines
                  for phrase in line.split(" "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        file = open("website.txt", "w")
        file.write(text)
        file.close()
        hasher = hashlib.md5()
        with open('website.txt', 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        global original_md5sum
        original_md5sum = hasher.hexdigest()
        check_for_update()


def main():

    global url
    url = input("Paste the URL you want to check for updates: ")
    global push
    while True:
        temp = input("\nDo you want to get a notification \
to your phone when the website has been changed? (y/n): ")
        if (temp != "y" and temp != "n"):
            print("Error: Please enter y or n")
        else:
            if temp == "y":
                push = True
                print("Notifications to your phone have been turned ON\n")
                break
            else:
                print("Notifications to your phone have been turned OFF\n")
                break

    global music
    while True:
        temp = input("Do you want to play a song \
when the website has been changed? (y/n): ")
        if (temp != "y" and temp != "n"):
            print("Error: Please enter y or n")
        else:
            if temp == "y":
                music = True
                print("The music feature has been turned ON\n")
                break
            else:
                print("The music feature has been turned OFF\n")
                break

    global update_timer
    while True:
        temp = input("How often do you want to check \
the website for updates? Enter it in seconds (min. 20): ")

        if (temp.isdigit()):
            temp = int(temp)
            if temp > 19:
                print("The website will be checked for \
updates every " + str(temp) + " seconds\n")
                update_timer = temp
                break
            else:
                print("Make sure to enter a value bigger than 19\n")
        else:
            print("Please enter an integer (which has to be bigger than 19)\n")

    path = os.path.dirname(os.path.realpath(__file__))
    try:
        os.remove(path + "/website.txt")
    except OSError:
        pass
    try:
        os.remove(path + "/website_new.txt")
    except OSError:
        pass
    original_md5sum = ""
    new_md5sum = ""
    check_for_update()
    mainloop()


def mainloop():

    while True:

        check_for_update()
        '''
        print("Original: ", original_md5sum)
        print("New: ", new_md5sum)
        '''
        if original_md5sum == new_md5sum:
            print("Website hasn't been updated yet... " +
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            print("Website hat been updated! " +
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            if push is True:
                init("<token>")
                Client("<client_id>\
").send_message("Website has been updated!", title="Website update")

            if music is True:
                # example: file:///home/anon/Music/song.mp3
                p = vlc.MediaPlayer("file://<path>")
                p.play()
                time.sleep(60)
                p.stop()
            break
        time.sleep(update_timer)


main()