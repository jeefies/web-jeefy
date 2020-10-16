from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
#from config import config
import config as cf
config = cf.config

bootstrap = Bootstrap()
#mail = Mail()
moment = Moment()
#db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    #print(config_name)
    #input()
    conf = config[config_name]
    #conf = config['default']
    app.config.from_object(conf)
    conf.init_app(app)

    bootstrap.init_app(app)
    #mail.init_app(app)
    moment.init_app(app)
    #db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .cookie import cookie as cookie_blueprint
    app.register_blueprint(cookie_blueprint, url_prefix='/cook')

    from .study import study as study_blueprint
    app.register_blueprint(study_blueprint, url_prefix='/study')

    return app

