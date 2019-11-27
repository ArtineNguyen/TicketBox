from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user
from flask_admin import Admin


app = Flask(__name__)


app.secret_key = 'Secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgres://artine:12345@localhost:5432/flask-ticketbox'

db = SQLAlchemy(app)


from src.models import *
from src.models.user import User
## more models incoming
migrate = Migrate(app, db)

## set up login_manager
login_manager= LoginManager(app)
login_manager.login_view= 'userbp.login'

@login_manager.user_loader
def load_user(id):
  return User.query.get(id)


from src.components.event import event_blueprint
app.register_blueprint(event_blueprint, url_prefix='/event')

from src.components.user import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

from src.components.root import root_bp
app.register_blueprint(root_bp, url_prefix='/')

from src.models.admin import MyAdmin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name='Artine', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session)) 


from src.components.root import root_bp
app.register_blueprint(root_bp, url_prefix="/")