// Exemplo de script para alternar a exibição da navbar em dispositivos móveis
document.addEventListener("DOMContentLoaded", function () {
    const navbarToggler = document.querySelector(".navbar-toggler");
    const navbarMenu = document.querySelector("#navbarNav");

    navbarToggler.addEventListener("click", function () {
        // Toggle a visibilidade do menu
        navbarMenu.classList.toggle("show");
    });
});
