from app.models.user import User
from app.services import facade

user = User(first_name="Leia", last_name="Organa", email="leia@rebellion.org")
facade.user_repo.add(user)

print("User created with ID:", user.id)
