import os
from dotenv import load_dotenv

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR=os.path.abspath(os.path.join(FILE_DIR, os.pardir))
load_dotenv(os.path.join(BASE_DIR, ".env"))

class Config:
    def __init__(self):
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_USER = os.getenv("DB_USER", "user")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
        self.DB_NAME = os.getenv("DB_NAME", "mydatabase")
        self.DB_PORT = os.getenv("DB_PORT", 3306)
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

    def is_production(self):
        return self.ENVIRONMENT == "production"
    
    def set_production(self):
        self.ENVIRONMENT = "production"
    
credentials=Config()
DATABASE_URL=f'mysql+pymysql://'+credentials.DB_USER+':'+credentials.DB_PASSWORD+'@'+credentials.DB_HOST+':'+str(credentials.DB_PORT)+'/'+credentials.DB_NAME
TOKEN_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
SECRET_KEY='secret'