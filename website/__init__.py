from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from os import path, getenv
from flask_admin import Admin
from flask_migrate import Migrate
from .config import Config, StagingConfig, DevelopmentConfig


# app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
admin = Admin()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    env_config = getenv("APP_SETTINGS", "DevelopmentConfig")
    if env_config == 'Config':
        env_config = Config
    elif env_config == 'StagingConfig':
        env_config = StagingConfig
    else:
        env_config = DevelopmentConfig
    print(env_config)
    app.config.from_object(env_config)
    # app.config['SECRET_KEY'] = "adlfakdjf1;adklfjaj38 dak"
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    migrate.init_app(app, db)
    db.init_app(app)
    admin.init_app(app)


    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User


    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app



# if __name__ == '__main__':
#     app.run(debug=True) 

def create_database(app):
    db.create_all(app=app)
    print('Created Database!')