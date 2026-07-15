import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# This reads the .env file and loads GOOGLE_API_KEY into the program
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

# Stop the program early with a clear message if the key is missing
if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found. Please add it to your .env file."
    )

# This model object is what the rest of the project will use to talk to Gemini
# Low temperature keeps support answers consistent instead of random
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.2,
)
