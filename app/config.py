import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.rate_limiters import InMemoryRateLimiter

# Load environment variables
load_dotenv(r"C:\Users\jey\Dev\.env", override=True)

# Rate Limiter Configuration
# 10 requests per minute (approx every 6 seconds)
rate_limiter = InMemoryRateLimiter(
    requests_per_second=30/60,
    check_every_n_seconds=0.1,
    max_bucket_size=5
)

# Initialize Model (Groq)
# Using openai/gpt-oss-120b as requested
# Note: Ensure GROQ_API_KEY is set in your environment
model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    max_retries=2,
    rate_limiter=rate_limiter
)
