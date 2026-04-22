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
from storage.save_csv import save_csv
from datetime import date, timedelta, datetime
from features.database_builder import build_dataset
from model.train_model import train_model
from database.trends_db import create_table, insert_trend_rows, fetch_all_trend
import time

def run_pipeline():
    print("Pipeline started...")
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

    X, words = compute_tfidf(all_titles) #ne yapıyor ?????
    print("\nTF-IDF words: ")
    print(words[:10])

    # ----- kaydediyoruz 

    today = date.today()
    today_str = str(date.today())
    today_counts = dict(words_counts)
    save_json(
        today_counts ,
        f"data/daily_counts/{today_str}_counts.json"
    )
    save_json(
        all_titles,
        f"data/raw_titles/{today_str}_titles.json"
    )

    yesterday = today - timedelta(days=1)
    yesterday_str = str(yesterday)
    yesterday_counts = load_json(f"data/daily_counts/{yesterday_str}_counts.json")
    if yesterday_counts is None:
        yesterday_counts = {}

    #save_json(tweets, f"data/x_posts/{today_str}_x_posts.json")

    trend_results = []

    all_words = set(today_counts.keys()) | set(yesterday_counts.keys())

    today_words = set(today_counts.keys())
    yesterday_words= set(yesterday_counts.keys())

    common_words= today_words & yesterday_words
    print("\nCommon words count: ", len(common_words))
    print("\nCommon words: \n")
    for word in common_words:
        print(word)

    for word in all_words:
        today_count = today_counts.get(word,0)
        yesterday_count = yesterday_counts.get(word, 0)
        
        growth_rate = compute_growth_rate(today_count, yesterday_count)
        trend_score = compute_trend_score(today_count, yesterday_count)

        trend_results.append({
            "word" : word,
            "today_count" : today_count,
            "yesterday_count" : yesterday_count,
            "growth_rate" : growth_rate,
            "trend_score" : trend_score
        })

    trend_results.sort(key= lambda x: x["trend_score"], reverse = True)
    print("\nTop trend candidates: \n")
    for item in trend_results[:10]:
        print(item)

    dataset_rows = build_dataset(
        common_words,
        today_counts,
        yesterday_counts,
        compute_growth_rate,
        compute_trend_score
    )

    print("\nDataset Preview: \n")
    for row in dataset_rows[:10]:
        print(row)

    save_json(
        dataset_rows,
        f"data/dataset/{today_str}_titles.json"
    )

    save_csv(
        dataset_rows,
        f"data/dataset/{today_str}_dataset.csv"
    )

    model = train_model(f"data/dataset/{today_str}_dataset.csv")

    create_table()
    insert_trend_rows(dataset_rows, today_str)
    all_db_rows = fetch_all_trend()
    print("\nDatabase rows preview: \n")
    for row in all_db_rows[:10]:
        print(row)
    print("Pipeline finished")

if __name__ == "__main__":
    while True:
        try:
            run_pipeline()
        except Exception as e:
            print("Error: ", e)
        print("Waiting 300 seconds...")
        time.sleep(300)


