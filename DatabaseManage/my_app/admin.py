import time

from flask import flash, Response
from flask_admin import AdminIndexView, expose, Admin, BaseView
from flask_admin.contrib.sqla import ModelView
from my_app.common import *
from my_app.models import UserCreateDatabase
from my_app.utils import *
from urllib.parse import unquote, quote

class MyUserIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user:
            flash('Please log in first...', category='danger')
            return redirect(url_for('login_account'))
        userCreateDatabase = UserCreateDatabase.query.filter_by(IdUserCreate = current_user.Id)
        self._template_args["userCreateDatabase"] = userCreateDatabase
        return super(MyUserIndexView, self).index()

class UserProfileView(BaseView):
    @expose('/', methods=["POST","GET"])
    def index(self):
        user = Users.query.filter_by(Id = current_user.Id, IsDelete = 0, Active = 1).first()
        if request.method == "POST":
            fullName = request.form.get('full_name')
            phone = request.form.get('phone')
            if fullName == "":
                pass
            else:
                user.FullName = fullName
            if phone == "":
                pass
            else:
                user.Phone = phone
            db.session.commit()
            return redirect(url_for('_userProfile.index'))
        self._template_args["user"] = user
        return self.render('admin/profile.html')

class UserManageDatabaseView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/database/create-database.html')


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

                userCreateDatabase = UserCreateDatabase()
                userCreateDatabase.Active = 1
                userCreateDatabase.Name = request.form.get('nameDatabase')
                userCreateDatabase.IdUserCreate = current_user.Id
                db.session.add(userCreateDatabase)
                db.session.commit()
            return redirect(url_for('_user.index'))
        return redirect(url_for('_createDatabase.index'))


class UserManageTableView(BaseView):
    @expose('/')
    def index(self):
        databaseOfUser = get_all_database(current_user.UserName)
        dataDatatype = get_all_datatype()
        self._template_args["my_database"] = databaseOfUser
        self._template_args["datatype"] = dataDatatype
        return self.render('admin/table/create-table.html')

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
        return redirect(url_for('_createTable.index'))

class DetailDatabaseView(ModelView):
    list_template = 'admin/database/detail-database.html'

    @expose('/detail-database')
    def details(self):
        name = False if request.args.get('name') is None else request.args.get('name')
        userName = current_user.UserName + '_' + name
        getAllTable = get_all_table_of_database(userName)
        self._template_args["nameDatabase"] = name
        self._template_args["data"] = getAllTable
        return super(DetailDatabaseView, self).index_view()

class DetailTableView(ModelView):
    list_template = 'admin/table/detail-table.html'

    @expose('/detail-table')
    def details(self):
        name = False if request.args.get('name') is None else request.args.get('name')
        name_database = (current_user.UserName + "_" + GetDatabase(name))
        name_table = GetTable(name)
        column = GetAllColumnOfTable(name_database, name_table)
        dataTable = GetAllDataOfTableInDatabase(name_database, name_table)
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

class DetailDataTableView(ModelView):
    list_template = 'admin/table/detail-data-table.html'

    @expose('/data-table')
    def details(self):
        data = StringHandling(str(request), 1)
        name_database = current_user.UserName + "_" + data[0]
        name_table = data[1].replace("' [", "")

        allDataTable = GetAllDataOfTableInDatabase(name_database, name_table)
        nameColumn = GetAllColumnOfTable(name_database, name_table)

        self._template_args["name_database"] = data[0]
        self._template_args["name_table"] = name_table
        self._template_args["allDataTable"] = allDataTable
        self._template_args["nameColumn"] = nameColumn
        self._template_args["column"] = len(nameColumn)
        return super(DetailDataTableView, self).index_view()

class EditColumnTableView(ModelView):
    list_template = 'admin/table/edit-column-table.html'
    @expose('/edit')
    def details(self):
        data = StringHandling(str(request), 1)
        name_database = current_user.UserName + "_" + data[0]
        name_table = data[1].replace("' [", "")
        allInfoTable = GetAllInfoTable(name_database, name_table)
        datatype = get_all_datatype()
        checkPRI = 0
        for item in allInfoTable:
            if str(item[3]) == "PRI":
                checkPRI = 1

        self._template_args["allInfoTable"] = allInfoTable
        self._template_args["name_table"] = name_table
        self._template_args["name_database"] = name_database
        self._template_args["datatype"] = datatype
        self._template_args["checkPRI"] = checkPRI
        # self._template_args["typeColumnTable"] = typeColumnTable
        # self._template_args["row"] = row
        return super(EditColumnTableView, self).index_view()

