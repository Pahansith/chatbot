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
