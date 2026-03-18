import httpx
from fastapi import HTTPException


ARTIC_API_BASE = "https://api.artic.edu/api/v1"


async def check_place_exists(external_id: int) -> bool:
    url = f"{ARTIC_API_BASE}/artworks/{external_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            return True, data.get("title", "Unknown")
        else:
            return False, None


async def fetch_place_data(external_id: int):
    url = f"{ARTIC_API_BASE}/artworks/{external_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=400, detail="Place not found in external API")
        data = response.json()
        return {
            "external_id": external_id,
            "title": data.get("title", "Unknown"),
            "api_data": data
        }
