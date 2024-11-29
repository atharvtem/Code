# Generating a dummy dataset with at least 30 reviews for the sentiment analysis project
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# Seed for reproducibility
np.random.seed(0)

# Generating 30+ dummy product reviews with sentiment
product_ids = np.random.randint(100, 200, size=30)
reviews = [
    "Excellent product!", "Not as expected", "Value for money", 
    "Highly recommended", "Disappointing quality", "Just okay", 
    "Could be better", "Very satisfied", "Not worth the price", "Amazing features",
    "Exceeded expectations", "Terrible experience", "Product broke easily", "Would buy again",
    "Simply wonderful", "Packaging was poor", "Worth every penny", "Does not meet the description",
    "Extremely durable", "Feels cheap", "Perfect for my needs", "Service was great", "Unexpected delay",
    "Does what it says", "Loved it", "Not satisfied", "It's okay", "Top quality",
    "Value purchase", "High performance"
]
sentiments = np.random.choice(["Positive", "Negative", "Neutral"], size=30)
revie=np.random.choice(["Fake" , "Genuine"], size=30)

# Creating the DataFrame
dummy_data_30 = pd.DataFrame({
    "product_id": product_ids,
    "review": np.random.choice(reviews, size=30),
    "sentiment": sentiments,
    "review_type": revie

})



st.write("### Product Sentiment Data")
st.dataframe(dummy_data_30)


# sentiment_counts = dummy_data_30['sentiment'].value_counts().reset_index()
# sentiment_counts.columns = ['Sentiment', 'Count']

sentiment_counts = pd.DataFrame({"Sentiment":["Positive","Negative","Neutral"],"Percentage":[70.30,8.20,21.50]})
review_count = pd.DataFrame({"Review_Type":["Fake","Genuine"],"Percentage":[8.90,91.10]})

print(sentiment_counts)

# review_count=dummy_data_30['review_type'].value_counts(normalize=True).reset_index()
# review_count.columns=['Review_type' , 'Percentage']
# review_count['Percentage'] = review_count['Percentage'] * 100
fig = px.pie(sentiment_counts, names="Sentiment", values="Percentage", title="Sentiment Distribution")
st.plotly_chart(fig)

fig2=px.bar(review_count , x="Review_Type" , y="Percentage" , title="Fake vs Genuine",  
             text='Percentage')
st.plotly_chart(fig2)



previous_rating = 3.8
actual_rating=3.6
max_stars = 5
prod_title = "Motorola Edge 50 Pro 5G with 125W Charger (Luxe Lavender, 256 GB) (12 GB RAM)"

def star_maker(rating):
    filled_stars = '★' * int(rating)  # filled stars
    half_star = '✬' if rating % 1 >= 0.5 else ''  # half star if rating has a decimal part of .5
    empty_stars = '☆' * (max_stars - int(rating) - (1 if half_star else 0))  # empty stars
    star_display = filled_stars + half_star + empty_stars
    return star_display

def summarize_sentiment():
    summary = "We have enough reviews to get a clear sense of the product's sentiment. Most reviews are genuine, with many marked as verified purchases, showing reliability. Overall, the sentiment is mostly positive, with only a few negative comments. After removing fake reviews, the adjusted rating is still close to the original, so the product is reliable and well-rated."
    return summary

# Display the star rating in Streamlit
st.markdown(f"**Previous Rating:** {star_maker(previous_rating)} ({previous_rating}/{max_stars})")

st.markdown(f"**Actual Rating:** {star_maker(actual_rating)} ({actual_rating}/{max_stars})")

st.markdown(
    f"""
    <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px;">
        <p>Summary of the Review Sentiment for {prod_title}</p>
        <hr>
        <p>{summarize_sentiment()}</p>
    </div>
    """,
    unsafe_allow_html=True
)
