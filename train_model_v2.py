import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load both datasets
df1 = pd.read_csv("steam_reviews_final.csv")
df2 = pd.read_csv("slang_data.csv", encoding="cp1252")

# Combine
df = pd.concat([df1, df2], ignore_index=True)
df = df.drop_duplicates(subset="text")

print("Combined class balance:")
print(df['voted_up'].value_counts())

X = df["text"]
y = df["voted_up"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(max_features=8000, ngram_range=(1, 3))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred, target_names=["Negative", "Positive"]))

joblib.dump(model, "sentiment_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Model updated and saved")