import os
from dotenv import load_dotenv
from openai import OpenAI
import dspy
import time
from functools import wraps


load_dotenv()


BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
GOOGLE_SAFE_BROWSING_API_KEY = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")
URLSCAN_API_KEY = os.getenv("URLSCAN_API_KEY")


def retry(max_attempts=5, delay_seconds=5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts < max_attempts:
                        print(f"Retrying function '{func.__name__}'... Attempt {attempts} of {max_attempts}. Error: {e}")
                        time.sleep(delay_seconds)
                    else:
                        print(f"Max attempts reached for function '{func.__name__}', failing gracefully.")
                        raise
        return wrapper
    return decorator




def init_llm()-> None:
    """
    Initializes the LLM using DSPY
    :return:
    """
    print(f"Setting up LLM with {BASE_URL}, {API_KEY}, {MODEL_NAME}")

    lm = dspy.LM(api_base=BASE_URL,
                     api_key=API_KEY,
                     model=MODEL_NAME,
                     max_tokens=3000)

    dspy.configure(lm=lm)
