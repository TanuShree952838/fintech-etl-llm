import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_insights(data):
    prompt = f"You are a fintech analyst. Based on the following performance data for {data['date']}, provide a short summary and 3 actionable recommendations to improve performance. Data:\n\n{data}"
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=150
    )
    
    return response.choices[0].text.strip()
