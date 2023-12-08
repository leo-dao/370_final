import pandas as pd
import json
import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

with open(r".\stopwords.txt", "r") as stopwords_file: # replace with path to stopwords
    stopwords_file = set(stopwords_file.read().splitlines())

stopwords_nltk = set(stopwords.words("english"))

# Combine stopwords
stopwords_set = stopwords_file | stopwords_nltk 

print("stopwords:", stopwords)

df = pd.read_csv("annotatedarticles.csv")    #replace with path to csv

group_mapping = {
    1: "Movie Reviews and Critiques",
    2: "Box Office",
    3: "Movie Recommendations and Comparisons",
    4: "Streaming and Release Information",
    5: "Behind-the-Scenes and Production Insights",
    6: "Cultural Impact",
    7: "Adaptation from Game",
    8: "Streaming records and Comparison",
    9: "Unrelated"
}

# Initialize dictionaries for topics
grouped_data = {}

def clean_word(word):
    cleaned_word = re.sub(r"[^a-zA-Z0-9]", '', word)
    return cleaned_word.lower()


def is_above_threshold(count, threshold=5):
    return count >= threshold

df["Description"].fillna("", inplace=True)  

# Group by the "Annotation" column
grouped = df.groupby("Annotation")

# Create dictionaries for "Title" and "Content"
for group, data in grouped:

    group_name = group_mapping.get(group, f"Group{group}")

    word_dict = {}
        
    # Iterate over rows in the group
    for index, row in data.iterrows():
        # Add words from "Title" to the word_dict
        for word in row["Title"].split():
            title_word = clean_word(word)
            if title_word not in stopwords_set:
                word_dict[title_word] = word_dict.get(title_word, 0) + 1
        
        # Add words from "Description" to the word_dict
        for word in row["Description"].split():
            description_word = clean_word(word)
            if description_word not in stopwords_set:
                word_dict[description_word] = word_dict.get(description_word, 0) + 1
    
    # Words with frequency >= 5
    words_dict = {word: count for word, count in word_dict.items() if "'" not in word and is_above_threshold(count)}

    # WGoups in descending order
    sorted_words_dict = dict(sorted(words_dict.items(), key=lambda x: x[1], reverse = True))
    

    grouped_data[group_name] = sorted_words_dict


with open("word_count.json", "w") as json_file:
    json.dump(grouped_data, json_file, indent=2)

print("Output written to output.json")