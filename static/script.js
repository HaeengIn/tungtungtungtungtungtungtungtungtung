document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('writeForm');
    if (!form) return;
    form.addEventListener('submit', function(e) {
        var username = document.getElementById('username').value.trim();
        if (username === 'TVS Dev Team') {
            var pw = prompt('이 닉네임을 사용하려면 비밀번호를 입력하세요: ');
            if (pw === null || pw === '') {
                alert('비밀번호를 입력해야 합니다.');
                e.preventDefault();
                return false;
            }
            document.getElementById('admin_password').value = pw;
        }
    });
});