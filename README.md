Task Doy - Flask Todo App

A sleek, responsive To-Do List application built with Python and Flask. This project allows users to manage daily tasks with a modern interface, featuring task editing, completion toggles, and an Undo safety net.

Links Live Demo: https://todotask-1qep.onrender.com/ Repository: https://github.com/NbscDandoy/Todotask

System Design

Entity Relationship Diagram (ERD) The database uses a relational structure to ensure data persistence.

Field Type Constraint Description id Integer Primary Key Unique task identifier. title String Not Null The task description. complete Boolean Default: False Status of the task. System Flowchart The following diagram maps the logic from the user interface through the Flask routes to the database file operations.

Implementation Algorithm The "Undo" feature utilizes a Buffered Persistence Strategy:

Capture: Fetch task data from SQLite before deletion. Buffer: Store the title in the encrypted flask.session. Execute: Commit the hard delete to the todos.db file. Notify: Redirect with a URL flag (?undone=True) to trigger the UI toast. Restore: Re-insert data from the session buffer if the user clicks "Undo". Tech Stack Backend: Python / Flask Database: SQLite & SQLAlchemy Frontend: HTML5, CSS3, Bootstrap Icons Deployment: Render.com

Local Setup

Clone the repo: git clone https://github.com/NbscDandoy/Todotask.git Install dependencies: pip install flask flask-sqlalchemy Run the app: python app.py
