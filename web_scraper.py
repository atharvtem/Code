import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep

# Configure Selenium WebDriver (headless mode optional)
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no UI)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Path to your downloaded chromedriver
driver_path = "E:\Installations\chromedriver-win64\chromedriver.exe"  # Replace with the path to your Chrome WebDriver

# Setup the driver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the product page (you can replace the URL with your product's review page)
product_url = 'https://www.amazon.in/Motorola-Edge-Fusion-128GB-Storage/dp/B0D4JMFNN8'

reviewList = []

def get_review_url(productUrl,pageNumber):
    page_ref = f"/ref=cm_cr_getr_d_paging_btm_next_{pageNumber}?pageNumber={pageNumber}"
    reviewUrl = productUrl.replace("dp","product-reviews") + page_ref
    print(reviewUrl)
    return reviewUrl

def get_total_pages(url):
    return 1

def clean_scraped_data(reviewList):
    for review in reviewList:
        review['RATING'] = int(float(review['RATING'].split(" ")[0]))
        review['VERIFIED_PURCHASE'] = 1 if review['VERIFIED_PURCHASE'] == 'Verified Purchase' else 0

    return reviewList

def extractReviews(productUrl):
    # url = productUrl.replace("dp","product-reviews")
    # total_pages = get_total_pages(url)

    # for i in range(1,total_pages+1):
    #     reviewUrl = get_review_url(productUrl,i)

    #     driver.get(reviewUrl)
    #     sleep(2)
    #     soup = BeautifulSoup(driver.page_source, 'html.parser')

    #     reviews = soup.findAll('div',{'data-hook':'review'})
    #     # print(reviews)

    #     for item in reviews:
    #         review = {
    #             'RATING':item.find('i',{'data-hook':'review-star-rating'}).text.strip(),
    #             'REVIEW_TEXT':item.find('span',{'data-hook':'review-body'}).text.strip(),
    #             'VERIFIED_PURCHASE':item.find('span',{'data-hook':'avp-badge'}).text.strip(),
    #         }
        
    #         reviewList.append(review)

    # df = pd.DataFrame(clean_scraped_data(reviewList))
    # df.to_csv("data2.csv",index=False)
    df = pd.read_csv('data.csv')
    return df

extractReviews(product_url)