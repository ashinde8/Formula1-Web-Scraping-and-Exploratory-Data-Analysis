# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 02:35:52 2020

@author: Lenovo
"""

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

    
    for yr in range(year1,year2 + 1):

        file_yr = str(yr)
        file_name = 'race_results_table_' + file_yr +'.txt'
        
        fw=open(file_name,'w',encoding='utf8') # output file
        
        writer=csv.writer(fw,lineterminator='\n')   
            #create a csv writer for this file
        races_result_link = url + '/' + str(yr) + '/races.html'

        for i in range(5): # try 5 times

            response=requests.get(races_result_link,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
        
            if response: # explanation on response codes: https://realpython.com/python-requests/#status-codes
                break # we got the file, break the loop
            else:time.sleep(2) # wait 2 secs
             
        html=response.text# read in the text from the file
        soup = BeautifulSoup(html,features ='html5lib') # parse the html 
        
        table = soup.find('table',{'class':'resultsarchive-table'} )
        body = table.find('tbody')
        table_rows = body.find_all('tr')
 
        for tr in table_rows:

            grand_prix , date , winner , constructor , laps = 'NA', 'NA', 'NA', 'NA', 'NA'
            
            grand_prix_chunk=tr.find('a',{'href':re.compile('/en/results.html/'+ str(yr) + '/races')})
            grand_prix = grand_prix_chunk.text.strip()
            
       
            date_chunk = tr.find('td',{'class':'dark hide-for-mobile'})
            date = date_chunk.text.strip()
        
            winner_chunk = tr.find('span',{'class':'hide-for-mobile'})
            winner = winner_chunk.text.strip()
            
            constructor_chunk = tr.find('td',{'class':'semi-bold uppercase'})
            constructor = constructor_chunk.text
            
            laps_chunk = tr.find('td',{'class':'bold hide-for-mobile'})
            laps = laps_chunk.text.strip()
            
            writer.writerow([grand_prix , date , winner , constructor , laps]) # write to file 
        
        fw.close()
        
        var = str(yr) + '_Race_Results'  
        var = str(var)
        
        new_path = os.path.join(folder_path, var)
        new_path = new_path + '.csv'
        
       # if not os.path.exists(new_path):
           # os.makedirs(new_path)
        
        race_table = pd.read_csv(file_name, names = ['GRAND PRIX','GP_DATE','WINNER','CONSTRUCTOR','LAPS'], sep = ',')
        race_table.to_csv(new_path, index = False, header=True)

run(2000,2019)