class AddColumnTable(ModelView):
    @expose('/add', methods=["POST"])
    def index(self):
        i = 1
        data = StringHandling(str(request), 0)
        name_database = data[0]
        name_table = data[1].replace("' [P", "")

        listQuery = []
        while (request.form.get('nameTable' + str(i)) != "" and request.form.get('nameTable' + str(i)) is not None) or (request.form.get('chooseTypeColumn' + str(i)) != "" and request.form.get('chooseTypeColumn' + str(i)) is not None):
            query = "ALTER TABLE " + name_database + "." + name_table + " ADD COLUMN "
            query += request.form.get('nameTable' + str(i)) + " " + request.form.get('chooseTypeColumn' + str(i))
            if request.form.get('chooseNull' + str(i)) == "YES":
                pass
            else:
                query += " NOT NULL"
            if request.form.get('choosePRI' + str(i)) == "" or request.form.get('choosePRI' + str(i)) is None:
                query += ""
            else:
                query += " PRIMARY KEY"

            listQuery.append(query)
            i += 1

        for item in listQuery:
            SendRequest("https://sqs.us-east-1.amazonaws.com/126581837666/QueueAddNewColumnTable", item)

        self._template_args["full_query"] = listQuery
        self._template_args["name_database"] = name_database
        self._template_args["name_table"] = name_table
        time.sleep(5)
        return redirect(request.referrer)

class RenameColumnTableView(ModelView):
    list_template = 'admin/table/rename-column-table.html'

    @expose('/column', methods=["POST", "GET"])
    def details(self):
        getData = info(str(request), -1)
        name_database = getData[0].replace("ame=", "")
        name_table = getData[1].replace("table=", "")
        column = (getData[2].replace("column=", "")).replace("'","")

        allInfoTable = GetAllInfoTable(name_database, name_table)
        getColumn = []

        for item in allInfoTable:
            if str(item[0]) == column:
                getColumn.append(item)
                break

        if request.method == "POST":
            query = "ALTER TABLE " + name_database + "." + name_table + " RENAME COLUMN " + column + " TO " + request.form.get('newColumnName')
            SendRequest("https://sqs.us-east-1.amazonaws.com/126581837666/QueueAddNewColumnTable", query)
            return redirect(url_for('_user.index'))

        self._template_args["name_database"] = name_database
        self._template_args["name_table"] = name_table
        self._template_args["column"] = column
        self._template_args["getColumn"] = getColumn
        return super(RenameColumnTableView, self).index_view()

class SubmitDropColumnTable(ModelView):
    @expose('/column')
    def details(self):
        getData = info(str(request), -1)
        name_database = getData[0].replace("ame=", "")
        name_table = getData[1].replace("table=", "")
        column = getData[2].replace("column=", "")
        query = "ALTER TABLE " + name_database + "." + name_table + " DROP COLUMN " + column
        SendRequest("https://sqs.us-east-1.amazonaws.com/126581837666/QueueAddNewColumnTable", query)
        return redirect(request.referrer)

class AddDataTable(BaseView):
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
        # redirectUrl = request.url.replace("add/", "")
        return redirect(request.referrer)

class EditDataTableView(ModelView):
    list_template = 'admin/table/edit-data-table.html'

    @expose('/details')
    def details(self):
        data = StringHandling(str(request), 1)
        column = GetAllColumnOfTable(data[0], data[1])
        url = ConverUrl(data)

        newdata = []
        for item in data:
            newdata.append(unquote(item))

        self._template_args["dataTable"] = newdata
        self._template_args["size"] = len(data)
        self._template_args["column"] = column
        self._template_args["url"] = url
        return super(EditDataTableView, self).index_view()

class SubmitEditDataTable(ModelView):
    @expose('/edit', methods=["POST"])
    def details(self):
        getData = StringHandling(str(request), 0)
        dataTableCurrent = []

        for item in getData:
            dataTableCurrent.append(unquote(item))

        column = GetAllColumnOfTable(dataTableCurrent[0], dataTableCurrent[1])
        dataTableEdit = []
        for index in range(len(column)):
            value = request.form.get(column[index])
            if value is None or value == "":
                dataTableEdit.append(dataTableCurrent[index + 2])
            else:
                dataTableEdit.append(value)

        query = OuputQueryUpdateDataTable(column, dataTableCurrent, dataTableEdit, 1)
        decodeQuery = query.replace("'", "$")
        SendRequest("https://sqs.us-east-1.amazonaws.com/126581837666/QueueEditDataTable", decodeQuery)

        url_convert_one = str(request.referrer)
        url_convert_two = url_convert_one.replace("edit-data-table/details?name=", "database/detail-table?name=")
        url_convert_three = url_convert_two.replace(current_user.UserName + "_", "")
        url = ""
        for i in range(len(url_convert_three)):
            if url_convert_three[i] == "?" and url_convert_three[i+1] == "i":
                break
            url += url_convert_three[i]
        return redirect(url)

class SubmitDeleteDataTable(ModelView):
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
        SendRequest("https://sqs.us-east-1.amazonaws.com/126581837666/QueueDeleteDataRowTable", decodeQuery)

        return redirect(request.referrer)

