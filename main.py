import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


URL = 'https://www.audible.com/search?keywords=book&node=18573211011'
# URL = 'https://www.audible.com/search?keywords=book&node=18573211011&pageSize=50&page=11'

# chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver =  webdriver.Chrome('C:\Development\chromedriver.exe')

# firefox
# driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Edge
# driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

driver.get(URL)
timeout = 5

# field names
fields = ['Title', 'Subtitle', 'Author', 'Narrator', 'Runtime', 'Release Date', 'Rating', 'Price']
# data rows to be save in csv file
rows = []
# browse pages
while True:
    try:
        # wait until page fully loaded
        element = EC.presence_of_all_elements_located((By.CLASS_NAME, 'pagingElements'))
        WebDriverWait(driver, timeout=timeout).until(element)

        page_elmt = driver.find_element(By.CLASS_NAME, 'pagingElements')

        # books to csv starts
        book_list = driver.find_elements(By.CLASS_NAME, 'productListItem')
        for book in book_list:
            row = []
            title = book.get_attribute('aria-label')
            # print(title)
            try:
                subtitle = book.find_element(By.CLASS_NAME, 'subtitle').text
            except NoSuchElementException:
                subtitle = ''            
            
            author = book.find_element(By.CLASS_NAME, 'authorLabel').text  
            author = author[author.index(': ')+2:]
            try:          
                narrator = book.find_element(By.CLASS_NAME, 'narratorLabel').text   
                narrator = narrator[narrator.index(': ')+2:]
            except NoSuchElementException:
                narrator='N/A'

            runtime = book.find_element(By.CLASS_NAME, 'runtimeLabel').text     
            runtime = runtime[runtime.index(': ')+2:]       
            release_date = book.find_element(By.CLASS_NAME, 'releaseDateLabel').text
            release_date = release_date[release_date.index(': ')+2:]
            rating = book.find_element(By.CLASS_NAME, 'ratingsLabel').text
            rating = rating.split()[0]
            price_element = book.find_element(By.CLASS_NAME, 'buybox-regular-price')
            price = price_element.text[price_element.text.index('$'):]

            # print(subtitle)
            # print(author)
            # print(narrator)
            # print(runtime)
            # print(release_date)
            # print(rating)
            # print(price)

            row.append(title)
            row.append(subtitle)
            row.append(author)
            row.append(narrator)
            row.append(runtime)
            row.append(release_date)
            row.append(rating)
            row.append(price)

            rows.append(row)
        # books to csv ends

    except TimeoutException:
        print('Timed out waiting for page to be loaded')

    page_li_elmt = page_elmt.find_elements(By.CLASS_NAME, 'bc-list-item')  # page navigator
    # print(len(page_li_elmt))
    forward_elmt = page_li_elmt[-1]  # forward arrow
    try:
        clickable = forward_elmt.find_element(By.CLASS_NAME, 'bc-button-disabled')
        print("Last page")
        break
    except NoSuchElementException as e:
        # print(e)
        forward_elmt.click()

filename = 'audiobooks.csv'
with open(filename, 'w', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields) #write header
    csvwriter.writerows(rows) #write data


driver.quit()
