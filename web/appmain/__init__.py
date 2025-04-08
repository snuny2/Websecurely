from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

app.config["SECRET_KEY"] = "f45e55e904ebe239ee03bb3f8582302c"

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = ""
app.config["MAIL_PASSWORD"] = ""

mail = Mail(app)

from appmain.routes import main
app.register_blueprint(main)

from appmain.user.routes import user
app.register_blueprint(user)