#!/usr/bin/python
import os
import shutil
import smtplib
import random
import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

JESS_FBOOK_PICS="/home/brett/secondary/virtual_drives/vm_share/fbook_images/Jessica Graziano"
BRETT_FBOOK_PICS="/home/brett/secondary/virtual_drives/vm_share/fbook_images/Brett Broderick"
SHARED_FBOOK_PICS="/home1/broderi5/public_html/bwbroderick/vday/facebook_images"
MESSAGE_LIST_FILENAME="/home1/broderi5/public_html/bwbroderick/vday/song_lyrics.txt"
SMTP_SERVER="mail.broderick-tech.com"
SMTP_SERVER_PORT=26
GMAIL_ACCOUNT="vday@broderick-tech.com"
GMAIL_PASSWORD="PASSWORD"
RECIPIENTS=["APHONENUMBER@tmomail.net", "bwbroderick@gmail.com"]
MESSAGE_SUBJECT="Your Daily Love Song"
START_DATE="20150214"
START_SUBJECT="Happy Valentine's Day My Love!"
START_MESSAGE="""
Dear Jessica,
    I was standing in CVS trying to pick out a card that could even
begin to describe how much I love you. After reading nearly every card I
tought to myself poets, and songwriters are so lucky, they can apply their
craft for the ones they love to bring them happiness. 

Then I thought programmers are certainly nerdy but they can also be romantic. 
So every night for a week while you slept
I stayed up and built you a program. Sure it's not soft, or shiny, or sweet,
but it is the skill I am best at in this world and I want to do it for you, because
I LOVE YOU JESSICA.

First I wrote a script to download every picture of you on facebook. Then I downloaded
every picture of myself. I came up with an algorithm to determine which pictures we
were both in and I saved those. Then I put all the sweet nothings I could thinkg of and
more into a text file. I uploaded all of this onto a webserver and scheduled a
job to run everyday.

WAKE UP! Sorry I geeked out on you, long story short, everyday from now on at 9:30AM,
after I leave from work and you are on your commute, you
are going to get an email from a.boy.who.loves.a.girl@gmail.com
with different picture of me and you and a note about how I will always
love you. It's my geeky way of saying I am always thinking of you!

Love,
Brett
"""

def get_file_list(directory):
    file_list = []
    for dirname, dirnames, filenames in os.walk(directory):
        # print path to all filenames.
        for filename in filenames:
            full_path_filename = os.path.join(dirname, filename)
            parent_dir = os.path.basename(os.path.normpath(dirname))
            relative_filename = os.path.join(parent_dir, filename)
            if ".jpg" in full_path_filename:
                file_list.append(relative_filename)
    return file_list

def find_shared_pics():
    jess_pics = get_file_list(JESS_FBOOK_PICS)
    brett_pics = get_file_list(BRETT_FBOOK_PICS)
    return set(jess_pics) & set(brett_pics)

def create_shared_pics_dir():
    shared_list = find_shared_pics()
    for picture in shared_list:
        src = os.path.join(BRETT_FBOOK_PICS, picture)
        dst = os.path.join(SHARED_FBOOK_PICS, os.path.basename(picture))
        shutil.copyfile(src, dst)

def send_mms(subject, message, image_filename, to=RECIPIENTS):
    with open(image_filename, 'rb') as image:
        image_data = image.read()
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = "a.boy.who.loves.a.girl.15@gmail.com"

    text = MIMEText(message)
    msg.attach(text)
    print "Sending image: " + image_filename
    image = MIMEImage(image_data, "jpeg", name=os.path.basename(image_filename))
    msg.attach(image)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_SERVER_PORT)
    server.starttls()
    server.login(GMAIL_ACCOUNT, GMAIL_PASSWORD)
    
    for recipient in to: 
        msg['To'] = recipient
        server.sendmail(GMAIL_ACCOUNT, recipient, msg.as_string())

def get_random_image():
    file_list = os.listdir(SHARED_FBOOK_PICS)
    return os.path.join(SHARED_FBOOK_PICS, random.choice(file_list))

def get_random_message():
    with open(MESSAGE_LIST_FILENAME, 'r') as message_list_file:
        message_list = message_list_file.readlines()
    message_list = [line.rstrip('\n') for line in message_list]
    return random.choice(message_list)

def play(only_play_song_once=False):
    """Seranades my lover with a beautiful song of adoration and romance"""
    today = int(datetime.datetime.today().strftime("%Y%m%d"))
    print "Today: "
    print today
    print "Start Date: "
    print START_DATE
    if today < int(START_DATE):
        print "Not VDAY yet, quiting"
        return
    if today == int(START_DATE):
        message = START_MESSAGE
        subject = START_SUBJECT
        play_helper(MESSAGE_SUBJECT, message)
        play_helper()
        play_helper()
    else:
        play_helper()
    
    if only_play_song_once:
        os.remove(image)

def play_helper(subject=MESSAGE_SUBJECT, message=None, image=None):
    if not image:
        image = get_random_image()
    if not message:
        message = get_random_message()
    
    send_mms(MESSAGE_SUBJECT, message, image)


