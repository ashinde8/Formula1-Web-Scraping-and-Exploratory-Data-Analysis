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
import os
import pandas as pd

#2010 -2019

def run(year1,year2):
    
    url = 'https://www.formula1.com/en/results.html'
    folder_path = 'C:\\Users\\Lenovo\\Desktop\\Formula11'

    for i in range(year1, year2 + 1):
        
        file_yr = str(i)
        file_name = 'driver_standings_table' + file_yr + '.txt'

        fw=open(file_name,'w',encoding='utf8') # output file

        writer=csv.writer(fw,lineterminator='\n')                                    #create a csv writer for this file
        drivers_standings_link = url + '/' + file_yr + '/drivers.html'

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

            pos , driver_name , nationality , constructor_name , points = 'NA', 'NA', 'NA', 'NA', 'NA'
        
            pos_chunk = tr.find('td',{'class':'dark'})
            pos = pos_chunk.text.strip()
        
            driver_chunk = tr.find('td')
            #driver_tags = driver_chunk.find('a',{'class':'hide-for-mobile'})
            driver_tags = driver_chunk.find('a',{'href':re.compile('/en/results.html/'+ str(i) + '/drivers')})

            #driver = driver_tags.find('span',{'class':'hide-for-mobile'})
        
            driver_name = driver_tags.text.strip()
        
            nationality_chunk = tr.find('td',{'class':'dark semi-bold uppercase'})
            nationality = nationality_chunk.text.strip()
            
            constructor_chunk = tr.find('td')
            constructor_tags = constructor_chunk.find('a',{'class':'grey semi-bold uppercase Archivelink'})
            constructor_name = constructor_tags.text.strip()
            
            points_chunk = tr.find('td',{'class':'dark bold'})
            points = points_chunk.text.strip()
            
            writer.writerow([pos , driver_name , nationality , constructor_name , points]) # write to file             
        fw.close()
        
        var = str(i) + '_driver_standings'  
        var = str(var)
        
        new_path = os.path.join(folder_path, var)
        new_path = new_path + '.csv'
        
        drivers_standings = pd.read_csv(file_name, names = ['POS','DRIVER','NATIONALITY','CONSTRUCTOR','POINTS'], sep = ',')
        drivers_standings.to_csv(new_path, index = False, header=True)

run(2010,2012)


