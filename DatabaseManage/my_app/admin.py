from flask import flash
from flask_admin import AdminIndexView, expose, Admin
from flask_login import current_user

from my_app import routes

from my_app.common import *


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self): return super(MyAdminIndexView, self).index()


teacher = Admin(app, name='Admin', index_view=MyAdminIndexView(url='/admin', endpoint='_admin'),
                base_template='master.html', template_mode='bootstrap4', url='/admin', endpoint='_admin')
