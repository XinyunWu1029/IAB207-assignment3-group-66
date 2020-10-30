from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required,logout_user
from . import db


#create a blueprint
bp = Blueprint('auth', __name__)


# this is the hint for a login function
@bp.route('/login', methods=['GET', 'POST'])
def authenticate(): #view function
    print('In Login View function')
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(username=user_name).first()
        if u1 is None:
            error='Incorrect user name'
        elif not check_password_hash(u1.password, password): # takes the hash and password
            error='Incorrect password'
        if error is None:
            login_user(u1)
            nextp = request.args.get('next') #this gives the url from where the login page was accessed
            print(nextp)
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login',title='Login')

@bp.route('/register', methods=['GET', 'POST'])
def authenticatebyregister(): #view function
    print('In Register View function')
    register_form = RegisterForm()
    error=None
    if(register_form.validate_on_submit()==True):
        user_name = register_form.user_name.data
        email_id = register_form.email_id.data
        password = register_form.password.data
        confirm = register_form.confirm.data
        u1 = User.query.filter_by(username=user_name).first()
        if not u1 is None:
            error='exist user name'
        if error is None:
            u2=User(user_name,generate_password_hash(password),email_id)
            u2.savebyadd()
            return redirect(url_for('auth.authenticate'))
        else:
            flash(error)
    return render_template('user.html', form=register_form, heading='Register',title='Register')