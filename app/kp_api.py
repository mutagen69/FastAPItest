import aiohttp
from app import schemas
from fastapi import HTTPException
import os


async def get_session():
    session = aiohttp.ClientSession(headers={'X-API-KEY': os.getenv('KINOPOISK_API_KEY'), 'Content-Type': 'application/json'})
    try:
        yield session
    finally:
        await session.close()
        

async def send_api(session: aiohttp.ClientSession, method: str, api_method: str, params: dict = None)->list|dict:
    """
    Выполняет метод апи на кинопоиске
    """
    response = await session.request(method, os.getenv('KINOPOISK_API')+api_method, params=params)
    if 300 < response.status < 200:
        raise HTTPException(status_code=response.status, detail=await response.text())
    data = await response.json()
    return data

        
async def search_by_keyword(session: aiohttp.ClientSession, query: str, page: str = '1'):
    """
    Поиск по ключевым словам
    """
    return await send_api(session, 
                          'get', '/api/v2.1/films/search-by-keyword', {
                              'keyword': query, 'page': page })
    

async def get_film(session: aiohttp.ClientSession, film_id: str)->dict:
    """
    Получение фильма по id
    """
    return await send_api(session,
                          'get', f'/api/v2.2/films/{film_id}')