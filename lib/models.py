from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

# join table for followers/following
followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.UniqueConstraint('follower_id', 'followed_id', name='unique_follow_pair')
)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
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

    followers = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('following', lazy='dynamic'), lazy='dynamic'
    )
    
    # One-to-One relationship with Role
    role = db.relationship("Role")
    
    serialize_rules = ("-profile.user","-properties.user","-sent_messages.sender","-received_messages.receiver","-role.Role")

    def __repr__(self):
        return f'<User {self.name}>'
    
    def to_dict(self, view_property=False):
        if view_property:
            return {
                "id": self.id,
                "name": self.name,
                "profile":self.profile.to_dict(),
                "followers":self.follower_count,
                "following":self.following_count,
                "email":self.email,
                "properties": [p.to_dict() for p in self.properties],
                "sent_messages":[m.to_dict() for m in self.sent_messages],
                "received_messages":[m.to_dict() for m in self.received_messages],
            }
        return {
            "id": self.id,
            "name": self.name,
            "email":self.email,
            "profile":self.profile.to_dict(),
            "role_id":self.role_id,
            "followers":self.follower_count,
            "following":self.following_count,
            "sent_messages":[m.to_dict() for m in self.sent_messages],
            "received_messages":[m.to_dict() for m in self.received_messages],
        }
        
    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(followers.c.followed_id == user.id).count() > 0
    
    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()


class Profile(db.Model, SerializerMixin):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer)
    bio = db.Column(db.String)
    location = db.Column(db.String(100))
    profile_pic = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # One-to-One relationship with User
    user = db.relationship("User", back_populates="profile")
    
    serialize_rules = ("-user.profile",)

    def __repr__(self):
        return f'<Profile {self.user_id}, {self.location}>'
    
    def to_dict(self):
        return{
            "id":self.id,
            "role_id":self.role_id,
            "bio":self.bio,
            "location":self.location,
            "profile_pic":self.profile_pic,
            "user_id":self.user_id,
        }

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

    def __repr__(self):
        return f'<Message {self.sender_id}, {self.receiver_id}>'
    
    def to_dict(self, view_receiver=False):
        if view_receiver:
            return {
                "id": self.id,
                "sender": self.sender.name, 
                "receiver": self.receiver.name, 
                "content": self.content 
            }
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "content": self.content
        }
        
class Post(db.Model, SerializerMixin):
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    body = db.Column(db.String, nullable=False)
    img1 = db.Column(db.String)
    img2 = db.Column(db.String)
    img3 = db.Column(db.String)


    def __repr__(self):
        return f'<Post {self.id} {self.body}>'
    
    