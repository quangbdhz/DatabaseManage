from flask import flash, Response
from flask_admin import AdminIndexView, expose, Admin, BaseView
from flask_admin.contrib.sqla import ModelView
from my_app.common import *
from my_app.utils import *
from urllib.parse import unquote

class MyManageIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user:
            flash('Please log in first...', category='danger')
            return redirect(url_for('login_account'))

        return redirect(url_for('_manageUser.index'))

class ManageUserView(ModelView):
    list_template = 'manage/users.html'

    @expose('/')
    def index(self):
        users = Users.query.filter_by(IsAdmin=0, IsDelete = 0)
        self._template_args["listUsers"] = users
        return super(ManageUserView, self).index_view()

class LockUser(ModelView):
    @expose('/')
    def index(self):
        username = False if request.args.get('username') is None else request.args.get('username')

        users = Users.query.filter_by(UserName = username).first()
        if users.Active == 0:
            users.Active = 1
            db.session.commit()
        else:
            users.Active = 0
            db.session.commit()

        return redirect(url_for('_manageUser.index'))

class DeleteUser(ModelView):
    @expose('/')
    def index(self):
        username = False if request.args.get('username') is None else request.args.get('username')
        users = Users.query.filter_by(UserName = username).first()
        users.IsDelete = 1
        db.session.commit()
        return redirect(url_for('_manageUser.index'))


manageView = Admin(app, name='Manage', index_view=MyManageIndexView(url='/manage', endpoint='_manage'), base_template='master.html', template_mode='bootstrap4', url='/manage', endpoint='_manage')
manageView.add_view(ManageUserView(Users, db.session, name="user", url='/manage/user', endpoint='_manageUser'))
manageView.add_view(LockUser(Users, db.session, name="lockUser", url='/manage/user/lock', endpoint='_lockUser'))
manageView.add_view(DeleteUser(Users, db.session, name="deleteUser", url='/manage/user/delete', endpoint='_deleteUser'))

