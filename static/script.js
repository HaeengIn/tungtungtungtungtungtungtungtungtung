document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('form');
    if (!form) return;
    form.addEventListener('submit', function(e) {
        var username = document.getElementById('username').value.trim();
        if (username === 'TVS Dev Team') {
            var request_password = prompt('이 닉네임을 사용하려면 비밀번호를 입력하세요: ');
            if (request_password === null) {
                e.preventDefault();
                return false;
            }
            if (request_password === '') {
                alert('비밀번호를 입력해야 합니다.');
                e.preventDefault();
                return false;
            }
            if (request_password !== admin_password) {
                alert('비밀번호가 일치하지 않습니다.');
                e.preventDefault();
                return false;
            }
            document.getElementById('admin_password').value = admin_password;
        }
    });
});