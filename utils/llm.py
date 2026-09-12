from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

def get_llm():
	api_key=os.getenv("GOOGLE_API_KEY")

	if not api_key:
		raise ValueError(
			"Google API key not there, please check."
		)

	return ChatGoogleGenerativeAI(
		model="gemini-3.1-flash-lite",
		google_api_key=api_key,
		temperature=0
	)