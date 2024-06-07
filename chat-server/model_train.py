import json
import pandas as pd

import string
import os
import pickle

from tf_keras.preprocessing.text import Tokenizer
from tf_keras.preprocessing.sequence import pad_sequences
from tf_keras.models import Model
from tf_keras.layers import Input, LSTM, Dense, Embedding
from tf_keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

# Define the global variables
tokenizer = Tokenizer(num_words=2000)
folder_name = 'conf'
le = LabelEncoder()

#Loading the data from json file and map them into objects
def load_data():
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
    dataset = pd.DataFrame({'inputs': inputs, "tags" : tags})
    return dataset, responses

# Remove special characters / symbols from the data loaded from the json
def process_data(dataset):
    dataset['inputs'] = dataset['inputs'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
    dataset['inputs'] = dataset['inputs'].apply(lambda wrd: ''.join(wrd))
    return dataset

# Tokenize the data and generate train data set
def tokenize_data(dataset):
    tokenizer.fit_on_texts(dataset['inputs'])
    train = tokenizer.texts_to_sequences(dataset['inputs'])
    x_train = pad_sequences(train)
    y_train = le.fit_transform(dataset['tags'])
    input_shape = x_train.shape[1]
    print("Input shape : ", input_shape)
    vocabulary = len(tokenizer.word_index)
    print("number of unique words : ", vocabulary)
    output_length = le.classes_.shape[0]
    print("Output length :", output_length)
    return x_train, y_train, input_shape, output_length, vocabulary

# Configure the LSTM model
def configure_model(input_shape, vocabulary, output_length):
    i = Input(shape=(input_shape,))
    x = Embedding(vocabulary+1,10)(i)
    x = LSTM(10, return_sequences=False)(x)
    x = Dense(output_length, activation="softmax")(x)
    model = Model(i, x)
    model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
    return model

# Train the model with train data set
def train_model(model, x_train, y_train):
    model.fit(x_train, y_train, epochs=1500)
    return model

# Save the trained model and configurations to filesystem. 
def save_configurations(folder_name, model, responses, input_shape, le):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    model.save(os.path.join(folder_name, 'chatbot_model.h5'))  # Save the model to an HDF5 file

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

def main():
    data_set, responses = load_data()
    data_set = process_data(data_set)
    x_train, y_train, input_shape, output_length, vocabulary = tokenize_data(data_set)
    model = configure_model(input_shape, vocabulary, output_length)
    print(model.summary)
    model = train_model(model, x_train, y_train)
    save_configurations(folder_name, model, responses, input_shape, le)

if __name__ == "__main__":
    main()