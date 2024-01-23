document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            event.preventDefault();
            const isValid = validateLoginForm();

            if (isValid) {
                const username = document.getElementById('username').value.trim();
                const password = document.getElementById('password').value.trim();

                login(username, password);
            }
        });
    }

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

    function login(username, password) {
        fetch("/login", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
            .then(handleResponse)
            .then(handleLoginSuccess)
            .catch(handleError);
    }

    function handleResponse(response) {
        if (!response.ok) {
            throw new Error('Erro na solicitação: ' + response.statusText);
        }
        return response.json();
    }

    function handleLoginSuccess(data) {
        if (data.redirect) {
            window.location.href = data.redirect;
        } else {
            alert("Credenciais inválidas. Tente novamente.");
        }
    }

    function handleError(error) {
        console.error(error);
        alert('Ocorreu um erro ao processar seu login. Por favor, tente novamente.');
    }

    // Outros eventos e lógica JavaScript podem ser adicionados conforme necessário
});
