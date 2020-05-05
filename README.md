# Introduction 

This project checks the website http://www.hauts-de-seine.gouv.fr/booking/create/8485 to see whether there's a slot for the titre de sejour in the website. 

# Prerequisites 

## Valid gmail username and password 
You need a valid gmail username and password to send to the destination email adress a notification message. Make sure that you disable the "Control acess to less secure apps" (https://myaccount.google.com/lesssecureapps). 

## Dependencies
First, you need to install dependencies: 
```bash
pip install -r requirements.txt
```

## ChomeDriver for selenium
* Install Google Chrome and Google ChromeDriver at: https://chromedriver.chromium.org/ 
* Put the directory of Google Chrome and Google ChromeDriver executive files in the system's path. 

## Run headless selenium
You can either run with the Google Chrome header (with the browser open and closed graphically) or headlessly (without). In linux system, you have to install `xvfb`:

```bash
sudo apt-get install xvfb
```

## Run Crontab

If you want to run the script periodically (every 10 minutes) in linux, you can use crontab: 

```bash
*/10 * * * * bash /home/dm/production/start-crawling-prefecture.sh
```
In order for the crontab job to run, you need to add environment variables at the end of your `.profile` file in `/home/dm/.profile`:
```bash
export GMAIL_USERNAME="your_gmail_username@gmail.com"
export GMAIL_PASSWORD="your_gmail_password"
export MAIL_DEST="your_mail@destination"
export PNGS_DIR="/home/dm/pngs"
export LOGS_DIR="/home/dm/logs"
```
You might need to do `source /home/dm/.profile` to activate these changes. 
