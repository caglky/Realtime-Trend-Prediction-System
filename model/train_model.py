import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib 

def train_model(dataset_path):
    df = pd.read_csv(dataset_path)
    print(df.columns.tolist())
    X = df[["today_count", "yesterday_count ", "growth_rate", "trend_score"]]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\nAccuracy: ", accuracy_score(y_test, y_pred))
    print("\nClassification Report: \n")
    print(classification_report(y_test, y_pred))
    joblib.dump(model, "model/model.pkl")

    return model