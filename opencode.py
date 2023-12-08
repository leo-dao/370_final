import json
from gensim import corpora, models
from gensim.models.phrases import Phrases, Phraser
from gensim.utils import simple_preprocess
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk

nltk.download('wordnet')
nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')
custom_stop_words = ['five', 'nights', 'freddy', 'movie', 'film']  # Extend with more words as needed
stop_words.extend(custom_stop_words)

def preprocess(text):
    result = []
    for token in simple_preprocess(text):
        if token not in stop_words and len(token) > 2:
            result.append(lemmatizer.lemmatize(token))
    return result

with open('/Users/keremersoz/370 project/movie_articles.json', 'r') as file:
    data = json.load(file)

documents = []
for article in data['Five Nights at Freddy’s']['articles']:
    text = article.get('title', '') + ' ' + article.get('description', '')
    documents.append(preprocess(text))

bigram = Phrases(documents, min_count=5)
bigram_mod = Phraser(bigram)

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

processed_docs = make_bigrams(documents)

dictionary = corpora.Dictionary(processed_docs)
corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

ldamodel = models.ldamodel.LdaModel(corpus, num_topics=8, id2word=dictionary, passes=15)

#topics = ldamodel.print_topics(num_words=10)
#for num, topic in enumerate(topics):
#    print(f"Topic {num + 1}: {topic}")

# Print the topics in a more organized format
for num, topic in ldamodel.show_topics(num_topics=8, num_words=10, formatted=False):
    topic_words = ", ".join([word for word, _ in topic])
    weights = ", ".join([f"{weight:.2f}" for _, weight in topic])
    print(f"Topic {num + 1}:")
    print(f"   Words: {topic_words}")
    print(f"   Weights: {weights}")
    print("\n")
