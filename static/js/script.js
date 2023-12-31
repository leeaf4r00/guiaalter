// script.js

// Aguarda o carregamento completo do DOM antes de executar o código JavaScript
document.addEventListener("DOMContentLoaded", function () {
    // Seu código JavaScript aqui

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
});

// Mais código JavaScript pode ser adicionado conforme necessário
