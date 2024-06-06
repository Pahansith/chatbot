import json

# Load the data from the files
with open('inputs.json', 'r') as file:
    questions = json.load(file)

with open('data.json', 'r') as file:
    answers = json.load(file)

# Combine the data
combined_data = []
for question in questions:
    question_text = question['input']
    label = question['label']
    possible_answers = answers.get(label, [])
    combined_data.append({
        'question': question_text,
        'answers': possible_answers
    })

# Save the combined data to a new JSON file
with open('combined_questions_answers.json', 'w') as file:
    json.dump(combined_data, file, indent=4)

print("Combined file created successfully!")
