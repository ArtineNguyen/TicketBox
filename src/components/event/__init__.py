from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from src import *


event_blueprint = Blueprint('event', __name__, template_folder='../../templates')

## 'host/event/'
@event_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
  if request.methods == 'POST':
      new_event = Event(body=request.form['body'],
                      user_id=current_user.id)
      db.session.add(new_post)
      db.session.commit()
      return redirect(url_for('root'))
  user = User.query.get(2)
  return "here id event"
