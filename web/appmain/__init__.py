import os

from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.config["SECRET_KEY"] = "f45e55e904ebe239ee03bb3f8582302c"

app.config["MAIL_SERVER"] = os.getenv('MAIL_SERVER')
app.config["MAIL_PORT"] = int(os.getenv('MAIL_PORT', 587))
app.config["MAIL_USE_TLS"] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config["MAIL_USERNAME"] = os.getenv('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

from appmain.routes import main
app.register_blueprint(main)

from appmain.user.routes import user
app.register_blueprint(user)

from appmain.article.routes import article
app.register_blueprint(article)