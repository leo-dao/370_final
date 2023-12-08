import json
from collections import Counter
import math

def compute_tf(term_freq):

    # Compute term frequency 
    total_words = sum(term_freq.values())
    tf = {term: freq / total_words for term, freq in term_freq.items()}
    return tf

def compute_idf(groups):
    # Compute inverse document frequency (IDF) for terms in the entire document set
    num_groups = len(groups)
    idf = {}
    for document in groups.values():
        for term in document:
            idf[term] = idf.get(term, 0) + 1

    idf = {term: math.log(num_groups / (freq + 1)) for term, freq in idf.items()}
    return idf

def compute_tf_idf(groups):
    tf_idf_result = {}
    
    # Compute IDF for all groups
    idf = compute_idf(groups)

    # Compute TF-IDF for each word
    for category, document in groups.items():
        tf = compute_tf(document)
        tf_idf = {term: tf.get(term, 0) * idf.get(term, 0) for term in document}

        # Sort by TF-IDF value, take top 10
        top_terms = dict(sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)[:10])
        tf_idf_result[category] = top_terms

    return tf_idf_result

def main():
    with open("word_count.json", "r") as json_file:
        grouped_data = json.load(json_file)

    # Compute TF-IDF for each category
    tf_idf_result = compute_tf_idf(grouped_data)

    with open("tf_idf_output.json", "w") as json_file:
        json.dump(tf_idf_result, json_file, indent=2)

if __name__ == "__main__":
    main()

