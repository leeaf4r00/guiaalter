// Adicione isso ao seu código JavaScript no frontend
document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm'); // Substitua 'loginForm' pelo ID do seu formulário

    function handleLoginResponse(data) {
        if (data.redirect) {
            // Login bem-sucedido, redirecione para a página especificada no servidor
            window.location.href = data.redirect;
        } else {
            // Exiba uma mensagem de erro para o usuário
            alert('Login falhou: ' + data.message);
        }
    }

    function handleLoginError(error) {
        console.error('Erro na requisição AJAX:', error);
        alert('Erro ao tentar fazer login. Por favor, tente novamente.');
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Impede o envio do formulário padrão

            // Obtenha os valores de usuário e senha do formulário
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value.trim();

            // Faça uma requisição AJAX para o endpoint de login
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            })
                .then(response => response.json())
                .then(handleLoginResponse)
                .catch(handleLoginError);
        });
    }
});
