from flask import Flask, render_template, request, redirect
import oracledb
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_oracle_connection():
    return oracledb.connect(
        user = os.getenv('oracle_user'),
        password = os.getenv('oracle_password'),
        dsn = os.getenv('oracle_dsn'),
        config_dir = os.getenv('oracle_wallet_dir'),
        wallet_location = os.getenv('oracle_wallet_dir')
    )

@app.route('/')
def index():
    conn = get_oracle_connection()
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
        title = request.form['title']
        content = request.form['content']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = get_oracle_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO posts (username, title, content, created_at) VALUES (:1, :2, :3, :4)",
            (username, title, content, created_at)
        )

        conn.commit()
        conn.close()

        return redirect('/')
    
    return render_template('write.html')

@app.route('/view/<int:post_id>')
def view(post_id):
    conn = get_oracle_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE id = :1", (post_id,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return "Post not found", 404
    post = {'id': row[0], 'username': row[1], 'title': row[2], 'content': row[3], 'created_at': row[4]}
    
    return render_template("view.html", post=post)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)