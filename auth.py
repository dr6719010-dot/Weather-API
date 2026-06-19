import bcrypt
from models import User
from jwt_handler import create_token
from database import get_user_by_email, save_user
from exceptions import EmailNotFoundError, InvalidPasswordError, UserAlreadyExistError

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
        # Convert both strings to bytes to perform the check
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(email: str, password: str, name: str):
    """Register a new user."""
    #check if user already exist
    if get_user_by_email(email):
        raise UserAlreadyExistError(f"Email already exist")
    
    # Hash the password
    hashed_password = hash_password(password)

    #Create A new User instance
    new_user = User(email=email, password=hashed_password, name=name)

    save_user(new_user)
    user_dict = new_user.model_dump()
    user_dict.pop("password")  # remove before returning
    return user_dict

    
def login_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        raise EmailNotFoundError(f"Invalid password or email.")

    if not verify_password(password, user['password']):
        raise InvalidPasswordError("Invalid password or email.")
    token = create_token({"user_id": user["user_id"]})
    safe_dict = user.pop("password")
    return {"token": token, "user": user}