import re 

stopwords = ["ve", "bir","bu","için","ile","de","da","mi","mu", "mı", "mü", 
             "neden", "nasıl","hangi" "kadar","göre", "ilgili","ne", "en", "neler", 
             "daha", "sonra", "önce", "çok","ama","gibi", "çok", "olan", "oldu","oluyor", 
             "son", "kimse", "var","yok", "yaptı","etti","bitti","başladı","söyledi","geldi","gitti"]

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-ZğüşöçıİĞÜŞÖÇ\s]", "", text) #israil'in => "israil", "in"

    words = text.split()
    words = [w for w in words if len(w)>2]
    words = [w for w in words if w not in stopwords]

    return words