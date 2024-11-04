from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import oauth2, database, schemas, models, kp_api
from aiohttp import ClientSession


router = APIRouter(
    prefix="/movies",
    tags=['Movies']
)


@router.get('/search')
async def search_films(query: str, page: str = '1', current_user: models.User = Depends(oauth2.get_current_user), api: ClientSession = Depends(kp_api.get_session)):
    """
    Поиск фильма по ключевым
    """
    return await kp_api.search_by_keyword(api, query, page)

@router.get('/favorites')
async def get_favorites(
    current_user: models.User = Depends(oauth2.get_current_user)):
    return current_user.favorites

@router.get('/{film_id}', response_model=schemas.FilmResponse)
async def get_film(film_id: str, current_user: models.User = Depends(oauth2.get_current_user), api: ClientSession = Depends(kp_api.get_session)):
    """
    Получение фильма по id
    """
    return await kp_api.get_film(api, film_id)


@router.post('/favorites', status_code=status.HTTP_201_CREATED, response_model=schemas.FilmResponse)
async def add_favorite(
    film_id: str, 
    current_user: models.User = Depends(oauth2.get_current_user), 
    api: ClientSession = Depends(kp_api.get_session), 
    db: Session = Depends(database.get_db)):
    
    film_db = db.query(models.Film).get({'kinopoiskId': film_id})
    if film_db is None:
        film_data = await kp_api.get_film(api, film_id)
        film_schema = schemas.FilmResponse.model_validate(film_data)
        film_parse = database.parse_pydantic_schema(film_schema)
        film_db = models.Film(**film_parse)
        db.add(film_db)
        db.flush()
    
    current_user.favorites.append(film_db)
    db.commit()
    return film_db
    

@router.delete('/favorites/{film_id}')
async def delete_favorite(
    film_id: str,
    current_user: models.User = Depends(oauth2.get_current_user), 
    db: Session = Depends(database.get_db)):
    
    film_db = db.query(models.Film).get({'kinopoiskId': film_id})
    if film_db is None:
        raise HTTPException(status_code=404, detail="Фильм не найден") 
    if not film_db in current_user.favorites:
        raise HTTPException(status_code=400, detail="Фильм уже не в избранном") 
    current_user.favorites.remove(film_db)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Фильм удален из избранного"})
