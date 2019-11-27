from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from src.models.user import User

root_bp = Blueprint('root_bp', __name__, template_folder='../../templates')

## 'host/event/'
@root_bp.route('/')
# @login_required
def root():
    return render_template('home.html')

# @root_bp.route('/logout')
# # @login_required
# def logout():
#   return render_template('home.html')

@root_bp.route('/login')
# @login_required
def login():
      if request.method == 'POST':
          user = User.query.filter_by(email=request.form['email']).first()
          if not user:
              flash('Email is not registered', 'warning')
              return redirect(url_for('register'))
          if user.check_password(request.form['password']):
              login_user(user)
              flash(f'Welcome back {current_user.name}!', 'success')
              return redirect(url_for('root'))
          flash('wrong password or email', 'warning')
          return redirect(url_for('login'))
          if current_user.is_authenticated:
              return redirect(url_for('root'))
      return render_template('login.html')

@root_bp.route('/register')
# @register_required
def register():
      if request.method == 'POST':
        check_email = User.query.filter_by(email=request.form['email']).first()
        if check_email:  # if email taken
            flash('Email already taken', 'warning')  # we alert the user
            # then reload the register page again
            return redirect(url_for('register'))
        # if email not taken, we add new user to the database
        # we start with create an object for new_user
        new_user = User(name=request.form['name'],
                        email=request.form['email'])
        # raw password will be hashed using the generate_password method
        new_user.generate_password(request.form['password'])
        db.session.add(new_user)  # then we add new user to our session
        db.session.commit()  # then we commit to our database (kind of like save to db)
        login_user(new_user)  # then we log this user into our system
        flash('Successfully create an account and logged in', 'success')
        return redirect(url_for('root'))  # and redirect user to our root
        if current_user.is_authenticated:
            return redirect(url_for('root'))
        return render_template('templates/register.html')

@root_bp.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
      user = User.query.filter_by(email=form.email.data).first_or_404()
      # Redirect to the main login form here with a "password reset email sent!"
    return render_template('reset.html', form=form)

# @root_bp.route('/forgetpassword')
# def forgetpassword():
#   return "Here is root index"
