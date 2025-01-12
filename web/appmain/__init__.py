from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = "f45e55e904ebe239ee03bb3f8582302c"

from appmain.routes import main
app.register_blueprint(main)

from appmain.user.routes import user
app.register_blueprint(user)