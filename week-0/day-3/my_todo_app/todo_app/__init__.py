import os

from flask import Flask
from flask import request
from flaskext.mysql import MySQL
from flask import render_template
from flask import redirect, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    mysql = MySQL()
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'administrator'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'Divik@123'
    app.config['MYSQL_DATABASE_DB'] = 'divik'
    mysql.init_app(app)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    def select_todos(name):
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("SELECT todo FROM todos WHERE user = %s",(name))
        data = cur.fetchall()
        print(data)
        retdata = [tmp[0] for tmp in data]
        if len(retdata) == 0:
            return None
        return retdata

    def insert_todo(name, todo):
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO todos(user,todo) VALUES(%s,%s)",(name,todo))
        conn.commit()
        return

    def add_todo_by_name(name, todo):
        # call DB function
        insert_todo(name, todo)
        return

    def get_todos_by_name(name):
        try:
            return select_todos(name)
        except:
            return None


    # http://127.0.0.1:5000/todos?name=duster
    @app.route('/todos')
    def todos():
        name = request.args.get('name')
        print('---------')
        print(name)
        print('---------')

        person_todo_list = get_todos_by_name(name)
        if person_todo_list == None:
            return render_template('404.html'), 404
        else:
            return render_template('todo_view.html',todos=person_todo_list)


    @app.route('/add_todos',methods=['POST'])
    def add_todos():
        name = request.form.get('user_name')
        todo = request.form.get('todo')
        add_todo_by_name(name, todo)
        return redirect(url_for('todos',name=name))

    return app

