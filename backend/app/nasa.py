import os, httpx, asyncio

NASA_KEY = os.getenv("NASA_API_KEY")

async def search_techport(query: str):
    url = f"https://api.nasa.gov/techport/api/projects?searchText={query}&api_key={NASA_KEY}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, timeout=30)
        data = r.json()
    # just return first project abstract for demo
    try:
        return data["projects"]["project"][0]["abstract"]
    except Exception:
        return "No NASA data found."
