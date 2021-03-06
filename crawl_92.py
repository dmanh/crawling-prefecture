#!/home/dm/anaconda3/envs/crawling/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 10:11:44 2020

@author: duy-m
@goals:
    * Crawl the 92 rendez-vous 
"""
import logging
import os
import time
from selenium import webdriver
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pyvirtualdisplay import Display


# Email login to send email. You can replace by your choice.  
USERNAME = os.environ["GMAIL_USERNAME"]
PASSWORD = os.environ["GMAIL_PASSWORD"]
# Email address to send to 
SENDTO = os.environ["MAIL_DEST"]
# Saved screen and logs directory, change to your convenience. 
SCREENDIR = os.environ["PNGS_DIR"]
LOGDIR = os.environ["LOGS_DIR"]

URL = r"http://www.hauts-de-seine.gouv.fr/booking/create/8485"

#---------------- Create and configure logger -------------------------------
logging.basicConfig(filename=os.path.join(LOGDIR,"crawling-prefecture-92.log"), 
                    format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO, filemode='a') 
#Creating an object 
logger = logging.getLogger() 

def send_notification():
    msg = MIMEMultipart()
    msg['subject'] = 'Plage horaire libre disponible'
    msg['from'] = USERNAME
    msg['to'] = SENDTO
    message = 'Allez directement sur le site et enregistrer:' + URL
    msg.attach(MIMEText(message))
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    # s.ehlo()
    s.login(USERNAME , PASSWORD)
    s.sendmail(USERNAME, SENDTO , msg.as_string())
    s.quit()

def run_header():
    logger.info("----------------------- START ---------------------------")
    
    try: 
        driver = webdriver.Chrome()
        
        # Get to the website
        driver.get(URL)
        driver.maximize_window()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.save_screenshot(os.path.join(SCREENDIR, 'screen0.png'))
        time.sleep(5)
        logger.info("Sleeping 5 seconds: 1st")

        try:
            driver.find_element_by_link_text("Accepter").click()
            logger.info("Passe accepter")
        except:
            logger.warning("There's no pass accepter")
            pass
        
        
        driver.maximize_window()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        checkbox = driver.find_element_by_id("condition")
        checkbox.click()
        driver.save_screenshot(os.path.join(SCREENDIR, 'screen1.png'))
        time.sleep(5)
        logger.info("Sleeping 5 seconds: 2nd")
        
        driver.maximize_window()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        checkbox = driver.find_element_by_name("nextButton")
        checkbox.click()
        driver.save_screenshot(os.path.join(SCREENDIR, 'screen2.png'))
        time.sleep(5)
        logger.info("Sleeping 5 seconds: 3rd")
        
        
        formbk = driver.find_element_by_id("FormBookingCreate")
        if not formbk.text.startswith("Il n'existe plus de plage horaire"):
            # Send notification email
            logger.info("Good news")
            send_notification()
        else:
            logger.info(formbk.text)
        
        time.sleep(5)
        logger.info("Sleeping 5 seconds: 4th")
        driver.quit()
    except Exception as err: 
        logger.error("Exception: " + str(err))
        pass
    
    logger.info("----------------------- FINISHED ------------------------\n")
    
    
def execute():
    if os.name == "nt": # windows
        run_header()
    else: # linux to run headlessly
        display = Display(visible=0, size=(1920, 1080))
        display.start()
        run_header()
        display.stop()

if __name__ == '__main__':
    execute()