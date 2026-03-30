from scraper import scrape_products
from database import init_db, save_products, get_all_products
from telegram_bot import send_message

def run():
    print("Starting price monitor...")
    send_message("✅ Price Monitor is running!")
    init_db()
    
    # Scrape current products
    products = scrape_products()
    print(f"Scraped {len(products)} products")
    
    # Save and detect changes
    new_products, price_changes = save_products(products)
    
    # Alert for new products
    if new_products:
        send_message(f"🆕 {len(new_products)} new products found!")
        for product in new_products:
            send_message(
                f"🆕 <b>New Product</b>\n\n"
                f"📚 <b>{product['title']}</b>\n"
                f"💰 Price: {product['price']}\n"
                f"🔗 <a href='{product['url']}'>View Product</a>"
            )
            print(f"New product: {product['title']}")
    
    # Alert for price changes
    if price_changes:
        for change in price_changes:
            emoji = "🔥" if change["old_price"] > change["new_price"] else "📈"
            send_message(
                f"{emoji} <b>Price Change!</b>\n\n"
                f"📚 <b>{change['title']}</b>\n"
                f"💰 Old: {change['old_price']}\n"
                f"💰 New: {change['new_price']}\n"
                f"🔗 <a href='{change['url']}'>View Product</a>"
            )
            print(f"Price change: {change['title']} - {change['old_price']} → {change['new_price']}")
    
    if not new_products and not price_changes:  
        print("No changes detected")

if __name__ == "__main__":
    run()