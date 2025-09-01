from fastapi import FastAPI
from workout_api.routers import api_router

app = FastAPI(title='WorkoutApi')
app.include_router(api_router)

from fastapi_pagination import add_pagination

add_pagination(app)


