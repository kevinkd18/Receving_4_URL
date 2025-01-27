import os
import certifi
from flask import Flask, render_template, redirect, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
WEBHOOK_URL = os.getenv("WEBHOOK_URLg")  # Primary webhook for final verification
WEBHOOK_URL2 = os.getenv("WEBHOOK_URL2g")  # Current webhook

# --- MongoDB Setup ---
try:
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    db = client["media_shortener"]
    users_collection = db["users"]
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"MongoDB connection error: {e}")
    exit(1)

app = Flask(__name__)

@app.route("/verify/<unique_id>", methods=["GET"])
def verify_page(unique_id):
    """
    Serve the initial verification page.
    After 5 seconds, redirects to WEBHOOK_URL.
    """
    try:
        return render_template("verify.html", unique_id=unique_id, webhook_url=WEBHOOK_URL)
    except Exception as e:
        print(f"Error rendering verification page: {e}")
        return "<h1>Something went wrong.</h1>", 500


@app.route("/verify_next/<unique_id>", methods=["GET"])
def verify_next(unique_id):
    """
    Serve the third verification page.
    After 5 seconds, redirects back to WEBHOOK_URL for the final step.
    """
    try:
        return render_template("verify_next.html", unique_id=unique_id, webhook_url=WEBHOOK_URL)
    except Exception as e:
        print(f"Error rendering next verification page: {e}")
        return "<h1>Something went wrong.</h1>", 500


@app.route("/verify_continue/<unique_id>", methods=["GET"])
def redirect_to_webhook(unique_id):
    """
    Redirect the user to the primary webhook's final verification page.
    """
    try:
        # Redirect to the primary webhook's verification page
        return redirect(f"{WEBHOOK_URL}/verify_continue/{unique_id}")
    except Exception as e:
        print(f"Error redirecting to webhook: {e}")
        return "<h1>Something went wrong during redirection.</h1>", 500

@app.route("/", methods=["GET"])
def index():
    return ""
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
