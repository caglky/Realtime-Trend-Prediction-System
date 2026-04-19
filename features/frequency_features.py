from collections import Counter

def get_word_frequencies(all_titles, clean_text):
    cleaned_words = []
    for title in all_titles:
        cleaned_words.extend(clean_text(title))
    return Counter(cleaned_words)