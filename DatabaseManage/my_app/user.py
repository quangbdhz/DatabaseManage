from flask import flash, Response
from my_app.models import UserCreateDatabase
from flask_admin import AdminIndexView, expose, Admin, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from my_app.common import *
from my_app.utils import *
from urllib.parse import unquote

class MyUserIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user:
            flash('Please log in first...', category='danger')
            return redirect(url_for('login_account'))
        databaseOfUser = get_all_database(current_user.UserName)

        self._template_args["my_database"] = databaseOfUser
        self._template_args["countDatabase"] = len(databaseOfUser)

        return super(MyUserIndexView, self).index()


# class UserDatabaseManageView(ModelView):
#     create_template = 'admin/create-database.html'
#
#
# class UserDatabaseManageView_User(ModelView):
#     @expose('/user/database')
#     def index(self):
#         return super(UserDatabaseManageView, self).index_view()

class UserManageDatabaseView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/create-database.html')


class SubmitUserCreateDatabase(BaseView):
    @expose('/', methods=["POST"])
    def index(self):
        if request.method == "POST":
            getNamDatabase = ""
            if request.method == "POST":
                getNamDatabase = (current_user.UserName + "_" + request.form.get('nameDatabase'))

                url = "https://sqs.us-east-1.amazonaws.com/126581837666/testQueue"
                headers = {"Content-Type": "application/x-www-form-urlencoded"}

                payload = {
                    "name_database": getNamDatabase
                }
                payload = quote(str(payload))
                params = {
                    'Action': 'SendMessage',
                    'MessageBody': payload
                }
                send = requests.post(url, headers=headers, params=params)
            return redirect(url_for('_user.index'))
        return redirect(url_for('_createDatabase.index'))


class UserManageTableView(BaseView):
    @expose('/')
    def index(self):
        databaseOfUser = get_all_database(current_user.UserName)
        dataDatatype = get_all_datatype()
        self._template_args["my_database"] = databaseOfUser
        self._template_args["datatype"] = dataDatatype
        return self.render('admin/create-table.html')


class SubmitUserManageTableView(BaseView):
    @expose('/', methods=["POST"])
    def index(self):
        i = 1
        full_query = "("
        while request.form.get('nameColumnTable' + str(i)) != "" and request.form.get(
                'nameColumnTable' + str(i)) is not None:
            query = ""
            query += request.form.get('nameColumnTable' + str(i)) + " "
            query += request.form.get('chooseTypeColumn' + str(i))
            if request.form.get('PK' + str(i)) == "PK":
                query += " PRIMARY KEY"
            if request.form.get('NN' + str(i)) == "NN":
                query += " NOT NULL"
            if request.form.get('UQ' + str(i)) == "UQ":
                query += " UNIQUE"
            if request.form.get('nameColumnTable' + str(i + 1)) != "" and request.form.get(
                    'nameColumnTable' + str(i + 1)) is not None:
                query += ","
            full_query += query
            i = i + 1
        full_query += ");"
        getNameDatabase = (current_user.UserName + "_" + request.form.get('choose_database'))
        getNameTable = request.form.get('nameTable')

        if request.method == "POST":
            url = "https://sqs.us-east-1.amazonaws.com/126581837666/QueueCreateTableDatabase"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            payload = {
                "name_database": getNameDatabase,
                "name_table": getNameTable,
                "query": full_query,
            }
            payload = quote(str(payload))
            params = {
                'Action': 'SendMessage',
                'MessageBody': payload
            }
            send = requests.post(url, headers=headers, params=params)
        return redirect(url_for('_createDatabase.index'))


class DetailDatabaseView(ModelView):
    list_template = 'admin/detail-database.html'

    @expose('/detail-database')
    def details(self):
        name = False if request.args.get('name') is None else request.args.get('name')
        userName = current_user.UserName + '_' + name
        getAllTable = get_all_table_of_database(userName)
        self._template_args["nameDatabase"] = name
        self._template_args["data"] = getAllTable
        return super(DetailDatabaseView, self).index_view()


