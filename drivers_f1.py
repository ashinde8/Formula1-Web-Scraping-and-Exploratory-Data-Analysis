# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 04:25:26 2020

@author: Lenovo
"""

# Formula 1 Web Scraping

from bs4 import BeautifulSoup
import re
import time
import requests
import csv
import pandas as pd

def run(year):
    
    url = 'https://www.formula1.com/en/results.html'

    fw=open('driver_standings_table.txt','w',encoding='utf8') # output file

    writer=csv.writer(fw,lineterminator='\n')                                    #create a csv writer for this file
    drivers_standings_link = url + '/' + str(year) + '/drivers.html'

    for i in range(5): # try 5 times

            #send a request to access the url
        response=requests.get(drivers_standings_link,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
        
        if response: # explanation on response codes: https://realpython.com/python-requests/#status-codes
            break # we got the file, break the loop
        else:time.sleep(2) # wait 2 secs
             
    html=response.text# read in the text from the file
        
    soup = BeautifulSoup(html,features ='html5lib') # parse the html 
        
    table = soup.find('table',{'class':'resultsarchive-table'} )
    body = table.find('tbody')
    table_rows = body.find_all('tr')
       
    for tr in table_rows:

        pos , driver , nationality , constructor , points = 'NA', 'NA', 'NA', 'NA', 'NA'
        
        pos_chunk = tr.find('td',{'class':'dark'})
        pos = pos_chunk.text.strip()
        
        
        driver_tags = tr.find('a',{'href':re.compile('/en/results.html/'+ str(year) + '/drivers')})
        constructor_tags = tr.find('a',{'href':re.compile('/en/results.html/'+ str(year) + '/team')})

        driver = driver_tags.find('span',{'class':'hide-for-mobile'})
        
        driver_name = driver.text.strip()
        
        nationality_chunk = tr.find('td',{'class':'dark semi-bold uppercase'})
        nationality = nationality_chunk.text.strip()
            
        constructor_name = constructor_tags.text.strip()
            
        points_chunk = tr.find('td',{'class':'dark bold'})
        points = points_chunk.text.strip()
            
        writer.writerow([pos , driver_name , nationality , constructor_name , points]) # write to file             
    fw.close()

run(2019)

drivers_2019_standings = pd.read_csv('driver_standings_table.txt', names = ['POS','DRIVER','NATIONALITY','CONSTRUCTOR','POINTS'], sep = ',')
print(drivers_2019_standings)

drivers_2019_standings.to_csv (r'C:\Users\Lenovo\Desktop\drivers_2019_standings.csv', index = False, header=True)
