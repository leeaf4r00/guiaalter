document.addEventListener('DOMContentLoaded', function () {
    function validateLoginForm() {
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!username || !password) {
            alert('Por favor, preencha todos os campos.');
            return false;
        }

        return true;
    }

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const isValid = validateLoginForm();
            if (isValid) {
                fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username: document.getElementById('username').value,
                        password: document.getElementById('password').value
                    })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'success') {
                        window.location.href = '/admin';
                    } else {
                        alert('Login falhou. Verifique suas credenciais.');
                    }
                })
                .catch(error => {
                    console.error('Erro na requisição AJAX:', error);
                });
            }
        });
    }
});
