from flask import Flask, send_from_directory, render_template, flash, redirect, url_for, Blueprint, g, request
from flask.ext.login import LoginManager, current_user, login_user, logout_user, login_required
import ldap
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired
from core.models import db, ModelType, User
from core.api import rest_api
from core import data
import settings

#Flask App
app = Flask(__name__, static_url_path='/enermod/assets')
app.config.from_object(settings)

#SQLAlchemy Initiate
db.init_app(app)

#EnerMod Rest api
app.register_blueprint(rest_api, url_prefix='/enermod/api')

#Flask Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

#Name of the view to redirect when user needs to login
login_manager.login_view = 'login'

#LoginForm Class
class LoginForm(Form):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])

@app.after_request
def adding_header_content(head):
    head.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    head.headers["Pragma"] = "no-cache"
    head.headers["Expires"] = "0"
    head.headers['Cache-Control'] = 'public, max-age=0'
    return head

@login_manager.user_loader
def load_user(id):
        return User.query.get(int(id))

@app.before_request
def get_current_user():
    g.user = current_user

@app.route('/enermod/')
@app.route('/enermod/home')
@login_required
def home():
    return render_template('home.html', owner = data.get_dist_username(), modeltype = data.get_dist_modelType(), submodels = data.get_dist_sub_models(), funclist = data.get_dist_func(), mainversionList = data.get_main_version(current_user.username))

@app.route('/enermod/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Logged in')
        return redirect(url_for('home'))

    #Custom LoginForm to validate
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        usernmae = request.form.get('username')
        password = request.form.get('password')

        try:
            conn = ldap.initialize(settings.LDAP_PROVIDER_URL)
            conn.simple_bind_s(
                'CN=%s,OU=Employees,OU=Managed Users,DC=KAPSARC,DC=ORG' % request.form.get('username'), request.form.get('password')
            )
        except ldap.INVALID_CREDENTIALS:
            flash('Invalid Username or Password', 'error')
            return render_template('login.html', form=form)
        user = User.query.filter_by(username=request.form.get('username')).first()
        if not user:
            user = User(request.form.get('username'), request.form.get('password'))
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash('Login Success', 'info')
        return redirect(url_for('home'))
    if form.errors:
        flash('Form errors', 'error')

    return render_template('login.html', form=form)

@app.route('/enermod/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/enermod/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == "__main__":
    try:
        app.run(host=settings.SERVER_HOST, port=settings.SERVER_PORT)
    except KeyboardInterrupt:
        pass