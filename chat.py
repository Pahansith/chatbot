import random
import json
import numpy as np
import pandas as pd
import nltk
import string

from tf_keras.preprocessing.text import Tokenizer
from tf_keras.preprocessing.sequence import pad_sequences
from tf_keras.models import Model
from tf_keras.layers import Input, LSTM, Dense, Embedding, GlobalMaxPool1D, Flatten
from tf_keras.utils import to_categorical
from tf_keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import os

folder_name = "conf"

model = load_model(os.path.join(folder_name,'chatbot_model.h5'))
import pickle

# Load the tokenizer
with open(os.path.join(folder_name,'tokenizer.pickle'), 'rb') as handle:
    tokenizer = pickle.load(handle)


# Load the responses dictionary
with open(os.path.join(folder_name,'responses.pickle'), 'rb') as handle:
    responses = pickle.load(handle)

# Load the input_shape
with open(os.path.join(folder_name,'input_shape.pickle'), 'rb') as handle:
    input_shape = pickle.load(handle)

# Load the LabelEncoder
with open(os.path.join(folder_name,'label_encoder.pickle'), 'rb') as handle:
    le = pickle.load(handle)


confidence_threshold = 0.5 
while True:
    texts_p = []
    prediction_input = input('You : ')
    prediction_input = [letters.lower() for letters in prediction_input if letters not in string.punctuation]
    prediction_input = ''.join(prediction_input)
    texts_p.append(prediction_input)

    prediction_input = tokenizer.texts_to_sequences(texts_p)
    prediction_input = np.array(prediction_input).reshape(-1)
    prediction_input = pad_sequences([prediction_input], input_shape)

    output = model.predict(prediction_input)
    confidence = np.max(output)

    if confidence < confidence_threshold:
        print("Bot : I'm sorry, I don't understand your question.")
    else:
        output = output.argmax()
        response_tag = le.inverse_transform([output])[0]
        print(response_tag)
        print("Bot : ", random.choice(responses[response_tag]))
    if response_tag == 'thanks':
        break