// script.js

// Aguarda o carregamento completo do DOM antes de executar o código JavaScript
document.addEventListener("DOMContentLoaded", function () {
    // Exemplo: Adicionando um evento de clique a um elemento com ID "meuElemento"
    var meuElemento = document.getElementById("meuElemento");

    if (meuElemento) {
        meuElemento.addEventListener("click", function () {
            alert("Cliquei no elemento!");
        });
    }

    // Exemplo: Implementação do lazy loading para imagens
    var lazyImages = document.querySelectorAll('img.lazy');

    if ('IntersectionObserver' in window) {
        var lazyImageObserver = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    var lazyImage = entry.target;
                    lazyImage.src = lazyImage.dataset.src;
                    lazyImage.classList.remove('lazy');
                    lazyImageObserver.unobserve(lazyImage);
                }
            });
        });

        lazyImages.forEach(function (lazyImage) {
            lazyImageObserver.observe(lazyImage);
        });
    }

    // Exemplo: Adicionar um evento de clique a um botão com ID "meuBotao"
    var meuBotao = document.getElementById("meuBotao");

    if (meuBotao) {
        meuBotao.addEventListener("click", function () {
            alert("Cliquei no botão!");
        });
    }

    // Exemplo: Fazer uma solicitação AJAX quando um botão com ID "meuBotaoAjax" for clicado
    var meuBotaoAjax = document.getElementById("meuBotaoAjax");

    if (meuBotaoAjax) {
        meuBotaoAjax.addEventListener("click", function () {
            // Fazer uma solicitação AJAX aqui
            // Por exemplo, usando a biblioteca fetch:
            fetch("/url_do_servidor")
                .then(function (response) {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error("Erro na solicitação");
                    }
                })
                .then(function (data) {
                    // Manipular os dados recebidos do servidor
                })
                .catch(function (error) {
                    console.error(error);
                });
        });
    }

    // Mais código JavaScript pode ser adicionado conforme necessário
});
