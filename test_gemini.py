import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print("API key found:", api_key is not None)

genai.configure(api_key=api_key)

model = genai.GenerativeModel("models/gemini-2.5-flash")
print("Before API call")

response = model.generate_content("Say hello")

print("After API call")
print(response.text)