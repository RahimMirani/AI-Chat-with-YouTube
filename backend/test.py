import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
  api_key= os.getenv("OPENAI_API_KEY")
)

response = client.responses.create(
  model="gpt-4o-mini",
  input="what is ai? Describe in 10 words",
  store=True,
)

print(response.output_text);
