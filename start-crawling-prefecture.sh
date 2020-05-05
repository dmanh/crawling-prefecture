#!/bin/bash
#for environment variables in the /home/dm/.profile 
. /home/dm/.profile
#for ChromeDriver is in the path
PATH=$PATH:/usr/local/bin/
#Execute the script 
/home/dm/station/crawling-prefecture/crawl_92.py