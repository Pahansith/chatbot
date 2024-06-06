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
folder_name = 'conf'

import os
# Create the folder if it doesn't exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

model.save(os.path.join(folder_name, 'chatbot_model.h5'))  # Save the model to an HDF5 file

import pickle

# Save the tokenizer to a file
with open(os.path.join(folder_name,'tokenizer.pickle'), 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Save the responses dictionary
with open(os.path.join(folder_name,'responses.pickle'), 'wb') as handle:
    pickle.dump(responses, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Save the input_shape
with open(os.path.join(folder_name,'input_shape.pickle'), 'wb') as handle:
    pickle.dump(input_shape, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Save the LabelEncoder
with open(os.path.join(folder_name,'label_encoder.pickle'), 'wb') as handle:
    pickle.dump(le, handle, protocol=pickle.HIGHEST_PROTOCOL)


