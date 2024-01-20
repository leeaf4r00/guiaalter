// static/js/navbar.js
// Script para alternar a exibição da navbar em dispositivos móveis
document.addEventListener("DOMContentLoaded", function () {
    const navbarToggler = document.querySelector(".navbar-toggler");
    const navbarMenu = document.querySelector(".navbar-nav");

    navbarToggler.addEventListener("click", function () {
        // Alternar a visibilidade do menu
        navbarMenu.classList.toggle("show");

        // Opcional: Adicionar lógica para escurecer o fundo quando o menu está aberto
        // document.body.classList.toggle('body-dimmed');
    });
});
