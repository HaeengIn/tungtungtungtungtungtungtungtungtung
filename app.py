# 모듈 임포트
from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os
import Flask-Limiter

# .env 파일 불러오기
load_dotenv()

# Render 환경 변수에서 admin_password 가져오기
admin_password = os.environ.get('admin_password')

# Flask 앱 생성
app = Flask(__name__)

# 데이터베이스 연결
def get_db_connection():
    return sqlite3.connect('db/data.db')

# 메인 페이지
@app.route('/')
def index():
    # 데이터베이스에서 글 목록 불러오기
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = [
        {'id': row[0], 'username': row[1], 'title': row[2], 'content': row[3], 'created_at': row[4]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return render_template("index.html", posts=posts)

# 글 작성 페이지
@app.route('/write', methods=['GET', 'POST'])
def write():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        username = request.form['username'].strip() # 아무것도 입력되지 않으면 "교하고 학생"으로 설정
        if not username:
            username = '교하고 학생'
        if username == 'TVS Dev Team':
            # 관리자 비밀번호 입력값을 request_password에 저장
            request_password = request.form.get('admin_password', '').strip()
            # 환경 변수에서 admin_password를 가져와서 비교
            admin_password = os.getenv('admin_password', '').strip()
            if request_password is None:
                return render_template('write.html', username=username, title=title, content=content)
            if request_password != admin_password:
                return render_template('write.html', username=username, title=title, content=content, password_error=True)
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 데이터베이스에 연결해서 글 저장하고 메인 페이지로 이동하기
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

# 글 상세 페이지
@app.route('/view/<int:post_id>')
def view(post_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    row = cursor.fetchone()
    conn.close()

    # 글이 존재하지 않는 경우 404 띄우기
    if row is None:
        return "Post not found", 404
    return render_template("view.html", post=row)

# 앱 실행
if __name__ == '__main__':
    app.run(debug=True)