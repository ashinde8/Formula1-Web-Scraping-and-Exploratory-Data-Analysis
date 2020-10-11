# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 04:28:54 2020

@author: Lenovo
"""

# Formula 1 Web Scraping

from bs4 import BeautifulSoup
import re
import time
import requests
import csv
import pandas as pd
import os

def run(year1,year2):
    
    url = 'https://www.formula1.com/en/results.html'
    folder_path = 'C:\\Users\\Lenovo\\Desktop\\Formula1'

    for yr in range(year1,year2):
        
        file_yr = str(yr)

        file_name = 'constructor_standings' + file_yr + '.txt'
        fw = open(file_name,'w',encoding='utf8') # output file

        writer=csv.writer(fw,lineterminator='\n')                                    #create a csv writer for this file
        constructor_standings_link = url + '/' + str(yr) + '/team.html'
    
        for i in range(5): # try 5 times

            #send a request to access the url
            response=requests.get(constructor_standings_link,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
        
            if response: # explanation on response codes: https://realpython.com/python-requests/#status-codes
                break # we got the file, break the loop
            else:time.sleep(2) # wait 2 secs
             
        html=response.text     # read in the text from the file
        soup = BeautifulSoup(html,features ='html5lib') # parse the html 
        
        table = soup.find('table',{'class':'resultsarchive-table'} )
        body = table.find('tbody')
        table_rows = body.find_all('tr')
       
        for tr in table_rows:

            pos , constructor , points = 'NA', 'NA', 'NA'
        
            pos_chunk = tr.find('td',{'class':'dark'})
            pos = pos_chunk.text.strip()
                      
            constructor_tags = tr.find('a',{'href':re.compile('/en/results.html/'+ str(yr) + '/team')})
            constructor = constructor_tags.text.strip()
            
            points_chunk = tr.find('td',{'class':'dark bold'})
            points = points_chunk.text.strip()
            
            writer.writerow([pos, constructor, points]) # write to file 
            
        fw.close()
            
        var = str(yr) + '_Constructor_Standings'  
        var = str(var)
        
        new_path = os.path.join(folder_path, var)
        new_path = new_path + '.csv'
            
        constructor_standings = pd.read_csv(file_name, names = ['POS','CONSTRUCTOR','POINTS'], sep = ',')
        constructor_standings.to_csv(new_path, index = False, header=True)

run(2000,2010)

