import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env if present

TRANSACTION_SERVICE_URL = os.getenv('TRANSACTION_SERVICE_URL', 'http://localhost:3000/transaction-service/api')

APP_PORT = int(os.getenv('PORT', 5000))
APP_DEBUG = (os.getenv('DEBUG', 'False').lower() == 'true')