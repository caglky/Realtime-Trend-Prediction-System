def build_dataset(common_words, today_counts, yesterday_counts, compute_growth_rate, compute_trend_score ):
    dataset_rows = []
    for word in common_words: 
        today_count = today_counts.get(word,0)
        yesterday_count = yesterday_counts.get(word,0)
        growth_rate = compute_growth_rate(today_count, yesterday_count)
        trend_score = compute_trend_score(today_count, yesterday_count)
        label = 1 if growth_rate > 1 else 0
        dataset_rows.append({
            "word" : word,
            "today_count" : today_count,
            "yesterday_count " : yesterday_count,
            "growth_rate" : growth_rate,
            "trend_score" : trend_score,
            "label" : label
        })
    return dataset_rows