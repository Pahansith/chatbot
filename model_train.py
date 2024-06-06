import json
import numpy as np
import pandas as pd
import nltk

from tf_keras.preprocessing.text import Tokenizer
from tf_keras.preprocessing.sequence import pad_sequences
from tf_keras.models import Model
from tf_keras.layers import Input, LSTM, Dense, Embedding, GlobalMaxPool1D, Flatten
from tf_keras.utils import to_categorical
# import matplotlib.pyplot as plt


with open("train_data_set.json") as content:
    data = json.load(content)

tags = []
inputs = []
responses = {}

for intent in data["intents"]:
    responses[intent['label']] = intent['answers']
    for lines in intent['questions']:
        inputs.append(lines)
        tags.append(intent['label'])
# print(tags)
# print(inputs)
# print(responses)

dataset = pd.DataFrame({'inputs': inputs, "tags" : tags})
# dataset

import string
dataset['inputs'] = dataset['inputs'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
dataset['inputs'] = dataset['inputs'].apply(lambda wrd: ''.join(wrd))

tokenizer = Tokenizer(num_words=2000)
tokenizer.fit_on_texts(dataset['inputs'])
train = tokenizer.texts_to_sequences(dataset['inputs'])

x_train = pad_sequences(train)

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
y_train = le.fit_transform(dataset['tags'])

input_shape = x_train.shape[1]
print("Input shape : ", input_shape)

vocabulary = len(tokenizer.word_index)
print("number of unique words : ", vocabulary)
output_length = le.classes_.shape[0]
print("Output length :", output_length)


i = Input(shape=(input_shape,))
x = Embedding(vocabulary+1,10)(i)
x = LSTM(10, return_sequences=False)(x)
x = Dense(output_length, activation="softmax")(x)
model = Model(i, x)

model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=1000)

import random
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