class DetailTableView(ModelView):
    list_template = 'admin/detail-table.html'

    @expose('/detail-table')
    def details(self):
        name = False if request.args.get('name') is None else request.args.get('name')

        name_database = (current_user.UserName + "_" + GetDatabase(name))
        name_table = GetTable(name)

        column = GetAllColumnOfTable(name_database, name_table)
        dataTable = GetAllDataOfTableInDatabase(name_database, name_table)
        countRow = CountRowTable(name_database, name_table)

        UpdateInfoAddRowDatabase(name_database, name_table)

        self._template_args["name"] = name_database
        self._template_args["table"] = name_table
        self._template_args["column"] = column
        self._template_args["countRow"] = 0
        self._template_args["countColumn"] = len(column)
        self._template_args["dataTable"] = dataTable
        self._template_args["index"] = len(dataTable)
        self._template_args["urlEdit"] = GetUrlEditTable(dataTable)
        return super(DetailTableView, self).index_view()


class AddDataTableView(BaseView):
    @expose('/', methods=["POST"])
    def index(self):
        data = GetInfoAddRowDatabase()
        name_database = data[0]
        name_table = data[1]

        column = GetAllColumnOfTable(name_database, name_table)
        info = GetAllInfoTable(name_database, name_table)
        sizeColumn = len(column)

        converColumn = "("
        for index in range(sizeColumn):
            if str(info[index][3]) == "PRI" and str(info[index][5]) == "auto_increment":
                continue
            else:
                converColumn += column[index]
            if index == sizeColumn - 1:
                converColumn += ")"
            else:
                converColumn += ", "

        listQuery = []
        i = 1
        while request.form.get(str(column[0]) + str(i)) != "" and request.form.get(str(column[0]) + str(i)) is not None:
            query = "INSERT INTO " + name_database + "." + name_table + converColumn + " VALUES ("
            for index in range(0, sizeColumn):
                if str(info[index][3]) == "PRI":
                    if str(info[index][5]) == "auto_increment":
                        continue
                    else:
                        if str(info[index][1]) == "int" or str(info[index][1]) == "float":
                            query += request.form.get(column[index] + str(i))

                        checkChar = CheckChar(str(info[index][1]), 'char')
                        if checkChar != -1:
                            query += ("$" + request.form.get(column[index] + str(i)) + "$")
                else:
                    if str(info[index][2]) == "YES":
                        value = request.form.get(column[index] + str(i))
                        if value is None or value == "":
                            query += 'NULL'
                        else:
                            if str(info[index][1]) == "int" or str(info[index][1]) == "float":
                                query += request.form.get(column[index] + str(i))

                            checkChar = CheckChar(str(info[index][1]), 'char')
                            if checkChar != -1:
                                query += ("$" + request.form.get(column[index] + str(i)) + "$")
                    else:
                        if str(info[index][1]) == "int" or str(info[index][1]) == "float":
                            query += request.form.get(column[index] + str(i))

                        checkChar = CheckChar(str(info[index][1]), 'char')
                        if checkChar != -1:
                            query += ("$" + request.form.get(column[index] + str(i)) + "$")
                if index == sizeColumn - 1:
                    query += ")"
                else:
                    query += ", "
            listQuery.append(query)
            i += 1
        SubmitAddTable(listQuery)
        # self._template_args["listQuery"] = listQuery
        # return self.render('admin/test2.html')
        # #
        return redirect(url_for('_user.index'))


class EditDataTableView(ModelView):
    list_template = 'admin/edit-data-table.html'

    @expose('/details')
    def details(self):
        data = StringHandling(str(request), 1)
        column = GetAllColumnOfTable(data[0], data[1])
        url = ConverUrl(data)
        self._template_args["dataTable"] = data
        self._template_args["size"] = len(data)
        self._template_args["column"] = column
        self._template_args["url"] = url
        return super(EditDataTableView, self).index_view()


