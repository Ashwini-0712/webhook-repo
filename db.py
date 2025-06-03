from pymongo import MongoClient
from urllib.parse import quote_plus

# Replace this with your real password (with special characters)
raw_password = "Ashwini@4080"  # <-- put your real password here, inside quotes

# Encode the password so MongoDB URI works
encoded_password = quote_plus(raw_password)

# Use the encoded password in the MongoDB connection string
mongo_uri = f"mongodb+srv://Ashwini:{encoded_password}@githubwebhookdb.kvtcqr2.mongodb.net/?retryWrites=true&w=majority&appName=githubwebhookdb"

client = MongoClient(mongo_uri)
db = client["githubwebhook"]      # replace with your actual database name if different
collection = db["payloads"]       # replace with your actual collection name if different
