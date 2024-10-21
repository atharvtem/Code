from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
import xgboost as xgb
import numpy as np
import pickle
import pandas as pd


def classify_fake(df):
    model = pickle.load(open('models/fake.pkl','rb'))
    preprocessed_data = preprocess_data(df)
    y_pred_prob = model.predict(preprocessed_data)  # Predicted probabilities
    y_pred = np.where(y_pred_prob > 0.9, 1, 0)  # Convert probabilities to binary labels

    df['LABEL'] = 0
    for index,row in df.iterrows():
        df.at[index,'LABEL'] = y_pred[index]

    return df

def preprocess_data(df):
    data = df.dropna(subset=['REVIEW_TEXT'])
    le = LabelEncoder()
    data['verified_purchase_encoded'] = le.fit_transform(data['VERIFIED_PURCHASE'])
    tfidf = TfidfVectorizer(max_features=5000)
    tfidf_matrix = tfidf.fit_transform(data['REVIEW_TEXT'])
    X = hstack([tfidf_matrix, data[['RATING', 'verified_purchase_encoded']].values])
    dtest = xgb.DMatrix(X)
    return dtest
     