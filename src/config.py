from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST=os.environ.get("DB_HOST")
DB_NAME=os.environ.get("DB_NAME")
DB_PASSWORD=os.environ.get("DB_PASSWORD")
DB_PORT=os.environ.get("DB_PORT")
DB_USER=os.environ.get("DB_USER")
SECRET = os.environ.get("SECRET")
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")