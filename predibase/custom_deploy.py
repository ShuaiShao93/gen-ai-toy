import os
import time
from dotenv import load_dotenv
from predibase import DeploymentConfig, Predibase

load_dotenv()

pb = Predibase(api_token=os.environ.get("PREDIBASE_API_TOKEN"))

pb.deployments.create(
    name="my-llama-3-1-8b-instruct",
    config=DeploymentConfig(
        base_model="llama-3-1-8b-instruct",
        accelerator="a100_80gb_100",
        # cooldown_time=3600, # Value in seconds, defaults to 3600 (1hr)
        min_replicas=0,  # Auto-scales to 0 replicas when not in use
        max_replicas=1
    )
    # description="", # Optional
)

content = "The Los Angeles Dodgers won the World Series in 2020. Where was it played?"

lorax_client = pb.deployments.client("my-llama-3-1-8b-instruct")
start = time.time()
result = lorax_client.generate(content, max_new_tokens=1).generated_text
print("Time taken:", time.time() - start)

print(result)

# pb.deployments.delete("my-llama-3-1-8b-instruct")