from api.news_api import get_news
#from api.trends_api import get_trends
from api.web_scraping import get_tr_news
#from api.twitter_api import get_tweets => bearer_token ile dahi veri gelmiyor 
from preprocessing.cleaning import clean_text
from features.frequency_features import get_word_frequencies
from features.tfidf_features import compute_tfidf
from features.trend_score import compute_growth_rate, compute_trend_score
from storage.save_data import save_json
from storage.load_data import load_json
from datetime import date, timedelta

# ---- verileri topluyoruz 
news = get_news()
print("TR New from NewsAPI: ", news)
for article in news["articles"]:
    print(article["title"])
# because the content come empty, I did "web-scraping"

bbc_news = get_tr_news("https://www.bbc.com/turkce")
print("\nTR News from BBC: \n", bbc_news)

ntv_news = get_tr_news("https://www.ntv.com.tr")
print("\nTR News from NTV: \n", ntv_news)

#tweets = get_tweets("gülistan doku lang:tr -is:retweet", max_results=10)
#if "data" in tweets:
#    for post in tweets["data"]:
#        print(post["text"])
#else:
#    print("Post bulunamado ya da hata var")
#    print(tweets)

#trends = get_trends()
#print("\nGoogle Trends: \n", trends) => bot sandığı için google trends'den cevap alamıyorum, şimdilik bıraktım

all_titles = bbc_news + ntv_news

# ------ en çok geçenleri buluyoruz, temizliyoruz

words_counts = get_word_frequencies(all_titles, clean_text)
print("\nMost Common Words: \n")
print(words_counts.most_common(10))

# NLP, TF-IDF 

X, words = compute_tfidf(all_titles)
print("\nTF-IDF words: ")
print(words[:10])

# ----- kaydediyoruz 

today = date.today()
today_str = str(date.today())
save_json(
    dict(words_counts) ,
    f"data/daily_counts/{today_str}_counts.json"
)
save_json(
    all_titles,
    f"data/raw_titles/{today_str}_titles.json"
)

yesterday = today - timedelta(days=1)
yesterday_str = str(yesterday)
yesterday_counts = load_json(f"data/daily_counts{yesterday_str}_counts.json")
if yesterday_counts is None:
    yesterday_counts = {}

#save_json(tweets, f"data/x_posts/{today_str}_x_posts.json")

