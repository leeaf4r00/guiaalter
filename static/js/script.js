// script.js

// Aguarda o carregamento completo do DOM antes de executar o código JavaScript
document.addEventListener("DOMContentLoaded", function () {
    // Adiciona um ouvinte de evento ao formulário de login
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault(); // Impede o envio do formulário padrão
            const isValid = validateLoginForm();

            if (isValid) {
                const username = document.getElementById('username').value.trim();
                const password = document.getElementById('password').value.trim();

                // Fazer uma solicitação AJAX para o backend
                fetch("/login", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                })
                    .then(function (response) {
                        if (response.ok) {
                            return response.json();
                        } else {
                            throw new Error("Erro na solicitação");
                        }
                    })
                    .then(function (data) {
                        if (data.status === 'success') {
                            // Redireciona para a rota protegida após login bem-sucedido
                            window.location.href = '/admin'; // Substitua '/admin' pela rota desejada
                        } else {
                            // Mostrar mensagem de erro
                            alert("Credenciais inválidas. Tente novamente.");
                        }
                    })
                    .catch(function (error) {
                        console.error(error);
                    });
            }
        });
    }

    // Função para validar o formulário de login
    function validateLoginForm() {
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        if (!username || !password) {
            alert('Por favor, preencha todos os campos.');
            return false;
        }

        // Adicione aqui mais validações conforme necessário

        return true;
    }

    // Outros eventos e lógica JavaScript podem ser adicionados conforme necessário
});
