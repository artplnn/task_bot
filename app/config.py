import os
import logging

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
URI = os.getenv("URI")

logging.basicConfig(
    level=logging.INFO
)
logger = logging.getLogger(__name__)
