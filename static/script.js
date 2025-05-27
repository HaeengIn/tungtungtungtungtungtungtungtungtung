document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('form');
    if (!form) return;
    form.addEventListener('submit', function(e) {
        var username = document.getElementById('username').value.trim();
        if (username === 'TVS Dev Team') {
            var admin_password = prompt('이 닉네임을 사용하려면 비밀번호를 입력하세요: ');
            if (admin_password === null || admin_password === '') {
                alert('비밀번호를 입력해야 합니다.');
                e.preventDefault();
                return false;
            }
            document.getElementById('admin_password').value = admin_password;
        }
    });
});