from app import app
from lib import db, Property

with app.app_context():
    print("Deleting properties...")
    Property.query.delete()
    db.session.commit()
    print("Properties Deleted successfully")