from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
import os

# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import FileStorage


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SECRET KEY'] = 'kjdakjdsdlk4324k55kssdasda'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir,'static/images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
# patch_request_class(app)        # 16 megabytes

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
db.init_app(app)

from shop.admin import routes
from shop.products import routes