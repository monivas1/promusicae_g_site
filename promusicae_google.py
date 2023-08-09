# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 13:23:56 2021

@author: User
"""


# txt = "ATU10592107"



from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
import time

from bs4 import BeautifulSoup
import requests

import os.path


# from random import randint

import streamlit as st
import pandas as pd
from io import BytesIO

from pathlib import Path
from suds.client import Client
from datetime import datetime

#st.set_page_config(page_title="PROMUSICAE",page_icon="promusicae.ico",layout="wide")


st.write(
    """
# PROMUSICAE Búsqueda de canciones en google
Subir fichero "XLSX" con los las canciones a buscar en página "Hoja1 y según formato indicado".
"""
)



def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_beau_with_sel(URL):
    try:
        options = Options()
        options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        options.add_argument("--headless") 
        options.add_argument('--no-sandbox') # Bypass OS security model

        # driver = webdriver.Chrome(chrome_options=options, executable_path="C:/Utility/BrowserDrivers/chromedriver.exe", )

        # driver = webdriver.Chrome(ChromeDriverManager().install())

        #driver = webdriver.Chrome(chrome_options=options,executable_path="C:/Scraping/chromedriver.exe")
        driver = webdriver.Chrome(chrome_options=options,executable_path="chromedriver.exe")

        driver.get(URL)
        # driver.maximize_window()
        
        # source = driver.find_element_by_xpath('//div[@class="_1KRklrtnaQVWD-N2ldQ9d3"]')
        source = driver.page_source

        
        soup = BeautifulSoup(source, "lxml")

        driver.quit()
        
    except AttributeError:
        webpage = requests.get(URL, headers=HEADERS)
     
        soup = BeautifulSoup(webpage.content, "lxml")
 
    return soup

def get_beau_with_sel_FF(URL):
    try:
        
        TIMEOUT = 20
        XPATH = "//*[@class='ui-mainview-block eventpath-wrapper']"

        # options = Options()
        # options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        # options.add_argument("--headless") 
        # options.add_argument('--no-sandbox') # Bypass OS security model

        # driver = webdriver.Chrome(chrome_options=options,executable_path="C:/Scraping/chromedriver.exe")

        firefoxOptions = Options()
        firefoxOptions.add_argument("--headless")
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(
            options=firefoxOptions,
            service=service,
        )

        driver.get(URL)
        try:
            WebDriverWait(driver, TIMEOUT).until(
                EC.visibility_of_element_located((By.XPATH, XPATH,))
            )
        
        except TimeoutException:
            # st.warning("Timed out waiting for page to load")
            driver.quit()
        
        time.sleep(10)
        elements = driver.find_elements_by_xpath(XPATH)
        # st.write([el.text for el in elements])
        driver.quit()

        source = driver.page_source

        
        soup = BeautifulSoup(source, "lxml")

    except AttributeError:
        webpage = requests.get(URL, headers=HEADERS)
     
        soup = BeautifulSoup(webpage.content, "lxml")
 
    return soup

if (os.path.isfile('resultados_google.csv')):
    os.remove('resultados_google.csv')
    

with open ('resultados_google.csv', 'a', encoding="utf-8") as file:
   file.write("num_id;")
   file.write("Artist;")
   file.write("Track;")
   file.write("URL")
   file.write("\n")
    
   file.close()

HEADERS = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
      }
    # The webpage URL
    # URL = "https://www.amazon.com/s?k=playstation+4&ref=nb_sb_noss_2"

links_list = []

contador_web=0
contador_prod=0
uploaded_file = st.file_uploader("Upload Excel", type=".xlsx")

if uploaded_file:

    
    df = pd.read_excel(uploaded_file, sheet_name='Hoja1')
    #df = pd.read_excel("busquedas_google.xlsx", sheet_name='Hoja1')
    file_name = Path(uploaded_file.name).stem
    
    now = datetime.now()
    new_file_name_csv=file_name + "_" + str(now.year) + str(now.month) + str(now.day) + "_" + str(now.hour) +str(now.minute) + ".csv"
    new_file_name_xlsx=file_name + "_" + str(now.year) + str(now.month) + str(now.day) + "_" + str(int(now.hour)*100 +int(now.minute)) + ".xlsx"

    for i in range(0,len(df)):
            artist=df['artist'][i]
            track=df['track'][i]
            num_webs=df['num_web'][i]
            
            # st.write(f'Artist: "{artist}" Track: "{track}"')
            print(f'Artist: "{artist}" Track: "{track}"')
            # myvies=myvies[2:-3]
            # st.write(myvies)
            # myvies=myvies.strip(' \n')
            # st.write(myvies)
            try:
                
                texto_busqueda=artist.replace(" ","+") + "+" + track.replace(" ","+") +"+descarga"
            except Exception :
                texto_busqueda=""
            url_busqueda=""
            for num_web in range(num_webs):
                num_start=num_web*10
                url_busqueda="https://www.google.com/search?q=" + texto_busqueda + "&rlz=1C1RXQR_esES953ES953&sxsrf=AB5stBhQqY8seU3ChhccIYxk8sMEqNsoGA:1691481666902&ei=QvbRZJPiMcOjkwX_yrHABA&start=" + str(num_start)
                 

                contador_web=contador_web+1
                # main(links)    
                URL2 = url_busqueda
             
                # HTTP Request
                # webpage = requests.get(URL2, headers=HEADERS)
             
                # # Soup Object containing all data
                # soup = BeautifulSoup(webpage.content, "lxml")
                #soup=get_beau_with_sel(URL2)
                soup=get_beau_with_sel_FF(URL2)
             
                # Fetch links as List of Tag Objects
                # links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
                links = soup.find_all("a", attrs={'jscontroller': 'M9mgyc'})
             
             
                # Loop for extracting links from Tag Objects
                links_list=[]
                for link in links:
                    if not "/search?" in link.get('href') :
                        if "https://translate.google.com/translate?hl=es&sl=en&u="  in link.get('href') :
                            links_list.append(link.get('href').replace("https://translate.google.com/translate?hl=es&sl=en&u=",""))
                        else:
                            links_list.append(link.get('href'))
                    # links_list.append(link.get('data-ved'))
            
                    
                # Loop for extracting product details from each link 
                    
                for link in links_list:
                    contador_prod=contador_prod+1
                    print(f"Web analizada: {contador_web} enlace: {contador_prod}")
                    with open ('resultados_google.csv', 'a', encoding="utf-8") as file:
                       file.write(f'"{contador_prod}";')
                       file.write(f'"{artist}";')
                       file.write(f'"{track}";')
                       file.write(f'"{link}";')
                       file.write("\n")
        
                file.close()
    
    
    file_w = open("resultados_google.csv",encoding='latin1')

    st.download_button(label='?? Bajar los resultados actuales en CSV',data=file_w, file_name=new_file_name_csv )                    
    file_w.close()          
    
    try:
        df_escrito=pd.read_csv('resultados_google.csv',sep=';',encoding='latin1')
        file_x=to_excel(df_escrito)
        st.download_button(label='?? Bajar los resultados actuales en EXCEL',data=file_x, file_name=new_file_name_xlsx)   
    except Exception :
        st.write("Debido a un problema de tipos no es posible generar el fichero en MS Excel.")

