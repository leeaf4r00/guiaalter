// Adicione isso ao seu código JavaScript no frontend
document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm'); // substitua 'loginForm' pelo ID do seu formulário

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
                .then(data => {
                    if (data.status === 'success') {
                        // Login bem-sucedido, redirecione para a página desejada
                        window.location.href = '/'; // Substitua '/' pela rota desejada
                    } else {
                        // Exiba uma mensagem de erro ou realize alguma ação adequada
                        console.error('Login falhou');
                    }
                })
                .catch(error => {
                    console.error('Erro na requisição AJAX:', error);
                });
        });
    }
});
