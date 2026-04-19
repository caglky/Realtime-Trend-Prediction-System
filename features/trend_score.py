def compute_growth_rate(today_count, yesterday_count):
    if yesterday_count == 0:
        if today_count == 0:
            return 0
    return (today_count - yesterday_count) / yesterday_count

def compute_trend_score(today_count, yesterday_count):
    growth_rate = compute_growth_rate(today_count, yesterday_count)
    return today_count * growth_rate

