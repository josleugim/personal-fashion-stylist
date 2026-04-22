import httpx
from jose import jwt, JWTError

GOOGLE_CERTS_URL = "https://www.googleapis.com/oauth2/v3/certs"


async def verify_google_token(id_token: str, client_id: str) -> dict | None:
    async with httpx.AsyncClient() as client:
        resp = await client.get(GOOGLE_CERTS_URL)
        jwks = resp.json()

    try:
        header = jwt.get_unverified_header(id_token)
    except JWTError:
        return None

    kid = header.get("kid")
    key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
    if not key:
        return None

    try:
        return jwt.decode(id_token, key, algorithms=["RS256"], audience=client_id)
    except JWTError:
        return None
