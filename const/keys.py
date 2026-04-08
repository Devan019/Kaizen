import os
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
open_weather_key = os.getenv("OPEN_WEATHER_API_KEY")
