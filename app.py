import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --- DEPLOYMENT UPDATES ---
# 1. Secret Key for security and sessions
app.config['SECRET_KEY'] = 'dev-key-taskdoy-123'

# 2. Robust Database Path for Windows and Render (Linux)
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

@app.route('/delete/<int:id>')
def delete(id):
    todo = db.session.get(Todo, id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))

# Ensure tables are created before the app starts
with app.app_context():
    # This creates the 'instance' folder if it doesn't exist
    if not os.path.exists(os.path.join(basedir, 'instance')):
        os.makedirs(os.path.join(basedir, 'instance'))
    db.create_all()

if __name__ == '__main__':
    # Using 0.0.0.0 is best practice for deployment environments
    app.run(host='0.0.0.0', port=5000, debug=True)