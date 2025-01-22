import requests
import csv
from bs4 import BeautifulSoup

def extract_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text.strip() if soup.find('title') else "No Title"
        paragraphs = soup.find_all('p', class_='Normal')
        content = ' '.join(p.text.strip() for p in paragraphs)
        return title, content
    else:
        print(f"Failed to fetch {url}")
        return "No Title", ""

def process_csv(input_csv, output_csv):
    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        results = []
        
        for row in reader:
            url = row['share_url']
            title, content = extract_content(url)
            results.append({'title': title, 'content': content})
        
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Extraction completed. Data saved to {output_csv}")

if __name__ == "__main__":
    process_csv("vnexpress_articles.csv", "vnexpress_contents.csv")
