import os
import time
from dotenv import load_dotenv
from predibase import Predibase

load_dotenv()

pb = Predibase(api_token=os.environ.get("PREDIBASE_API_TOKEN"))

content = "The Los Angeles Dodgers won the World Series in 2020. Where was it played?"

lorax_client = pb.deployments.client("llama-3-1-8b-instruct")
start = time.time()
result = lorax_client.generate(content, max_new_tokens=1).generated_text
print("Time taken:", time.time() - start)

print(result)