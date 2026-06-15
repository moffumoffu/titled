import pandas as pd
import re

def clean_text(text):
    text = re.sub(r'\[.*?\]', '', str(text))
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_file(input_file):
    df = pd.read_csv(input_file)
    df['text'] = df['text'].apply(clean_text)
    df = df[df['text'].str.len() > 10]
    return df

# Clean both files
df1 = clean_file("steam_reviews.csv")
df2 = clean_file("steam_reviews_2.csv")

# Combine
combined = pd.concat([df1, df2], ignore_index=True)

# Remove duplicates if any
combined = combined.drop_duplicates(subset="text")

print("Combined class balance:")
print(combined['voted_up'].value_counts())

combined.to_csv("steam_reviews_final.csv", index=False)
print(f"Saved {len(combined)} total cleaned reviews to steam_reviews_final.csv")