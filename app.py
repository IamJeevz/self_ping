from fastapi import FastAPI, Response
import requests
import threading
import time
from contextlib import asynccontextmanager

# Self URL for local testing
SELF_URL = "https://self-ping.onrender.com"

# List of URLs to ping
URLS = [
    "https://resume-wzmz.onrender.com",
    "https://lunch-form.onrender.com",
    SELF_URL
]

# Function to make HEAD requests every 30 minutes
def ping_every_30_minutes():
    while True:
        print("Pinging URLs...")
        for url in URLS:
            try:
                response = requests.head(url, timeout=10)
                print(f"[HEAD] {url} -> {response.status_code}")
            except Exception as e:
                print(f"[HEAD] {url} -> Error: {e}")
        print("Sleeping for 2 minutes...\n")
        time.sleep(120)  # 30 minutes

# Lifespan context: starts background thread safely
@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=ping_every_30_minutes, daemon=True)
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
