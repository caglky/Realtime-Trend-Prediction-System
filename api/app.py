from fastapi import FastAPI
import sqlite3 
import json 
import os 
from datetime import date, timedelta
from glob import glob
import joblib
import pandas as pd

app = FastAPI()

def get_db_connection():
    conn = sqlite3.connect("database/trends.db")
    conn.row_factory = sqlite3.Row
    return conn

def load_json(filepath) :
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileExistsError:
        return {}

def get_latest_dataset_path():
    dataset_files = glob("data/dataset/*_dataset.csv")
    if not dataset_files:
        None
    dataset_files.sort(key = os.path.getatime)
    return dataset_files[-1]


def load_model():
    model_path = "model/model.pkl"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

model = load_model()

#---endpoints---

@app.get("/") 
def home():
    return {"message" : "Trend Prediction API is working"}

@app.get("/trends")
def get_trends():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, word, today_count, yesterday_count, growth_rate, trend_score, label
        FROM trends
        ORDER BY trend_score DESC 
        LIMIT 10 """)
    
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/dataset")
def get_dataset():
    latest_dataset = get_latest_dataset_path()
    if latest_dataset is None:
        return {"error" : "No dataset file found"}
    df = pd.read_csv(latest_dataset)
    return {
        "dataset_file" : latest_dataset,
        "row_count" : len(df),
        "preview" : df.head(20).to_dict(orient = "records")
    }

@app.get("/predict")
def predict(today_count: int, yesterday_count: int):
    if model is None:
        return {"error" : "Model file not found"}
    if yesterday_count == 0:
        growth_rate = (today_count-yesterday_count) / (yesterday_count+1)
    else:
        growth_rate = (today_count-yesterday_count) / yesterday_count 
    trend_score = today_count * growth_rate
    X = [[today_count, yesterday_count, growth_rate, trend_score]]
    prediction = model.predict(X)[0]
    return {
        "today_count" : today_count,
        "yesterday_count" : yesterday_count,
        "growth_rate" : growth_rate,
        "trend_score" : trend_score,
        "trend" : bool(prediction)
    }


@app.get("/top-today")
def top_today():
    today_str = str(date.today())
    filepath = f"data/daily_counts/{today_str}_counts.json"
    counts = load_json(filepath)
    if not counts:
        return {"error" : f"No count file found for today: {filepath}"}
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return {
        "date" : today_str,
        "top_today" : [{"word" : word, "count": count} for word, count in sorted_counts[:10]]
    }

@app.get("/top-yesterday")
def top_yesterday():
    yesterday_str = str(date.today() - timedelta(days=1))
    filepath = f"data/daily_counts/{yesterday_str}_counts.json"
    counts = load_json(filepath)
    if not counts:
        return {"error": f"No count file fount for yesterday: {filepath}"}
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return {
        "date" : yesterday_str,
        "top_yesterday" : [{"word": word, "count": count} for word, count in sorted_counts[:10]]
    }

@app.get("/top-words")
def top_words():
    today_str = str(date.today())
    yesterday_str = str(date.today() - timedelta(days=1))
    today_counts = load_json(f"data/daily_counts/{today_str}_counts.json")
    yesterday_counts = load_json(f"data/daily_counts/{yesterday_str}_counts.json")
    if not today_counts and not yesterday_counts:
        return {"error" : "No count files found for today or yesterday"}
    today_sorted = sorted(today_counts.items(), key=lambda x: x[1], reverse=True)
    yesterday_sorted = sorted(yesterday_counts.items(), key=lambda x: x[1], reverse=True)

    return {
        "today": {
            "date" : today_str,
            "top_words" : [{"word" : word, "count" : count} for word, count in today_sorted[:10]]
        },
        "yesterday" : {
            "date" : yesterday_str,
            "top_words" : [{"word" : word, "count" : count} for word, count in today_sorted[:10]]
        }
    }

