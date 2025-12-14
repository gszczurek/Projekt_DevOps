import os
import time
import csv
import json
import logging
from flask import Flask
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

from src.db import db
from src.models import User

OUTPUT_DIR = '/app/seed/output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(OUTPUT_DIR, 'seed.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    "DATABASE_URL", "postgresql://postgres:root123@db:5432/app_db"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

sample_users = [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bobaa", "email": "bobaa@example.com"},
    {"name": "Charlie", "email": "charlie@example.com"},
    {"name": "David", "email": "david@example.com"},
    {"name": "Eve", "email": "eve@example.com"},
]

def wait_for_db(max_attempts=10, delay=3):
    with app.app_context():
        for attempt in range(max_attempts):
            try:
                db.session.execute(text("SELECT 1"))
                print("Database is ready!")
                return
            except OperationalError:
                print(f"Database not ready, retry {attempt + 1}/{max_attempts}...")
                time.sleep(delay)
        raise Exception("Database not ready after several attempts")

def seed():
    wait_for_db()

    with app.app_context():
        for u in sample_users:
            user = User(name=u["name"], email=u["email"])
            db.session.add(user)
        db.session.commit()
        logging.info(f"Inserted {len(sample_users)} users into database.")

        with open(os.path.join(OUTPUT_DIR, 'users.csv'), 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["name", "email"])
            writer.writeheader()
            for u in sample_users:
                writer.writerow(u)
        logging.info("Saved users.csv")

        with open(os.path.join(OUTPUT_DIR, 'users.json'), 'w') as jsonfile:
            json.dump(sample_users, jsonfile, indent=4)
        logging.info("Saved users.json")

if __name__ == "__main__":
    seed()
    print(f"Seeding done. Files: {OUTPUT_DIR}/users.csv, {OUTPUT_DIR}/users.json, {OUTPUT_DIR}/seed.log")
