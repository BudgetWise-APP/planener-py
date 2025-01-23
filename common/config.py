from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = "HS256"
ORIGINS = [
    'http://localhost:8899',
    'http://10.0.11.165:8899',
    'http://10.2.0.2:8899',
    'https://budgetwise-chi.vercel.app',
]
