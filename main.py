from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from database import init_db, get_all_products
from main_runner import run

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"status": "Price Monitor is running"}

@app.get("/products")
def get_products():
    products = get_all_products()
    return {
        "total": len(products),
        "products": [
            {
                "title": p[1],
                "current_price": p[2],
                "url": p[3],
                "first_seen": p[4],
                "last_seen": p[5]
            }
            for p in products
        ]
    }
@app.get("/run")
def run_scraper():
    run()
    return {"status": "Scraper executed successfully"}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    products = get_all_products()
    
    rows = ""
    for p in products:
        rows += f"""
        <tr>
            <td>{p[1]}</td>
            <td>{p[2]}</td>
            <td>{p[5]}</td>
            <td><a href="{p[3]}" target="_blank">View</a></td>
        </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Price Monitor Dashboard</title>
        <style>
            body {{ font-family: Arial; margin: 20px; background: #f5f5f5; }}
            h1 {{ color: #2E75B6; }}
            table {{ width: 100%; border-collapse: collapse; background: white; }}
            th {{ background: #2E75B6; color: white; padding: 10px; text-align: left; }}
            td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
            tr:hover {{ background: #f0f0f0; }}
            a {{ color: #2E75B6; }}
        </style>
    </head>
    <body>
        <h1>📊 Price Monitor Dashboard</h1>
        <p>Total products tracked: <strong>{len(products)}</strong></p>
        <table>
            <tr>
                <th>Title</th>
                <th>Current Price</th>
                <th>Last Seen</th>
                <th>Link</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """
    return html