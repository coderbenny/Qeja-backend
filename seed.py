from flask import session
from faker import Faker
from lib import db
from app import app
from random import choice
from lib import Property, Role, Post, Profile


with app.app_context():
    # Property.query.delete()
    
    fake = Faker()  
    # Seed roles
    # roles = ["owner", "tenant", "roommate"]
    
    # print("Seeding roles...")
    # for role in roles:
    #     new_role = Role(title=role)
    #     db.session.add(new_role)
    # db.session.commit()
    # print("Seeding roles complete")
    
    
    # Seeding property
    # Property.query.delete()
    # locations = ["Nairobi", "Kisumu", "Mombasa", "Eldoret"]
    
    
    # print("Seeding property...")
    # for _ in range(10):
    #     property = Property(
    #         pic1=fake.image_url(),
    #         pic2=fake.image_url(),
    #         pic3=fake.image_url(),
    #         description=fake.text(),
    #         location=choice(locations),
    #         rent=fake.random_number(digits=5),
    #         wifi=fake.boolean(),
    #         gated=fake.boolean(),
    #         hot_shower=fake.boolean(),
    #         kitchen=fake.boolean(),
    #         balcony=fake.boolean(),
    #         parking=fake.boolean(),
    #         rooms=fake.random_int(min=1, max=10),
    #         for_rent=fake.boolean(),
    #         user_id=1,
    #     )
            
    #     db.session.add(property)
    # print("Seeding property completed")
    
    # print("Seeding posts...")
    # posts_data = [
    # {"user_id": 1, "body": "Sample post 1"},
    # {"user_id": 2, "body": "Sample post 2"},
    # {"user_id": 1, "body": "Sample post 3"},
    # ]

    # for post_data in posts_data:
    #     post = Post(**post_data)
    #     db.session.add(post)

    # db.session.commit()

    # Create sample images for each post
    # images_data = [
    #     {"post_id": 1, "link": "https://example.com/image1.jpg"},
    #     {"post_id": 1, "link": "https://example.com/image2.jpg"},
    #     {"post_id": 2, "link": "https://example.com/image3.jpg"},
    #     {"post_id": 3, "link": "https://example.com/image4.jpg"},
    # ]

    # for image_data in images_data:
    #     image = Image(**image_data)
    #     db.session.add(image)

    # db.session.commit()

    # print("Seed data inserted successfully.")
    # db.session.commit()
    
    
    # print("Seeding posts complete.")
    
    print("Seeding profiles...")
    profiles = [
        {"role_id":1, "bio":"I love manchester united","followers":0,"following":0,"user_id":1,"location":"Nairobi", "profile_pic":"https://www.placeholder.com/image"},
        {"role_id":3, "bio":"I am nice in person","followers":0,"following":0,"user_id":2,"location":"Kisumu", "profile_pic":"https://www.placeholder.com/image"},
        {"role_id":1, "bio":"I am the administrator","followers":0,"following":0,"user_id":3,"location":"Wendani", "profile_pic":"https://www.placeholder.com/image"},
    ]
    for profile_data in profiles:
        profile = Profile(**profile_data)
        db.session.add(profile)

    db.session.commit()

    print("Seed data inserted successfully.")
