from pytrends.request import TrendReq
import time 
import random

def get_trends():
    try:
        time.sleep(random.uniform(2,5)) 

        pytrends = TrendReq()
        trends= pytrends.trending_searches(pn="us")

        print("\nTrends dataframe: \n")
        print(trends)

        return trends[0].tolist()
    
    except Exception as error:
        print("Trends Error: ", error)
        return []