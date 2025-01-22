import os
from dotenv import load_dotenv


load_dotenv()

VERTEXAI_PROJECT = os.getenv("VERTEXAI_PROJECT")
VERTEXAI_LOCATION = os.getenv("VERTEXAI_LOCATION")
