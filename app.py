from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return sqlite3.connect('db/data.db')

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = [
        {'id': row[0], 'username': row[1], 'title': row[2], 'content': row[3], 'created_at': row[4]}
        for row in cursor.fetchall()
    ]

    conn.close()

    return render_template("index.html", posts=posts)

@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        username = request.form['username'].strip()
        if not username:
            username = '교하고 학생'
        if username == 'TVS Dev Team':
            request_password = request.form.get('이 닉네임을 사용하려면 비밀번호를 입력하세요.', '')
            admin_password = os.getenv('admin_password')
            if request_password != admin_password:
                return "비밀번호가 일치하지 않습니다.", 403
        title = request.form['title']
        content = request.form['content']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO posts (username, title, content, created_at) VALUES (?, ?, ?, ?)",
            (username, title, content, created_at)
        )

        conn.commit()
        conn.close()

        return redirect('/')
    
    return render_template('write.html')

@app.route('/view/<int:post_id>')
def view(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return "Post not found", 404\
    
    return render_template("view.html", post=row)

if __name__ == '__main__':
    app.run(debug=True)