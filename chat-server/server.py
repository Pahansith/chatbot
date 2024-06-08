from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import os
from tf_keras.models import load_model
from tf_keras.preprocessing.sequence import pad_sequences
import numpy as np
import random
import string

# Define the path to your saved components
folder_name = 'conf'

# Load the saved model
model = load_model(os.path.join(folder_name, 'chatbot_model.h5'))

# Load the tokenizer
with open(os.path.join(folder_name, 'tokenizer.pickle'), 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load the responses dictionary
with open(os.path.join(folder_name, 'responses.pickle'), 'rb') as handle:
    responses = pickle.load(handle)

# Load the input_shape
with open(os.path.join(folder_name, 'input_shape.pickle'), 'rb') as handle:
    input_shape = pickle.load(handle)

# Load the LabelEncoder
with open(os.path.join(folder_name, 'label_encoder.pickle'), 'rb') as handle:
    le = pickle.load(handle)

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def predict():
    texts_p = []
    data = request.get_json(force=True)
    prediction_input = data['message']
    
    # Preprocess the message
    prediction_input = [letters.lower() for letters in prediction_input if letters not in string.punctuation]
    prediction_input = ''.join(prediction_input)
    texts_p.append(prediction_input)

    prediction_input = tokenizer.texts_to_sequences(texts_p)
    prediction_input = np.array(prediction_input).reshape(-1)
    prediction_input = pad_sequences([prediction_input], input_shape)

    output = model.predict(prediction_input)
    confidence = np.max(output)
    print("Prediction Confidence : ", confidence)
    if confidence < 0.7:
        return jsonify({'response': "I'm sorry, I do not understand your question."})
    else:
        pred_class = np.argmax(output)
        response_tag = le.inverse_transform([pred_class])[0]
        print("Predicted Tag : ", response_tag)
        return jsonify({'response': random.choice(responses[response_tag])})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
