from database import create_tables
create_tables()

from auth import register_user, login_user

result = register_user(
    email="vault_test3@example.com",
    password="StrongPass2!",
    name="Test User"
)
print("REGISTER RESULT:")
print(result)

print()

login_result = login_user(
    email="vault_test3@example.com",
    password="StrongPass2!"
)
print("LOGIN RESULT:")
print(login_result)