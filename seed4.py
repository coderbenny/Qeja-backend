from app import app
from lib import db, User

with app.app_context():
    users = User.query.all()

    print("Changing active status...")
    for user in users:
        print(f"Changing active status for {user.name}")
        user.is_active = 1
        print(f"{user.name} now active!")
    db.session.commit()
    print("Process finished!")