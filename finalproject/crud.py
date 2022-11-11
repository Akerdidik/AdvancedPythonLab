from models.models import User,db

def add_user(user:User) -> None:
    db.session.add(user)
    db.session.commit()

