from pydantic import BaseModel
from typing import Optional
from enum import Enum
from app import models
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str
    
    
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    
    
    
class Country(BaseModel):
    country: str
    
    class Meta:
        orm_model = models.Country

class Genre(BaseModel):
    genre: str
    
    class Meta:
        orm_model = models.Genre



class FilmProdaction(str, Enum):
    NONE = None
    FILMING = 'FILMING'
    PRE_PRODUCTION = 'PRE_PRODUCTION'
    COMPLETED = 'COMPLETED'
    ANNOUNCED = 'ANNOUNCED'
    UNKNOWN = 'UNKNOWN'
    POST_PRODUCTION = 'POST_PRODUCTION'

class FilmType(str, Enum):
    NONE = None
    FILM = 'FILM'
    VIDEO = 'VIDEO'
    TV_SERIES = 'TV_SERIES'
    MINI_SERIES = 'MINI_SERIES'
    TV_SHOW = 'TV_SHOW'
    

class FilmResponse(BaseModel):
    kinopoiskId: int
    kinopoiskHDId: str
    imdbId: str
    nameRu: str
    nameEn: str | None = None
    nameOriginal: str
    posterUrl: str
    posterUrlPreview: str
    coverUrl: str
    logoUrl: str
    reviewsCount: int
    ratingGoodReview: int
    ratingGoodReviewVoteCount: int
    ratingKinopoisk: float
    ratingKinopoiskVoteCount: int
    ratingImdb: float
    ratingImdbVoteCount: int
    ratingFilmCritics: float
    ratingFilmCriticsVoteCount: int
    ratingAwait: int | None = None
    ratingAwaitCount: int
    ratingRfCritics: int
    ratingRfCriticsVoteCount: int
    webUrl: str
    year: int
    filmLength: int
    slogan: str
    description: str
    shortDescription: str
    editorAnnotation: str | None = None
    isTicketsAvailable: bool
    productionStatus: FilmProdaction | None = None
    type: FilmType | None = None
    ratingMpaa: str
    ratingAgeLimits: str
    hasImax: bool
    has3D: bool
    lastSync: datetime
    countries: list[Country] | None = None
    genres: list[Genre] | None = None
    startYear: int | None = None
    endYear: int | None = None
    serial: bool | None = None
    shortFilm: bool | None = None
    completed: bool | None = None
    
    class Meta:
        orm_model = models.Film

class UserResponse(BaseModel):
    username: str
    id: int
    favorites: list[FilmResponse] | None = None
    
    class Meta:
        orm_model = models.User

    
class FilmSearchResponse_films(BaseModel):
    filmId: int
    nameRu: str
    nameEn: str
    type: FilmType
    year: int
    description: str
    filmLength: int
    countries: list[Country]
    genres: list[Genre]
    rating: int
    ratingVoteCount: int
    posterUrl: str
    posterUrlPreview: str


class FilmSearchResponse(BaseModel):
    keyword: str
    pagesCount: int
    searchFilmsCountResult: int
    films: list[FilmSearchResponse_films]
