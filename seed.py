from flask import session
from faker import Faker
from lib import db
from app import app
from random import choice
from lib import Property, Role


with app.app_context():
    Property.query.delete()
    
    fake = Faker()  
    # Seed roles
    roles = ["owner", "tenant", "roommate"]
    
    print("Seeding roles...")
    for role in roles:
        new_role = Role(title=role)
        db.session.add(new_role)
    db.session.commit()
    print("Seeding roles complete")
    
    
    # Seeding property
    # Property.query.delete()
    locations = ["Nairobi", "Kisumu", "Mombasa", "Eldoret"]
    
    
    print("Seeding property...")
    for _ in range(10):
        property = Property(
            pic1=fake.image_url(),
            pic2=fake.image_url(),
            pic3=fake.image_url(),
            description=fake.text(),
            location=choice(locations),
            rent=fake.random_number(digits=5),
            wifi=fake.boolean(),
            gated=fake.boolean(),
            hot_shower=fake.boolean(),
            kitchen=fake.boolean(),
            balcony=fake.boolean(),
            parking=fake.boolean(),
            rooms=fake.random_int(min=1, max=10),
            for_rent=fake.boolean(),
            user_id=1,
        )
            
        db.session.add(property)
    print("Seeding property completed")

    db.session.commit()
