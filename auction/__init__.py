#import flask - from the package import class
from flask import Flask 
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import sys

db=SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app=Flask(__name__,static_url_path='')  # this is the name of the module/package that is calling this app
    app.debug=True
    app.secret_key='utroutoru'
    #set the app configuration data 
    # app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///marketplace.sqlite'
    WIN = sys.platform.startswith('win')
    if WIN:
        prefix = 'sqlite:///'
    else:
        prefix = 'sqlite:////'
    dev_db = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
    app.config['SQLALCHEMY_DATABASE_URI']=dev_db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
    #initialize db with flask app
    db.init_app(app)

    bootstrap = Bootstrap(app)
    
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.authenticate'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))

    #importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)
    
    return app



