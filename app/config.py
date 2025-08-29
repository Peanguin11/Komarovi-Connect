from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///komarovi.db'
app.config['SECRET_KEY'] = '5792318bb0b13ce0c67dfde280ba245'
db = SQLAlchemy(app)
migrate = Migrate(app,db)


UPLOAD_FOLDER = "static"

app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER


# login_manager = LoginManager(app)
# login_manager.login_view = 'adminlogin'