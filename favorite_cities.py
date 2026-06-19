from models import FavoriteCity
from database import save_favorite_city, get_favorites_by_user, delete_favorite, user_by_id
from exceptions import CityNotInFavoritesError, UserNotExistError

def add_favorite(user_id, city):
    if not user_by_id(user_id):
        raise UserNotExistError(f"User with id '{user_id}' not found.")
    
    favorites = FavoriteCity(user_id=user_id, city=city)
    save_favorite_city(favorites)
    return favorites.model_dump()

def get_favorites(user_id):
    if not user_by_id(user_id):
        raise UserNotExistError(f"User with id '{user_id}' not found.")
    
    favorites_list = get_favorites_by_user(user_id)
    return favorites_list

def remove_favorite(user_id, city):
    if not user_by_id(user_id):
        raise UserNotExistError(f"User with id '{user_id}' not found.")
    
    result = delete_favorite(user_id, city)
    if result is False:
        raise CityNotInFavoritesError(f"City '{city}' is not in favorites for user '{user_id}'")

    if result is True:
        return {"status": "success", "message": f"'{city}' removed from favorites"}