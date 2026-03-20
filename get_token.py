from livekit import api

API_KEY = "api_key"
API_SECRET = "arm_voice_agent_super_secret_key_2026_xyz"
ROOM_NAME = "bank-room"

# Ստեղծում ենք հաճախորդի մուտքի տոմս (Token)
token = api.AccessToken(API_KEY, API_SECRET)
token.with_identity("client_001")
token.with_name("Հաճախորդ")
token.with_grants(api.VideoGrants(room_join=True, room=ROOM_NAME))

print("\n--- ՊԱՏՃԵՆԵՔ ՆԵՐՔԵՎԻ TOKEN-Ը ---\n")
print(token.to_jwt())
print("\n----------------------------------\n")