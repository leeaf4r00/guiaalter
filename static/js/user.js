document.addEventListener('DOMContentLoaded', function () {
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

    // Adiciona um ouvinte de evento ao formulário de login
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Impede o envio do formulário padrão
            const isValid = validateLoginForm();
            if (isValid) {
                // Implementar a lógica de login aqui (possivelmente usando AJAX)
            }
        });
    }

    // Adiciona um ouvinte de evento para 'loginSuccess'
    document.addEventListener('loginSuccess', function () {
        // Redireciona para a rota protegida após login
        window.location.href = '/admin'; // Substitua '/admin' pela rota desejada
    });

    // Aqui você pode adicionar mais códigos relacionados ao usuário, como requisições AJAX, etc.
});
