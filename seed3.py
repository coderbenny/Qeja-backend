from faker import Faker
from datetime import datetime
from app import app
from lib import db, User, Post

# Ensure that the app context is properly used
with app.app_context():
    faker = Faker()
    
    # Clear the Post table
    db.session.query(Post).delete()
    db.session.commit()

    # Assume we already have users in the database. Fetch user IDs dynamically.
    users = User.query.with_entities(User.id).all()
    user_ids = [user.id for user in users]

    if not user_ids:
        print("No users found in the database. Please seed users first.")
    else:
        print("Seeding posts...")
        for user_id in user_ids:
            new_post = Post(
                user_id=user_id,
                body=faker.text(),
                img1=faker.image_url(),
                img2=faker.image_url(),
                img3=faker.image_url(),
                created_at=datetime.now()  # Ensure created_at is a datetime object
            )
            db.session.add(new_post)
        
        db.session.commit()
        print("Seeding posts complete.")