class SubmitDropTable(ModelView):
    @expose('/delete')
    def details(self):
        getName = False if request.args.get('name') is None else request.args.get('name')
        name_database = (current_user.UserName + "_" + GetDatabase(getName))
        name_table = GetTable(getName)
        query = name_database + "." + name_table
        SendRequest("https://sqs.us-east-1.amazonaws.com/126581837666/QueueDropTable", query)
        return redirect(request.referrer)

class SubmitDropDatabase(ModelView):
    @expose('/database')
    def submit(self):
        getName = False if request.args.get('name') is None else request.args.get('name')
        name_database = getName.replace(current_user.UserName + "_", "")

        user = UserCreateDatabase.query.filter_by(Name = name_database).delete()
        db.session.commit()

        SendRequest("https://sqs.us-east-1.amazonaws.com/126581837666/QueueDropDatabase", getName)
        return redirect(url_for('_user.index'))

class AllDetailsDatabase(ModelView):
    list_template = 'admin/database/all-details-database.html'

    @expose('/database')
    def details(self):
        getName = False if request.args.get('name') is None else request.args.get('name')
        name_database = (current_user.UserName + "_" + getName)

        allTable = get_all_table_of_database(name_database)

        allColumnInTable = []
        allQuantityColumn = []
        quantityTable = 0
        allDataTable = []
        allRowTable = []
        a = []
        for item in allTable:
            quantityTable += 1
            columnTable = GetAllColumnOfTable(name_database, item)
            allQuantityColumn.append(len(columnTable))
            allColumnInTable.append(columnTable)
            dataTable = GetAllDataOfTableInDatabase(name_database, item)
            allDataTable.append(dataTable)
            temp = CountRowTable(name_database, item)
            countRow = temp[0][0]
            allRowTable.append(countRow)

        self._template_args["queryUpdate"] = name_database
        self._template_args["nameDatabase"] = getName.upper()
        self._template_args["quantityTable"] = quantityTable
        self._template_args["allTable"] = allTable
        self._template_args["allColumnInTable"] = allColumnInTable
        self._template_args["allQuantityColumn"] = allQuantityColumn
        self._template_args["allDataTable"] = allDataTable
        self._template_args["allRowTable"] = allRowTable
        return super(AllDetailsDatabase, self).index_view()


userView = Admin(app, name='User', index_view=MyUserIndexView(url='/user', endpoint='_user'), base_template='master.html', template_mode='bootstrap4', url='/user', endpoint='_user')
userView.add_view(UserManageDatabaseView(name="Database", url='/user/databases', endpoint='_createDatabase'))
userView.add_view(UserProfileView(name="Profile", url='/user/profile', endpoint='_userProfile'))
userView.add_view(SubmitUserCreateDatabase(name="submit_database", url='/user/databases/add', endpoint='_submitCreateDatabase'))
userView.add_view(UserManageTableView(name="Table", url='/user/table', endpoint='_createTable'))
userView.add_view(SubmitUserManageTableView(name="submit_table", url='/user/table/add', endpoint='_submitCreateTable'))
userView.add_view(DetailDatabaseView(Users, db.session, name="Detail Database", url='/user/database', endpoint='_detailDatabase'))
userView.add_view(DetailTableView(Users, db.session, name="Detail Table", url='/user/database', endpoint='_detailTable'))
userView.add_view(DetailDataTableView(Users, db.session, name="Detail Data Table", url='/user/database/table/detail', endpoint='_detailDataTable'))
userView.add_view(EditColumnTableView(Users, db.session, name="Edit Column Table", url='/user/database/table', endpoint='_editColumnTable'))
userView.add_view(AddColumnTable(Users, db.session, name="add_column_table", url='/user/database/table/column', endpoint='_addColumnTable'))
userView.add_view(RenameColumnTableView(Users, db.session, name="Rename Column Table", url='/user/database/table/rename', endpoint='_renameColumnTable'))
userView.add_view(SubmitDropColumnTable(Users, db.session, name="drop_column_table", url='/user/database/table/drop', endpoint='_dropColumnTable'))
userView.add_view(AddDataTable(name="add_data_table", url='/user/add-data-table', endpoint='_addDataTable'))
userView.add_view(EditDataTableView(Users, db.session, name="Edit Data Table", url='/user/edit-data-table',endpoint='_editDataTable'))
userView.add_view(SubmitEditDataTable(Users, db.session, name="submit_edit_data_table", url='/user/edit-data-table/submit', endpoint='_submitEditDataTable'))
userView.add_view(SubmitDeleteDataTable(Users, db.session, name="submit_delete_data_table", url='/user/delete-data-table/submit',endpoint='_deleteDataTable'))
userView.add_view(SubmitDropTable(Users, db.session, name="submit_drop_table", url='/user/drop-table/submit',endpoint='_dropTable'))
userView.add_view(SubmitDropDatabase(Users, db.session, name="submit_drop_database", url='/user/drop-database/submit',endpoint='_dropDatabase'))
userView.add_view(AllDetailsDatabase(Users, db.session, name="Detail All Data Of Database", url='/user/all-details-database',endpoint='_allDetailsDatabase'))
