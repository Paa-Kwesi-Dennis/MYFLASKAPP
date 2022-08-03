from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime 
import sqlite3

#TODo: fix refresh thing
#TODO: Update a todo
#TODO: Delete a todo

CREATE_TABLE = "Create table if not exists todo (id INTEGER PRIMARY KEY, todo TEXT, time_created TEXT)"
SELECT_ALL_FROM_TABLE = "Select * from todo order by id DESC"
UPDATE_TODO = "update todo set todo=?, post=? where id=?"

app = Flask(__name__)




@app.route("/", methods=["GET", "POST"])
def home():
    #This is showing the todos
    if request.method == "GET":
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        row_count = cursor.execute('select count(*) from todo').fetchone()# return tuple
        if row_count[0] ==1:
            cursor.execute(CREATE_TABLE)
            data = cursor.execute('select * from todo').fetchone()
            cursor.execute("update todo set id=1 where id=?", (data[0],))
            db.commit()
            dataset = cursor.execute(SELECT_ALL_FROM_TABLE)
            print('nigar')
            return render_template('home.html', dataset=dataset)
        else:
            cursor.execute(CREATE_TABLE)
            dataset = cursor.execute(SELECT_ALL_FROM_TABLE)
            return render_template('home.html', dataset=dataset)


        

    #This is adding the todos
    if request.method == 'POST':
        db = sqlite3.connect('database.db')
        cursor = db.cursor()
        cursor.execute(CREATE_TABLE)
        dataset = cursor.execute(SELECT_ALL_FROM_TABLE)
        return render_template('home.html', dataset=dataset,)

    return render_template('home.html')


@app.route("/addtask", methods=["GET", "POST"])
def addtask():
    if request.method == "POST":
        current_time = datetime.now()
        hour = current_time.hour
        minute = current_time.minute
        date = current_time.date()
        todo = request.form['todo']
        dates = f"{date} - {hour}:{minute}"

    
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        cursor.execute("Insert Into todo (todo, time_created) values (?, ?)", (todo, dates))
        db.commit()
        # Redirect to home when you submit on /addtask or on Addtask.html
        return redirect(url_for('home'))

    # This is the html template for the /addtask
    return render_template('Addtask.html')

#Updating the todos
@app.route("/update/<id>", methods = ["POST", "GET"])
def update(id):
    if request.method == "GET":
        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        todo_id = int(id)
        # Getting the text of the to-do
        todo = cursor.execute('select todo from todo where id=?', (todo_id,)).fetchone() #return tuple
        todo = ''.join(todo) #convert tuple to string
        return render_template("update.html", todos=todo, todo_id= todo_id)

    if request.method == "POST":
        db = sqlite3.connect("database.db")
        cursor = db.cursor()

        current_time = datetime.now()
        hour = current_time.hour
        minute = current_time.minute
        date = current_time.date()
        todo = request.form['todo']
        dates = f"{date} - {hour}:{minute}"


        db = sqlite3.connect("database.db")
        cursor = db.cursor()
        # data = cursor.execute("select * from todo where id=?", (id,)).fetchone()
        todo_id = int(id)+1
        #updating the todos
        cursor.execute("update todo set todo=?, time_created=? where id=?", (todo, dates, todo_id))
        db.commit()
        # Redirect to home when you update on update.html or /update/<id>
        return redirect(url_for('home'))

    return render_template('update.html')
    
# Get the id of to-do that is being updated-need text
# Get the text of that to-do-need-id
# Delete the text of that to-do and update the time
@app.route("/delete/<id>", methods=["POST", "GET"])
def delete(id):
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    #Getting the id the todo
    data = cursor.execute("select * from todo where id=?", (id,)).fetchone()
    todo_id = data[0]
    cursor.execute("delete from todo where id=?", (todo_id,))
    # cursor.execute("update todo set todo=?, time_created=? where id=?", (todo, dates, todo_id))
    db.commit()
    # Redirect to home when you update on update.html or /update/<id>
    return redirect(url_for('home'))



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form['name']
        password = request.form["password"]
        return render_template("login.html", name= name, password = password)
        
    return render_template("login.html")






if __name__ == "__main__":
    app.run(debug=True, threaded=True)