import asyncio
import aiohttp


async def get_data_api(city: str):

    url = f"https://api.artic.edu/api/v1/places/search?q={city}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f"--- Response status -> {response.status} ---")
            return await response.json()

if __name__ == "__main__":
    print(asyncio.run(get_data_api("Paris")))