
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class MyAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    # def inaccessible_callback(self, name, **kwargs):
    #     # redirect to login page if user doesn't have access
    #     return redirect(url_for('userbp.login', next=request.url))