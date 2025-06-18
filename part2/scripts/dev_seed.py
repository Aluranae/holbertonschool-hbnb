from app.models.user import User
from app.services import facade

# Création d’un utilisateur test
user = User(first_name="Leia", last_name="Organa", email="leia@rebellion.org")

# Ajout dans le repo mémoire partagé
facade.user_repo.add(user)

print("User created with ID:", user.id)
