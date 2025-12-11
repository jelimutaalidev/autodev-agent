import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.rate_limiters import InMemoryRateLimiter

# Load environment variables
load_dotenv(os.path.join("..", ".env"), override=True)

# Rate Limiter Configuration
# 10 requests per minute (approx every 6 seconds)
rate_limiter = InMemoryRateLimiter(
    requests_per_second=30/60,
    check_every_n_seconds=0.1,
    max_bucket_size=5
)

# Initialize Model
# Support for "provider:model" format (e.g. "groq:llama3-70b-8192")
llm_model = os.getenv("LLM_MODEL", "openai:gpt-4o")

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
