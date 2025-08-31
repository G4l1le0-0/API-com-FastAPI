from dataclasses import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    NOTA DE CORREÇÃO: O código original usava `Field(default=...)`, o que gerava um TypeError.
    Para classes que herdam de `BaseSettings` (da biblioteca pydantic-settings),
    a forma correta de definir um valor padrão é através de uma atribuição direta (=).
    DB_URL: str = 'postgresql+asyncpg://workout:workout@localhost/workout' 
    """
    DB_URL: str = 'postgresql+asyncpg://workout:workout@localhost/workout'

settings = Settings()