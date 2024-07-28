import os
from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail, Message

load_dotenv()

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv("DEFAULT_EMAIL") 
app.config['MAIL_PASSWORD'] = os.getenv("DEFAULT_APP_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.route("/")
def index():
    msg = Message(
        subject='Hello from the other side!', 
        sender='bhinnexclusive@gmail.com',  
        recipients=['qeja.ke@gmail.com']  
    )
    msg.body = "Hey, sending you this email from my Flask app, let me know if it works."
    msg.html = f"""
            <html>
                <body>
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
                        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; border: 1px solid #e9ecef;">
                            <h2 style="color: #343a40;">Welcome to Qeja!</h2>
                            <p>Dear guy,</p>
                            <p>Thank you for registering with Qeja. To complete your registration, please use the following activation code:</p>
                            <p style="font-size: 20px; font-weight: bold;">1234</p>
                            <p>If you did not request this registration, please ignore this email.</p>
                            <p>Best regards,</p>
                            <p>The Qeja Team</p>
                        </div>
                        <div style="text-align: center; margin-top: 20px; color: #6c757d; font-size: 12px;">
                            <p>&copy; 2024 Qeja, Inc. All rights reserved.</p>
                            <p>Qeja Inc., 1234 Housing Lane, Suite 100, City, State, 12345</p>
                        </div>
                    </div>
                </body>
            </html>
            """
    mail.send(msg)
    return "Message sent!"

if __name__ == '__main__':
    app.run(debug=True)