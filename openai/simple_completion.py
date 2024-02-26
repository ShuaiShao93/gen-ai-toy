from dotenv import load_dotenv
import httpx
from openai import OpenAI, timeout
from openai._base_client import SyncHttpxClientWrapper

# Set OPENAI_API_KEY in .env file
load_dotenv()

# Showcase how to extract each response, even if retry is triggered internally.
def _print_response_status_code(response: httpx.Response):
    print("Response status code", response.status_code)

http_client = SyncHttpxClientWrapper(
  base_url="https://api.openai.com/v1",
  timeout=timeout,
  follow_redirects=True,
  event_hooks={"response": [_print_response_status_code]},
)
client = OpenAI(http_client=http_client)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

print(response.choices[0].message)