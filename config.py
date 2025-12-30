import os
from dotenv import load_dotenv

load_dotenv()

KIS_BASE_URL = 'https://openapi.koreainvestment.com:9443'
KIS_APP_KEY=os.getenv('KIS_APP_KEY')
KIS_APP_SECRET=os.getenv('KIS_APP_SECRET')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, "token_info.json")