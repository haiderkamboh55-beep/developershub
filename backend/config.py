import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-super-secret-key-developershub')
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost:5432/developershub')
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')

