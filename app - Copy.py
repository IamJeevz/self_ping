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

# Function to make HEAD requests every 10 minutes
def ping_every_10_minutes():
    while True:
        print("Pinging URLs...")
        for url in URLS:
            try:
                response = requests.head(url, timeout=60)
                print(f"[HEAD] {url} -> {response.status_code}")
            except Exception as e:
                print(f"[HEAD] {url} -> Error: {e}")
        print("Sleeping for 10 minutes...\n")
        time.sleep(120)  # 10 minutes

# Lifespan context: starts background thread safely
@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=ping_every_10_minutes, daemon=True)
    thread.start()
    yield  # Run the app
    # Thread will exit when app shuts down

# FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"status": "Ping scheduler is running."}

@app.head("/")
def root_head():
    return Response(status_code=200)
