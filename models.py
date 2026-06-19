from pydantic import BaseModel, field_validator, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("password must contain at least one number")
        if len(v) > 72:
            raise ValueError("password must be at most 72 characters long")
        if not any(c in special_characters for c in v):
            raise ValueError("password must contain at least one special character")
        return v