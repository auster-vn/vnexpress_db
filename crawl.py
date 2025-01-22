import requests
import json
import csv

def crawl_vnexpress():
    base_url = "https://gw.vnexpress.net/tp?topic_id=25880&site_id=1003159&page={}&limit=1000"
    pages = range(1, 5)  
    
    results = []
    
    for page in pages:
        url = base_url.format(page)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get("data", {}).get("25880", {}).get("articles", {}).get("data", [])
            
            for article in articles:
                results.append({
                    "share_url": article.get("share_url", ""),
                    "title": article.get("title", "")
                })
        else:
            print(f"Failed to fetch page {page}: {response.status_code}")
    
    # Lưu dữ liệu vào file CSV
    csv_file = "vnexpress_articles.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["share_url", "title"])
        writer.writeheader()
        writer.writerows(results)
    
    print("Crawl completed. Data saved to vnexpress_articles.csv")

if __name__ == "__main__":
    crawl_vnexpress()
