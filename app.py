from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('db/data.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = cursor.fetchall()

    conn.close()
    
    return render_template("index.html", posts=posts)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        username = request.form['username'].strip()
        if not username:
            username = '교하고 학생'
        title = request.form['title']
        content = request.form['content']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('db/data.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO posts (username, title, content, created_at) VALUES (?, ?, ?, ?)",
            (username, title, content, created_at)
        )

        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('post.html')

if __name__ == '__main__':
    app.run(debug=True)