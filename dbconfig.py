from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.venv/dbconfig.env')

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name_product = os.getenv("DB_NAME_PRODUCT")
db_name_order = os.getenv("DB_NAME_ORDER")


