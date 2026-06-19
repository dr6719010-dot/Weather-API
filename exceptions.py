class WeatherAPIError(Exception):
    """Base class for exceptions in the Weather API application."""
    pass

class CityNotFoundError(WeatherAPIError):
    """Exception raised when OpenWeatherMap cannot find the requested city."""
    pass

class WeatherProviderError(WeatherAPIError):
    """Exception raised when OpenWeatherMap returns an unexpected error (bad key, server issue, etc.)."""
    pass

class JWTError(WeatherAPIError):
    """JWT ERROR ON VERIFICATION FAILURE"""
    pass

class InvalidTokenError(JWTError):
    """Invalid or expired Token"""
    pass

class UserAlreadyExistError(WeatherAPIError):
    "User Already Exist"
    pass

class InvalidPasswordError(WeatherAPIError):
    "Invalid Password"
    pass

class UserNotExistError(WeatherAPIError):
    """User doesn't exist"""
    pass

class EmailNotFoundError(WeatherAPIError):
    "User doesn't exist"
    pass

class CityNotInFavoritesError(WeatherAPIError):
    "No Favorite City yet"
    pass