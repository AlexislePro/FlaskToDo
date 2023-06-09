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

# When a GET request is received, the index() function queries the todos collection in the database using
# the find() method and returns a rendered HTML template called index.html along with the todos data to
# be displayed on the webpage.

# When a POST request is received, the index() function extracts data from the form submitted in the POST request
# using the request.form attribute, which is a dictionary-like object that holds the form data.
# The function then inserts this data into the todos collection in the database using the insert_one() method.
# After inserting the data, the function redirects to the index() function to display the updated todos data.
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        # The form data consists of four fields: content, degree, category, and date.
        # These fields are accessed using the request.form attribute
        # and then stored in a new document in the todos collection using the insert_one() method.
        content = request.form['content']
        degree = request.form['degree']
        category = request.form['category']
        date = request.form['date']
        todos.insert_one({'content': content, 'degree': degree, 'category': category, 'date': date})
        return redirect(url_for('index'))

    all_todos = todos.find()
    # The render_template() function is used to generate an HTML page based on the index.html template,
    # which is passed the all_todos variable holding the todos data.
    # This function returns the generated HTML page as a string, which is then sent as a response to the user's browser.
    return render_template('index.html', todos=all_todos)

#When a POST request is received, the delete() function extracts the ID value from the URL using the id parameter.
# It then calls the delete_one() method on the todos collection in the database,
# passing a dictionary object that specifies which document to delete based on the ID value extracted from the URL.


@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    #After deleting the document from the todos collection,
    # the function redirects to the index() function using the url_for() function, which generates the URL for the index() function.
    # The redirect() function is then used to redirect the user's browser to the URL generated by url_for(),
    # which displays the updated list of todos after the deletion.
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
