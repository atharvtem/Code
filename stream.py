import streamlit as st 
from web_scraper import extractReviews
from fake_classification import classify_fake
from sentiment_analysis import classify_sentiment
import pandas as pd
import plotly.express as px

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

    return classified_data
    
 
def star_maker(rating):
    filled_stars = '★' * int(rating)  # filled stars
    half_star = '✬' if rating % 1 >= 0.5 else ''  # half star if rating has a decimal part of .5
    empty_stars = '☆' * (5 - int(rating) - (1 if half_star else 0))  # empty stars
    star_display = filled_stars + half_star + empty_stars
    return star_display

def summarize_sentiment(actual_rating,modified_rating,positive,negative,neutral,fake):
    prompt = f"A product has average rating of {actual_rating} but when we identified fake reviews the rating is adjusted to {modified_rating} and the distribution of review sentiments is positive:{positive}%, negative:{negative}% and neutral:{neutral}%. Also the proportion of fake reviews is {fake}%. So give me the overall summary of the product review in 4-5 lines. Also according to proportion of fake reviews include the key aspect of reliability of the product in the summary. Dont include numbers in the summary. Explain it in simple words."

    import google.generativeai as genai

    genai.configure(api_key="AIzaSyAnGYRZkvlXmiHpdL96VYBKPQEm124ceh4")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    


    # summary = "We have enough reviews to get a clear sense of the product's sentiment. Most reviews are genuine, with many marked as verified purchases, showing reliability. Overall, the sentiment is mostly positive, with only a few negative comments. After removing fake reviews, the adjusted rating is still close to the original, so the product is reliable and well-rated."
    return response.text

col1, col2 = st.columns([2, 1])  

with col1:
    user_input=st.text_input('Enter URL',key="input")

with col2:
    st.markdown("<div style='padding-top: 25px;'></div>", unsafe_allow_html=True)
    get_button=st.button("Get")

if get_button:
    if user_input:
        # extracting data from url
        scrape=scrape_data(user_input)
        actual_rating = scrape['RATING'].mean()
        st.write("### Product Sentiment Data")
        st.dataframe(scrape)
        
        # filtering fake data
        real_data=fake_review_det(scrape)
        

        modified_rating = real_data['RATING'].mean()

        fake_percent = (len(scrape)-len(real_data))*100/len(scrape)
        review_count = pd.DataFrame({"Review_Type":["Fake","Genuine"],"Percentage":[fake_percent,100-fake_percent]})

        # sentiment classification
        sentiment_anal=sentiment(real_data)
        print(sentiment_anal)

        positive_percent = sentiment_anal['SENTIMENT'].value_counts().get(2,0)*100/len(real_data)
        neutral_percent = sentiment_anal['SENTIMENT'].value_counts().get(1,0)*100/len(real_data)
        negative_percent = sentiment_anal['SENTIMENT'].value_counts().get(0,0)*100/len(real_data)

        sentiment_counts = sentiment_anal['SENTIMENT'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Percentage']

        # Plotting the graphs
        fig2=px.bar(review_count , x="Review_Type" , y="Percentage" , title="Fake vs Genuine",  
                    text='Percentage')
        st.plotly_chart(fig2)

        fig = px.pie(sentiment_counts, names="Sentiment", values="Percentage", title="Sentiment Distribution")
        st.plotly_chart(fig)

        # Display the star rating in Streamlit
        st.markdown(f"**Actual Rating:** {star_maker(actual_rating)} ({actual_rating}/{5})")
        st.markdown(f"**Modified Rating:** {star_maker(modified_rating)} ({modified_rating}/{5})")

        # Displaying summary
        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
                <p>Summary of the Review Sentiment</p>
                <hr>
                <p>{summarize_sentiment(actual_rating,modified_rating,positive_percent,negative_percent,neutral_percent,fake_percent)}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.write("Please enter URL")

