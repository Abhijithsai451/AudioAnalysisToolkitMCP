import os
from dotenv import load_dotenv

load_dotenv()

def get_assemblyai_api_key():
    api_key = os.getenv('ASSEMBLY_AI_API_KEY')
    print(f"Your API Key: {api_key}")
