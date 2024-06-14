# %%
from langchain.llms import Ollama
import csv

# %%
ollama = Ollama(base_url="http://localhost:11434", model="phi3:mini")

# %%
def auto_label_advice(text):
    prompt = "Classify the following sentence as containing financial investment advice (1) or financial context(0) or not not reletade to finance (-1): " + "' " + text + " '" + " limit the answer to either 1,0 or -1 , nothing else."
    label = ollama(prompt)
    return label

# %%
def classify_data():
    # File path to your input CSV file
    input_file_path = r'merged_dataset.csv'
    # File path to your output CSV file
    output_file_path = r'new_dataset.csv'

    # List to store dictionaries of questions and answers
    data_list = []

    # Open the input file in read mode
    with open(input_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
    
        # Skip header if it exists
        next(reader)  # Skip the header row
        i = 0
        # Iterate over each row in the CSV file
        for row in reader:
            i = i +1
            print(i)
            question = row[0]
            answer = row[1]

            label = auto_label_advice(answer)
        
            # Create a dictionary for each question and answer pair
            data_dict = {
                'advice': answer,
                'label': label
            }
        
            # Append the dictionary to the list
            data_list.append(data_dict)

            if i == 1000:
                break

    # Write the list of dictionaries to the output CSV file
    with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['advice', 'label']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        writer.writeheader()  # Write the header row
        for data in data_list:
            writer.writerow(data)

    print("Processed data has been written to", output_file_path)

# %%
classify_data()


