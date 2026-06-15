import requests
import csv
import time

def get_reviews(app_id, num_reviews=1000):
    reviews = []
    cursor = "*"
    
    while len(reviews) < num_reviews:
        url = f"https://store.steampowered.com/appreviews/{app_id}"
        params = {
            "json": 1,
            "filter": "recent",
            "language": "english",
            "num_per_page": 100,
            "cursor": cursor
        }
        
        response = requests.get(url, params=params).json()
        
        batch = response.get("reviews", [])
        if not batch:
            break
            
        for r in batch:
            reviews.append({
                "text": r["review"],
                "voted_up": r["voted_up"],
                "playtime_hours": r["author"]["playtime_forever"] // 60
            })
        
        cursor = response.get("cursor", "")
        if not cursor:
            break
        
        time.sleep(1)
    
    return reviews[:num_reviews]

app_id = "1372880"  # app id
reviews = get_reviews(app_id, num_reviews=2000)

with open("steam_reviews_2.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "voted_up", "playtime_hours"])
    writer.writeheader()
    writer.writerows(reviews)

print(f"Saved {len(reviews)} reviews")