import re 

stopwords = ["ve", "bir","bu","için","ile","de","da","mi","mu", "mı", "neden", "nasıl", "kadar", "ne", "en", "neler", "daha", "cok","ama","gibi", "çok"]

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-ZğüşöçıİĞÜŞÖÇ\s]", "", text) 

    words = text.split()
    words = [w for w in words if w not in stopwords]
    
    return words 