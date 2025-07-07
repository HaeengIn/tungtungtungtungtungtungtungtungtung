document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('form');
    if (!form) return;
    form.addEventListener('submit', function(e) {
        var username = document.getElementById('username').value.trim();
        if (username === 'TVS Dev Team') {
            e.preventDefault();
            var request_password = prompt('이 닉네임을 사용하려면 비밀번호를 입력하세요: ');
            if (request_password === null) {
                return false;
            }
            if (request_password === '') {
                alert('비밀번호를 입력해야 합니다.');
                e.preventDefault();
                return false;
            }
            document.getElementById('admin_password').value = request_password;

            var password_data = new FormData(form);
            fetch('write', {
                method: 'POST',
                body: password_data
            })
            .then(response => response.text())
            .then(html => {
                if (html.includes('password_error')) {
                    alert('비밀번호가 맞지 않습니다.');
                    e.preventDefault();
                    return false;
                } else {
                    window.location.href = '/';
                }
            })
        }
    });
});
// 1. 특수문자를 안전한 글자로 바꿔주는 함수
function escapeHTML(str) {
  return str
    .replace(/&/g, "&amp;")   // & → &amp;
    .replace(/</g, "&lt;")    // < → &lt;
    .replace(/>/g, "&gt;")    // > → &gt;
    .replace(/"/g, "&quot;")  // " → &quot;
    .replace(/'/g, "&#039;"); // ' → &#039;
}

// 2. 서버에서 받은 메시지들을 화면에 안전하게 표시
function showMessages(messages) {
  const list = document.getElementById("messageList"); // 글 목록 위치
  list.innerHTML = ""; // 이전에 있던 글들 지우기

  messages.forEach(msg => {
    // 각 메시지마다 <li> 태그 하나 만들기
    const li = document.createElement("li");

    // 이름과 메시지를 escape 처리해서 "스크립트가 아닌 글자"로 표시
    const safeName = escapeHTML(msg.name);
    const safeMessage = escapeHTML(msg.message);

    // li 태그 안에 글자 넣기 (스크립트 실행 X, 안전)
    li.textContent = `${safeName}: ${safeMessage}`;

    // 만든 글(li)을 목록에 추가하기
    list.appendChild(li);
  });
}

// 3. 페이지가 다 로드되면 글 목록 불러오기
document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/messages") // 서버에서 메시지 가져오기
    .then(res => res.json())
    .then(data => {
      showMessages(data); // 안전하게 화면에 표시
    });
});