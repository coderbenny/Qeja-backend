from flask_mail import Mail
from app import app

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv("DEFAULT_EMAIL")
app.config['MAIL_PASSWORD'] = os.getenv("DEFAULT_EMAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)