import streamlit as st 
# from streamlit_option_menu import option_menu
from web_scraper import extractReviews
from fake_classification import classify_fake
from sentiment_analysis import classify_sentiment
import pandas as pd

def scrape_data(url):
    scraped_data = extractReviews(url)
    return scraped_data


def fake_review_det(scrape_data):
    # we'll now check each review and eliminate the fake reviews within. 
    # fake reviews will be drop
    classified_data = classify_fake(scrape_data)
    geniuine_rev = classified_data[classified_data.LABEL != 1]
    return geniuine_rev

def sentiment(reviews):
    #accord to fake review fun sentiment function will categorise into 3 like pos ,neg , neu and return count of each
    classified_data = classify_sentiment(reviews)

    positive_count = classified_data['SENTIMENT'].value_counts().get(2,0)
    neutral_count = classified_data['SENTIMENT'].value_counts().get(1,0)
    negative_count = classified_data['SENTIMENT'].value_counts().get(0,0)

    if positive_count> negative_count+neutral_count:
        sentiment_text="Gheun Taak ( ͡° ͜ʖ ͡°) "
    elif negative_count>positive_count+neutral_count:
        sentiment_text="Lund product ╭∩╮"
    else:
        sentiment_text="(ーー)"

    return sentiment_text
    
 
    


col1, col2 = st.columns([2, 1])  

with col1:
    user_input=st.text_input('Enter URL',key="input")

with col2:
    st.markdown("<div style='padding-top: 25px;'></div>", unsafe_allow_html=True)
    get_button=st.button("Get")

if get_button:
    if user_input:
        scrape=scrape_data(user_input)
        real_data=fake_review_det(scrape)
        sentiment_anal=sentiment(real_data)
        st.write(sentiment_anal)
    else:
        st.write("Please enter URL")

