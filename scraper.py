import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/"

def scrape_products():
    products = []
    page = 1
    
    while True:
        if page == 1:
            url = BASE_URL + "index.html"
        else:
            url = BASE_URL + f"page-{page}.html"
            
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        items = soup.find_all("article", class_="product_pod")
        
        for item in items:
            title = item.find("h3").find("a")["title"]
            price = item.find("p", class_="price_color").text.strip()
            link = item.find("h3").find("a")["href"]
            
            products.append({
                "id": link.split("/")[-2],
                "title": title,
                "price": item.find("p", class_="price_color").text.strip().encode("latin1").decode("utf8"),
                "url": "https://books.toscrape.com/catalogue/" + link.replace("../../../", ""),
                "scraped_at": str(datetime.now())
            })
        
        # Check if next page exists
        next_btn = soup.find("li", class_="next")
        if not next_btn:
            break
            
        page += 1
        print(f"Scraping page {page}...")
    
    return products

if __name__ == "__main__":
    products = scrape_products()
    print(f"Found {len(products)} products")
    for p in products[:3]:
        print(p)