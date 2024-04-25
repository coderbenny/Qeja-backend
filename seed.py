import os, random
from faker import Faker

from app import app
from lib.models import db, User, Profile, Role, Message, Property

faker = Faker()

with app.app_context():
    
    print("seeding users...")
    
    users = [
        User(
                name=faker.name(), 
                email=faker.email(), 
                password=faker.password(length=5),
                role_id=random.randint(1, 3)
            ) for i in range(6)
    ]
    
    db.session.add_all(users)
    db.session.commit()
    
    print("seeding users complete")
    
    
    
    
    
    
    
    
    
    
    # Role.query.delete()
    
    # roles = ["owner", "tenant", "roomie hunter"]
    
    # print("seeding roles...")
    # for a in roles:
    #     role = Role(title=a)
    #     db.session.add(role)
    # db.session.commit()
    
    # print("seeding roles complete.")
    
    
    