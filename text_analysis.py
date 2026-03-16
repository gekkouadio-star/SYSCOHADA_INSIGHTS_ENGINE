import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

nltk.download("stopwords")
stop_words = set(stopwords.words('french'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', '', text)
    words = text.split()
    words = [w for w in words if w not in stop_words and len(w) > 2]
    return " ".join(words)

def tokenize_corpus(text_series):
    cleaned = text_series.apply(clean_text)
    return cleaned

def word_frequencies(text_series):
    all_words = " ".join(text_series)
    words = all_words.split()
    freq = pd.Series(words).value_counts()
    return freq

def ngrams(text_series, n=2):
    vectorizer = CountVectorizer(ngram_range=(n,n))
    X = vectorizer.fit_transform(text_series)
    sum_words = X.sum(axis=0)
    words_freq = [(word, int(sum_words[0, idx])) for word, idx in vectorizer.vocabulary_.items()]
    return sorted(words_freq, key=lambda x: x[1], reverse=True)