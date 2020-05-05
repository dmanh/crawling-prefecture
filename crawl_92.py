#!/home/dm/anaconda3/envs/crawling/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 10:11:44 2020

@author: duy-m
@goals:
    * Crawl the 92 rendez-vous 
"""

from time import gmtime, strftime
import os
import time
from selenium import webdriver
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pyvirtualdisplay import Display

# Email login to send email. You can replace by your choice.  
USERNAME = os.environ["GMAIL_USERNAME"]
PASSWORD = os.environ["GMAIL_PASSWORD"]
# Email address to send to 
SENDTO = os.environ["MAIL_DEST"]

# Saved screen directory
SCREENDIR = os.environ["PNGS_DIR"]

def run():
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()))

    display = Display(visible=0, size=(1920, 1080))
    display.start()
    
    driver = webdriver.Chrome()
    URL = r"http://www.hauts-de-seine.gouv.fr/booking/create/8485"
    
    # Get to the website
    driver.get(URL)
    driver.maximize_window()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.save_screenshot(os.path.join(SCREENDIR, 'screen0.png'))
    time.sleep(5)
    
    try:
        driver.find_element_by_link_text("Accepter").click()
        print ("Passe accepter")
    except:
        pass
    
    
    driver.maximize_window()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    checkbox = driver.find_element_by_id("condition")
    checkbox.click()
    driver.save_screenshot(os.path.join(SCREENDIR, 'screen1.png'))
    time.sleep(5)
    
    driver.maximize_window()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    checkbox = driver.find_element_by_name("nextButton")
    checkbox.click()
    driver.save_screenshot(os.path.join(SCREENDIR, 'screen2.png'))
    time.sleep(5)
    
    
    formbk = driver.find_element_by_id("FormBookingCreate")
    if not formbk.text.startswith("Il n'existe plus de plage horaire libre pour votre demande de rendez-vous."):
        # Send notification email
        print ("Good news")
        msg = MIMEMultipart()
        msg['subject'] = 'Plage horaire libre disponible'
        msg['from'] = USERNAME
        msg['to'] = SENDTO
        message = 'Allez directement sur le site et enregistrer:'
        msg.attach(MIMEText(message))
        s = smtplib.SMTP('smtp.gmail.com:587')
        s.ehlo()
        s.starttls()
        # s.ehlo()
        s.login(USERNAME , PASSWORD)
        s.sendmail(USERNAME, SENDTO , msg.as_string())
        s.quit()
    else:
        print (formbk.text)
    
    time.sleep(10)
    driver.quit()
    display.stop()
    
    print ("Finished-------------")
    
if __name__ == '__main__':
    try:
        run()
    except Exception as err:
        print ("Exception: " + str(err))
        pass