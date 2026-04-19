from sklearn.feature_extraction.text import TfidfVectorizer

def compute_tfidf(all_titles):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(all_titles)
    words = vectorizer.get_feature_names_out()
    return X, words