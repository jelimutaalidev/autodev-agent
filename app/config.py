import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.rate_limiters import InMemoryRateLimiter

# Load environment variables
# Load environment variables
# Ensure we look for .env in the project root relative to this file
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "..", ".env")
load_dotenv(env_path, override=True)

# Rate Limiter Configuration
# 10 requests per minute (approx every 6 seconds)
rate_limiter = InMemoryRateLimiter(
    requests_per_second=30/60,
    check_every_n_seconds=0.1,
    max_bucket_size=5
)

# Initialize Model
# Support for "provider:model" format (e.g. "groq:llama3-70b-8192")
llm_model = os.getenv("LLM_MODEL")

if not llm_model:
    raise ValueError(
        "LLM_MODEL environment variable is missing. "
        "Please create a .env file and set LLM_MODEL (e.g., LLM_MODEL=groq:llama3-70b-8192)."
    )

if ":" in llm_model:
    provider, model_name = llm_model.split(":", 1)
    model = init_chat_model(
        model_name, 
        model_provider=provider, 
        rate_limiter=rate_limiter
    )
else:
    model = init_chat_model(
        llm_model, 
        rate_limiter=rate_limiter
    )
