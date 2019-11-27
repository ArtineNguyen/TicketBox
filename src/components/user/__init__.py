from flask import Flask, Blueprint, render_template, request, redirect, url_for, abort
from flask_login import current_user, logout_user
from src.models.user import User
from src import app, db
from itsdangerous import URLSafeTimedSerializer

user_blueprint = Blueprint('userbp', __name__, template_folder='../../templates')

def send_mail(token,email,name):
  url = "https://api.mailgun.net/v3/sandbox3e7cd47c8c6945d6b25f3c298c6ba368.mailgun.org/messages"
  try:
    response = requests.post(url, 
      auth=("api", app.config['EMAIL_API']), 
      data={"from": 'Artine Nguyen <artinenguyen@gmail.com>',
      "to": [self.email], 
      "subject": "Reset Password", 
      "text":f"Go to http://localhost:5000/user/new_password/{token}."}
      )
    response.raise_for_status()
  except HTTPError as http_err:
      print(f'HTTP error occurred: {http_err}')  # Python 3.6
  except Exception as err:
      print(f'Other error occurred: {err}')  # Python 3.6
  else:
      print('Success!')

## 'host/user/'
@user_blueprint.route('/user')
def root_user():
  return render_template('user/index.html')

@user_blueprint.route('/register')
def register():
  return render_template('user/index.html')

@user_blueprint.route('/login')
def login():
  return render_template('login.html')

@user_blueprint.route('/forget-password', methods=['POST','GET'])
def forget():
  if current_user.is_authenticated:
    return redirect(url_for('userbp.root'))
  if request.method == "POST":
    user = User(email=request.form['email']).check_user()
    if not user:
      print("Account does not exist")
      return redirect(url_for('userbp.forget'))
      s = URLSafeSerializer(app.secre_key)
      token = s.dumps(user.email, salt="RESET_PASSWORD")
      send_mail(token,user.email,user.name)
      print('OK')
      return redirect(url_for('userbp.login'))
  return render_template('forget.html')

@user_blueprint.route('/reset', methods=["GET", "POST"])
def reset():
  form = EmailForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first_or_404()
    # Redirect to the main login form here with a "password reset email sent!"
  return render_template('user/reset.html', form=form)

@user_blueprint.route('/new_password/<token>', methods=['POST', 'GET'])
def new_password(token):
    print(token)
    s = URLSafeSerializer(app.secre_key)
    email = s.loads(token, salt="RESET_PASSWORD", max_age=300)
    print(email)
    user = User(email=email).check_user()
    if not user:
      print('INVALID TOKEN')
      return redirect(url_for('root'))
    if request.method == 'POST':
      if request.form['password'] != request.form['comfirm']:
        print('passwords not match')
        return redirect(url_for('userbp.newpassword', token=token))
        user.set_password(request.form['password'])
        return redirect(url_for('root'))
    return render_template('user/new_password.html')
