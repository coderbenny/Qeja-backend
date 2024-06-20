from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'))
)

likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('property_id', db.Integer, db.ForeignKey('properties.id'))
)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String(100))
    password = db.Column(db.String)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # One-to-One relationship with Profile
    profile = db.relationship("Profile", uselist=False, back_populates="user")

    # One-to-Many relationship with Properties
    properties = db.relationship("Property", back_populates="user")

    # One-to-Many relationship with Messages as sender
    sent_messages = db.relationship("Message", foreign_keys="[Message.sender_id]", back_populates="sender")

    # One-to-Many relationship with Messages as receiver
    received_messages = db.relationship("Message", foreign_keys="[Message.receiver_id]", back_populates="receiver")

    # One-to-One relationship with Role
    role = db.relationship("Role")
    
    # Many-to-Many relationship with Property through Like
    liked_properties = db.relationship('Property', secondary=likes, back_populates='likers')

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            db.session.commit()  # Ensure the relationship is committed

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            db.session.commit()  # Ensure the relationship is committed

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.timestamp.desc())

    @property
    def followed_count(self):
        return self.followed.count()

    @property
    def followers_count(self):
        return self.followers.count()
    
    def __repr__(self):
        return f'<User {self.name}>'
    
    def to_dict(self, view_property=False):
        if view_property:
            return {
                "id": self.id,
                "name": self.name,
                "email": self.email,
                "properties": [p.to_dict() for p in self.properties],
                "sent_messages": [m.to_dict() for m in self.sent_messages],
                "received_messages": [m.to_dict() for m in self.received_messages],
                "profile": self.profile.to_dict() if self.profile else None,
                "role_id": self.role_id,
                "followed": [user.id for user in self.followed],
                "followers": [user.id for user in self.followers],
            }
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "profile": self.profile,
            "role_id": self.role_id,
            "sent_messages": [m.to_dict() for m in self.sent_messages],
            "received_messages": [m.to_dict() for m in self.received_messages],
            "followed": [user.id for user in self.followed],
            "followers": [user.id for user in self.followers],
        }

    def like_property(self, property):
        if not self.has_liked_property(property):
            self.liked_properties.append(property)
            db.session.commit()
    
    def unlike_property(self, property):
        if self.has_liked_property(property):
            self.liked_properties.remove(property)
            db.session.commit()
    
    def has_liked_property(self, property):
        return self.liked_properties.filter(
            likes.c.property_id == property.id).count() > 0

class Profile(db.Model, SerializerMixin):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String)
    followers = db.Column(db.Integer)
    following = db.Column(db.Integer)
    location = db.Column(db.String(100))
    profile_pic = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # One-to-One relationship with User
    user = db.relationship("User", back_populates="profile")
    
    serialize_rules = ("-user.profile",)

    def to_dict(self):
        return{
            "id":self.id,
            "bio":self.bio,
            "followers":self.followers,
            "following":self.following,
            "location":self.location,
            "profile_pic":self.profile_pic,
            "user_id":self.user_id,
            "name":self.user.name,
        }

    def __repr__(self):
        return f'<Profile {self.user_id}, {self.role_id}>'

class Role(db.Model, SerializerMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def __repr__(self):
        return f'<Role {self.title}>'

class Property(db.Model, SerializerMixin):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    pic1 = db.Column(db.String)
    pic2 = db.Column(db.String)
    pic3 = db.Column(db.String)
    description = db.Column(db.String)
    location = db.Column(db.String)
    rent = db.Column(db.String)
    wifi = db.Column(db.Boolean)
    gated = db.Column(db.Boolean)
    hot_shower = db.Column(db.Boolean)
    kitchen = db.Column(db.Boolean)
    balcony = db.Column(db.Boolean)
    parking = db.Column(db.Boolean)
    rooms = db.Column(db.Integer, default=0)
    for_rent = db.Column(db.Boolean)
    available = db.Column(db.Boolean)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship('User', back_populates="properties")
    likers = db.relationship('User', secondary=likes, back_populates='liked_properties')

    serialize_rules = ("-user.properties",)

    def __repr__(self):
        return f'<Property {self.rent}, {self.location}>'
    
    def to_dict(self, view_owner=False):
        if view_owner:
            return{
                "id": self.id, 
                "pic1": self.pic1, 
                "pic2": self.pic2, 
                "pic3": self.pic3, 
                "description": self.description, 
                "rent": self.rent, 
                "location": self.location, 
                "wifi": self.wifi,
                "gated": self.gated,
                "hot_shower": self.hot_shower,
                "kitchen": self.kitchen,
                "balcony": self.balcony,
                "parking": self.parking,
                "rooms": self.rooms,
                "for_rent": self.for_rent,
                "available": self.available,
                "owner": self.user.name
            }
        return{
            "id": self.id, 
            "pic1": self.pic1, 
            "pic2": self.pic2, 
            "pic3": self.pic3, 
            "description": self.description, 
            "rent": self.rent, 
            "rooms": self.rooms,
            "location": self.location, 
            "wifi": self.wifi,
            "gated": self.gated,
            "hot_shower": self.hot_shower,
            "kitchen": self.kitchen,
            "balcony": self.balcony,
            "parking": self.parking, 
            "for_rent": self.for_rent, 
            "available": self.available,
            "owner_id": self.user_id
        }

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String)
    timestamp = db.Column(db.DateTime)

    # Many-to-One relationship with User (sender)
    sender = db.relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    
    # Many-to-One relationship with User (receiver)
    receiver = db.relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")

    serialize_rules = ("-receiver.received_messages", "-sender.sent_messages")

