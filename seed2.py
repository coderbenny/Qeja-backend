from faker import Faker
from random import choice
from app import app
from lib import db, Property, Role, User

# Create Faker instance
fake = Faker()

with app.app_context():
    # Seed roles
    roles = ["owner", "tenant", "roommate"]

    print("Seeding roles...")
    for role_title in roles:
        role = Role.query.filter_by(title=role_title).first()
        if not role:
            role = Role(title=role_title)
            db.session.add(role)
    db.session.commit()
    print("Seeding roles complete")

    # Seed users
    print("Seeding users...")
    users = [
        {"name": "admin", "email": "admin@admin.com", "role_id": 1, "password": "admin123"},
        {"name": "benny", "email": "benny@benny.com", "role_id": 1, "password": "benny123"},
        {"name": "james", "email": "james@james.com", "role_id": 2, "password": "james123"},
        {"name": "sam", "email": "sam@sam.com", "role_id": 2, "password": "sam123"},
        {"name": "john", "email": "john@john.com", "role_id": 3, "password": "john123"},
        {"name": "kent", "email": "kent@kent.com", "role_id": 3, "password": "kent123"},
        {"name": "winnie", "email": "winnie@winnie.com", "role_id": 3, "password": "winnie123"},
        {"name": "kim", "email": "kim@kim.com", "role_id": 3, "password": "kim123"},
    ]

    for user_data in users:
        user = User.query.filter_by(email=user_data["email"]).first()
        if not user:
            user = User(name=user_data["name"], email=user_data["email"], password=user_data["password"], role_id=user_data["role_id"])
            db.session.add(user)
    db.session.commit()
    print("Seeding users complete")

    # Seed properties
    print("Seeding properties...")
    locations = ["Nairobi", "Kisumu", "Mombasa", "Eldoret"]

    for _ in range(10):
        property_data = {
            "pic1": fake.image_url(),
            "pic2": fake.image_url(),
            "pic3": fake.image_url(),
            "description": fake.text(),
            "location": choice(locations),
            "rent": fake.random_number(digits=5),
            "wifi": fake.boolean(),
            "gated": fake.boolean(),
            "hot_shower": fake.boolean(),
            "kitchen": fake.boolean(),
            "balcony": fake.boolean(),
            "parking": fake.boolean(),
            "rooms": fake.random_int(min=1, max=10),
            "for_rent": fake.boolean(),
            "user_id": 1,  # Assigning to user with id 1 for example purposes
        }
        property = Property(**property_data)
        db.session.add(property)
    db.session.commit()
    print("Seeding properties complete")
