from fastapi import FastAPI, Response
import requests
import threading
import time
from contextlib import asynccontextmanager

# List of URLs to ping
URLS = [
    "https://self-ping.onrender.com",
    "https://lunch-web.onrender.com"
]

# Function to make GET requests every 10 minutes
def ping_every_n_minutes():
    while True:
        print("Pinging URLs...")
        for url in URLS:
            try:
                response = requests.get(url, timeout=60)
                print(f"[GET] {url} -> {response.status_code}")
            except Exception as e:
                print(f"[GET] {url} -> Error: {e}")
        print("Sleeping for 2 minutes...\n")
        time.sleep(120)  # 2 minutes

# Lifespan context: starts background thread safely
@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=ping_every_n_minutes, daemon=True)
    thread.start()
    yield  # Run the app

# FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"status": "Ping scheduler is running."}

@app.head("/")
def root_head():
    return Response(status_code=200)
