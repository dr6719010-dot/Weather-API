import logging
import os
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi import Depends, Header
from jwt_handler import verify_token
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from auth import register_user, login_user
from weather_client import get_current_weather, get_forecast
from favorite_cities import add_favorite, get_favorites, remove_favorite
from exceptions import (
    WeatherAPIError,
    CityNotFoundError,
    WeatherProviderError,
    UserAlreadyExistError,
    EmailNotFoundError,
    InvalidPasswordError,
    CityNotInFavoritesError,
    UserNotExistError,
    InvalidTokenError,
)
from models import RegisterRequest, LoginRequest
from database import create_tables

class AddFavoriteRequest(BaseModel):
    city: str

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Weather API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

create_tables()

@app.get("/", tags=["Health"])
def home():
    """Health check endpoint."""
    logger.info("Health check called")
    return {"message": "Nimbus is live 🚀"}

@app.post("/register", tags=["Authentication"])
def register(request: RegisterRequest):
    """Register a new user."""
    try:
        register_user(request.email, request.password, request.name)
        logger.info(f"User '{request.email}' registered successfully.")
        return {"status": "success", "message": "User registered successfully."}
    except UserAlreadyExistError as e:
        logger.error(f"Registration failed for '{request.email}': {str(e)}")
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


def get_current_user_id(authorization: str = Header(...)) -> str:
    """Extract and verify the JWT from the Authorization header, return the user_id."""
    # authorization will look like: "Bearer eyJhbGc..."
    try:
        token = authorization.replace("Bearer ", "")
        payload = verify_token(token)
        return payload["user_id"]
    except InvalidTokenError as e:
        logger.error(f"Token Invalid or Expired: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/login", tags=["Authentication"])
def login(request: LoginRequest):
    """Login a user."""
    try:
        result = login_user(request.email, request.password)
        logger.info(f"User '{request.email}' logged in successfully.")
        return {"status": "success", "message": "Login successful.", "token": result["token"], "user": result["user"]}
    except (EmailNotFoundError, InvalidPasswordError) as e:
        logger.error(f"Login failed for '{request.email}': {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
    
@app.get("/weather/{city}")
def get_weather(city: str):
    "getting the weather of city"
    try:
        weather = get_current_weather(city)
        logger.info("Weather of {city} shown successfully")
        return {"status": "success", "weather": weather}
    except CityNotFoundError as e:
        logger.error(f"City not found: '{city}'")
        raise HTTPException(status_code=404, detail=str(e))
    except WeatherProviderError as e:
        logger.error(f"Weather provider error for '{city}': {str(e)}")
        raise HTTPException(status_code=503, detail=f"Weather service error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error for '{city}': {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

@app.get("/forecast/{city}")
def forecast_for_city(city: str):
    "getting forecast of the city"
    try:
        forecast = get_forecast(city)
        logger.info("Forecast of {city} shown successfully")
        return {"status": "success", "forecast": forecast}
    except CityNotFoundError as e:
        logger.error(f"City not found for forecast: '{city}'")
        raise HTTPException(status_code=404, detail=str(e))
    except WeatherProviderError as e:
        logger.error(f"Weather provider error for forecast '{city}': {str(e)}")
        raise HTTPException(status_code=503, detail=f"Weather service error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error for forecast '{city}': {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
    
@app.post("/favorites", tags=["Favorites"])
def insert_favorite(request: AddFavoriteRequest, user_id: str = Depends(get_current_user_id)):
    try:
        new_fav = add_favorite(user_id, request.city)
        logger.info(f"New Favorite Ciyt {new_fav} is added")
        return {"status": "success", "new_fav_city": request.city}
    except UserNotExistError as e:
        logger.error(f"User not found when adding favorite: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error adding favorite: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

@app.get("/favorites", tags=["Favorites"])
def list_favorites(user_id: str = Depends(get_current_user_id)):
    try:
        favorites = get_favorites(user_id)
        return {"status": "success", "favorites": favorites}
    except UserNotExistError as e:
        logger.error(f"User not found when fetching favorites: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error fetching favorites: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
    
@app.delete("/favorites/{city}", tags=["Favorites"])
def remove_favorite_endpoint(city: str, user_id: str = Depends(get_current_user_id)):
    try:
        deleted_data = remove_favorite(user_id, city)
        return {"status": "success", "deleted_city": city}
    except UserNotExistError as e:
        logger.error(f"User not found when removing favorite: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except CityNotInFavoritesError as e:
        logger.error(f"City '{city}' not in favorites for user '{user_id}'")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error removing favorite: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")