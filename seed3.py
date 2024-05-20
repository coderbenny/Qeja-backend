from faker import Faker
from app import app
from lib import db, User, Post

with app.app_context():
    faker = Faker()

    posts = [
        {
            "user_id": 1,
            "body": faker.text(),
            "img1": faker.image_url(),
            "img2": faker.image_url(),
            "img3": faker.image_url(),
        },
        {
            "user_id": 1,
            "body": faker.text(),
            "img1": faker.image_url(),
            "img2": faker.image_url(),
            "img3": faker.image_url(),
        }
    ]

    print("Seeding posts...")
    for post in posts:
        new_post = Post(**post)
        db.session.add(new_post)
    db.session.commit()
    print("Seeding posts complete.")
