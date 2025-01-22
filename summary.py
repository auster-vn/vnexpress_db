import requests
import csv
import google.generativeai as genai
from bs4 import BeautifulSoup

def get_api_key():
    try:
        with open('api_key.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("API key file not found.")
        return ""

def summarize_content(content, api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Tóm tắt đoạn văn sau: {content}")
        
        # Check if response is valid
        if response:
            return response.text
        else:
            print(f"Gemini API returned an empty response.")
            return "No response"
    
    except Exception as e:
        print(f"Error during summarization: {e}")
        return f"Error summarizing content: {e}"

def extract_content(url, api_key):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text.strip() if soup.find('title') else "No Title"
        paragraphs = soup.find_all('p', class_='Normal')
        content = ' '.join(p.text.strip() for p in paragraphs)
        
        # Log content being sent for summarization
        print(f"Summarizing content from URL: {url}")
        summarized_content = summarize_content(content, api_key)
        
        return title, summarized_content

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return "No Title", f"Error: {e}"

def process_csv(input_csv, output_csv):
    api_key = get_api_key()
    if not api_key:
        print("No API key available.")
        return
    
    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        results = []
        
        for row in reader:
            url = row['share_url']
            title, summarized_content = extract_content(url, api_key)
            results.append({'title': title, 'content': summarized_content})
        
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Summarization completed. Data saved to {output_csv}")

if __name__ == "__main__":
    process_csv("vnexpress_articles.csv", "vnexpress_summarized.csv")