class SubmitEditDataTable(ModelView):
    @expose('/edit', methods=["POST"])
    def details(self):
        dataTableCurrent = StringHandling(str(request), 0)
        column = GetAllColumnOfTable(dataTableCurrent[0], dataTableCurrent[1])
        infor = GetAllInfoTable(dataTableCurrent[0], dataTableCurrent[1])
        dataTableEdit = []
        for index in range(len(column)):
            value = request.form.get(column[index])
            if value == None or value == "":
                dataTableEdit.append(dataTableCurrent[index + 2])
            else:
                dataTableEdit.append(value)

        query = OuputQueryUpdateDataTable(column, dataTableCurrent, dataTableEdit, 1)
        decodeQuery = query.replace("'", "$")
        url = "https://sqs.us-east-1.amazonaws.com/126581837666/QueueEditDataTable"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "query": decodeQuery,
        }
        payload = quote(str(payload))
        params = {
            'Action': 'SendMessage',
            'MessageBody': payload
        }
        send = requests.post(url, headers=headers, params=params)
        #
        # self._template_args["dataTableEdit"] = dataTableEdit
        # self._template_args["dataColumn"] = column
        # self._template_args["dataTableCurrent"] = dataTableCurrent
        # self._template_args["info"] = infor
        # self._template_args["queryUpdate"] = query
        return redirect(url_for('_user.index'))


class SubmitDeleteDataTable(ModelView):
    list_template = 'admin/test.html'
    @expose('/delete')
    def details(self):
        dataTableCurrent = StringHandling(str(request), 1)
        column = GetAllColumnOfTable(dataTableCurrent[0], dataTableCurrent[1])

        dataTableCurrentDecode = []
        for item in range(len(dataTableCurrent)):
            if item < 2:
                dataTableCurrentDecode.append(dataTableCurrent[item])
            else:
                value = unquote(dataTableCurrent[item])
                dataTableCurrentDecode.append(value)

        dataTableEdit = []
        query = OuputQueryUpdateDataTable(column, dataTableCurrentDecode, dataTableEdit, 2)
        decodeQuery = query.replace("'", "$")
        url = "https://sqs.us-east-1.amazonaws.com/126581837666/QueueDeleteDataRowTable"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "query": decodeQuery,
        }
        payload = quote(str(payload))
        params = {
            'Action': 'SendMessage',
            'MessageBody': payload
        }
        send = requests.post(url, headers=headers, params=params)

        self._template_args["queryUpdate"] = query
        return redirect(url_for('_user.index'))

class SubmitDropTable(ModelView):
    list_template = 'admin/test.html'
    @expose('/delete')
    def details(self):
        name = False if request.args.get('name') is None else request.args.get('name')

        name_database = (current_user.UserName + "_" + GetDatabase(name))
        name_table = GetTable(name)

        query = "DROP TABLE " + name_database + "." + name_table

        SendRequest("https://sqs.us-east-1.amazonaws.com/126581837666/QueueDropTable", query)

        self._template_args["queryUpdate"] = query
        return super(SubmitDropTable, self).index_view()


userView = Admin(app, name='User', index_view=MyUserIndexView(url='/user', endpoint='_user'),
                 base_template='master.html', template_mode='bootstrap4', url='/user', endpoint='_user')
userView.add_view(UserManageDatabaseView(name="database", url='/user/databases', endpoint='_createDatabase'))
userView.add_view(
    SubmitUserCreateDatabase(name="submit_database", url='/user/databases/add', endpoint='_submitCreateDatabase'))

userView.add_view(UserManageTableView(name="table", url='/user/table', endpoint='_createTable'))
userView.add_view(SubmitUserManageTableView(name="submit_table", url='/user/table/add', endpoint='_submitCreateTable'))
userView.add_view(
    DetailDatabaseView(Users, db.session, name="detail_database", url='/user/database', endpoint='_detailDatabase'))
userView.add_view(
    DetailTableView(Users, db.session, name="detail_table", url='/user/database', endpoint='_detailTable'))
userView.add_view(AddDataTableView(name="add_data_table", url='/user/add-data-table', endpoint='_addDataTable'))
userView.add_view(EditDataTableView(Users, db.session, name="edit_data_table", url='/user/edit-data-table',
                                    endpoint='_editDataTable'))
userView.add_view(
    SubmitEditDataTable(Users, db.session, name="submit_edit_data_table", url='/user/edit-data-table/submit',
                        endpoint='_submitEditDataTable'))
userView.add_view(SubmitDeleteDataTable(Users, db.session, name="submit_delete_data_table", url='/user/delete-data-table/submit',
                                    endpoint='_deleteDataTable'))
userView.add_view(SubmitDropTable(Users, db.session, name="submit_drop_table", url='/user/drop-table/submit',
                                    endpoint='_dropTable'))