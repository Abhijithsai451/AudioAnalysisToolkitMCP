import os
from dotenv import load_dotenv

load_dotenv()

def get_assemblyai_api_key():
    return os.getenv('ASSEMBLY_AI_API_KEY')
