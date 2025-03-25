from flask import Flask, render_template, redirect, request, url_for
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

app = Flask(__name__)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT FALSE
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, content, completed FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form['task']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (content, completed) VALUES (%s, %s)', (task_content, False))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET completed = TRUE WHERE id = %s', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run()
