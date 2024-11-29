from keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pandas as pd

def classify_sentiment(df):
    model = load_model('models/1.h5')
    df = df.reset_index(drop=True)
    preprocessed_data = preprocess_data(df)
    y_pred = model.predict(preprocessed_data)

    df['SENTIMENT'] = 1
    print(y_pred)
    for index,row in df.iterrows():
        df.at[index,'SENTIMENT'] = np.argmax(y_pred[index])

    return df

def preprocess_data(df):
    data = df.dropna(subset=['REVIEW_TEXT'])
    tokenizer = Tokenizer(num_words=5000)
    tokenizer.fit_on_texts(data ['REVIEW_TEXT'])
    sequences = tokenizer.texts_to_sequences(data ['REVIEW_TEXT'])

    # Define maxlen for sequences
    maxlen = 100
    X = pad_sequences(sequences,maxlen=maxlen)
    return X
