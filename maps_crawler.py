import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

excludeSwitches: ['enable-logging']
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options, executable_path=r'C:\ProgramData\Anaconda3\envs\hltv\chromedriver.exe')

query_user = input('Digite sua busca / Type your google query: ')
query = query_user.replace(" ", "+")

driver_get = driver.get(f'https://www.google.com/maps/search/{query}')

def get_info(driver_get):
    """Gets all info from page"""

    response = driver.page_source
    soup = BeautifulSoup(response,'html.parser')
    results = soup.find_all('div',{"class":"section-result-content"})

    names = []
    addresses = []
    rating_scores = []
    num_ratings = []
    phone_numbers = []

    for result in results:
        try:
            names.append(str(result.find('h3').getText()))
        except:
            names.append('not found')
        
        try:
            addresses.append(str(result.find('span', {"class": "section-result-location"}).getText()))
        except:
            addresses.append('not found')

        try:
            rating_scores.append(str(result.find('span', {"class": "cards-rating-score"}).getText()))
        except:
            rating_scores.append('not found')
        
        try:
            num_ratings.append(str(result.find('span', {"class": "section-result-num-ratings"}).getText()))
        except:
            num_ratings.append('not found')

        try:
            phone_numbers.append(str(result.find('span', {"class": "section-result-info section-result-phone-number"}).getText()))
        except:
            phone_numbers.append('not found')

    df = pd.DataFrame({'name': names,
                    'address': addresses,
                    'rating_score': rating_scores,
                    'number_of_ratings': num_ratings,
                    'phone': phone_numbers,
                    'query': query_user})

    df['number_of_ratings'].replace('(', '').replace(')', '')
    
    return df

while True:
    
    wait = WebDriverWait(driver, 30)
    next_button = wait.until(EC.presence_of_element_located((By.ID, 'n7lv7yjyC35__section-pagination-button-next')))

    if next_button.is_enabled() == False:
        break
    else:

        df = get_info(driver_get)
        print(df)

        if 'spa_sp.csv' in os.listdir():
            df.to_csv(f'{query_user}.csv', mode='a', header=False, index=False, sep=";")
        else:
            df.to_csv(f'{query_user}.csv', mode='a', header=True, index=False, sep=";")
        time.sleep(2.9)

        webdriver.ActionChains(driver).move_to_element(next_button).click(next_button).perform()
    

driver.quit()