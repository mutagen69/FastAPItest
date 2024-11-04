from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy import String, Integer, ForeignKey, Column, Boolean, DateTime, func, Table, MetaData

class Base(DeclarativeBase):
    pass

film_genres_table = Table(
    "film_genres",
    Base.metadata,
    Column("film_id", Integer, ForeignKey("films.kinopoiskId")),
    Column("genre_id", Integer, ForeignKey("genres.id")),
)

film_countries_table = Table(
    "film_countries",
    Base.metadata,
    Column("film_id", Integer, ForeignKey("films.kinopoiskId")),
    Column("country_id", Integer, ForeignKey("countries.id")),
)
    
user_favorites_table = Table(
    "user_favorites",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("film_id", Integer, ForeignKey("films.kinopoiskId")),
)


class Film(Base):
    """
    Модель фильма
    """  
    __tablename__ = "films"
    
    kinopoiskId = Column(Integer, primary_key=True)
    users = relationship("User", secondary=user_favorites_table, back_populates='favorites')
    countries = relationship("Country", secondary=film_countries_table, back_populates='films')
    genres = relationship("Genre", secondary=film_genres_table, back_populates='films')
    
    kinopoiskHDId = Column(String(32))
    imdbId = Column(String(32))
    nameRu = Column(String(255))
    nameEn = Column(String(255), nullable=True, default=None)
    nameOriginal = Column(String(255))
    posterUrl = Column(String(255))
    posterUrlPreview = Column(String(255))
    coverUrl = Column(String(255))
    logoUrl = Column(String(255))
    reviewsCount = Column(Integer)
    ratingGoodReview = Column(Integer)
    ratingGoodReviewVoteCount = Column(Integer)
    ratingKinopoisk = Column(Integer)
    ratingKinopoiskVoteCount = Column(Integer)
    ratingImdb = Column(Integer)
    ratingImdbVoteCount = Column(Integer)
    ratingFilmCritics = Column(Integer)
    ratingFilmCriticsVoteCount = Column(Integer)
    ratingAwait = Column(Integer, nullable=True, default=None)
    ratingAwaitCount = Column(Integer)
    ratingRfCritics = Column(Integer)
    ratingRfCriticsVoteCount = Column(Integer)
    webUrl = Column(String(255))
    year = Column(Integer)
    filmLength = Column(Integer)
    slogan = Column(String(255))
    description = Column(String(1024))
    shortDescription = Column(String(255))
    editorAnnotation = Column(String(255), nullable=True, default=None)
    isTicketsAvailable = Column(Boolean)
    productionStatus = Column(String(55), nullable=True, default=None)
    type = Column(String(55), nullable=True, default=None)
    ratingMpaa = Column(String(5))
    ratingAgeLimits = Column(String(10))
    hasImax = Column(Boolean)
    has3D = Column(Boolean)
    lastSync = Column(DateTime(timezone=True), onupdate=func.now())
    startYear = Column(Integer, nullable=True, default=None)
    endYear = Column(Integer, nullable=True, default=None)
    serial = Column(Boolean, nullable=True, default=None)
    shortFilm = Column(Boolean, nullable=True, default=None)
    completed = Column(Boolean, nullable=True, default=None)

class Country(Base):
    """
    Модель страны
    """
    __tablename__ = "countries"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(255))
    films = relationship("Film", secondary=film_countries_table, back_populates='countries')

class Genre(Base):
    """
    Модель жанра
    """
    
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, autoincrement=True)
    genre = Column(String(255))
    films = relationship("Film", secondary=film_genres_table, back_populates='genres')
    

class User(Base):
    """
    Модель юзера
    """  
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True)
    password = Column(String(64))
    
    favorites = relationship("Film", secondary=user_favorites_table, back_populates='users')
    