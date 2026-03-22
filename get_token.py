import os
from livekit import api
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch secrets securely from environment variables
# Fallback to default values only if environment variables are missing
API_KEY = os.getenv("LIVEKIT_API_KEY", "devkey")
API_SECRET = os.getenv("LIVEKIT_API_SECRET", "arm_voice_agent_super_secret_key_2026_xyz")
ROOM_NAME = "bank-room"

# Create a secure access token for the client
token = api.AccessToken(API_KEY, API_SECRET)
token.with_identity("client_001")
token.with_name("Customer")
token.with_grants(api.VideoGrants(room_join=True, room=ROOM_NAME))

print("\n--- COPY THE TOKEN BELOW ---\n")
print(token.to_jwt())
print("\n----------------------------\n")