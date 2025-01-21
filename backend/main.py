from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# FastAPI setup
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model
class ClipboardItem(BaseModel):
    content: str


# Routes
@app.post("/add")
async def add_clipboard_item(item: ClipboardItem):
    result = collection.insert_one(item.dict())
    return {"id": str(result.inserted_id)}


@app.get("/get_all")
async def get_all_clipboard_items():
    items = list(collection.find({}, {"_id": 0}))
    return items


@app.delete("/delete_all")
async def delete_all_clipboard_items():
    collection.delete_many({})
    return {"message": "All items deleted successfully"}


@app.get("/get")
async def get_clipboard_item(code: str):
    """Fetch clipboard item by code."""
    item = collection.find_one({"code": code}, {"_id": 0})
    if not item:
        raise HTTPException(status_code=404, detail="No data found for the provided code")
    return item


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
