import pymongo as pymongo
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__, template_folder='templates', static_folder='static')
# client = MongoClient('localhost', 27017)
# client = MongoClient('localhost', 27017, username='username', password='password')


client = pymongo.MongoClient(
    "mongodb+srv://a_cognet:alexisadmin@cluster0.vtrpkli.mongodb.net/?retryWrites=true&w=majority")
db = client.test

db = client.flask_db
todos = db.todos


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        category = request.form['category']
        date = request.form['date']
        todos.insert_one({'content': content, 'degree': degree, 'category': category, 'date': date})
        return redirect(url_for('index'))

    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)


@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
