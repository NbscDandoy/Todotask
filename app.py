import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- DEPLOYMENT UPDATES ---
# Secret key is mandatory to securely sign cookies for Flask session caching
app.config['SECRET_KEY'] = 'dev-key-taskdoy-123'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'todos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

# Database Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>')
def update(id):
    todo = db.session.get(Todo, id)
    if todo:
        todo.complete = not todo.complete
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    todo = db.session.get(Todo, id)
    if not todo:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        todo.title = request.form.get('title')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo)

# --- UPDATED DELETE WITH UNDO SUPPORT ---
@app.route('/delete/<int:id>')
def delete(id):
    todo = db.session.get(Todo, id)
    if todo:
        # Save the task title in a session container so we can restore it if "Undo" is clicked
        session['last_deleted_title'] = todo.title
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index', undone=True))

# --- NEW UNDO ROUTE ---
@app.route('/undo')
def undo():
    # Retrieve and simultaneously drop the title from the cookie context
    title = session.pop('last_deleted_title', None)
    if title:
        # Re-add the task back to the SQLite layer
        new_todo = Todo(title=title, complete=False)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

# Ensure database structures and tracking instance folders are generated setup
with app.app_context():
    if not os.path.exists(os.path.join(basedir, 'instance')):
        os.makedirs(os.path.join(basedir, 'instance'))
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
