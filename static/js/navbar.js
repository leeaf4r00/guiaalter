// Adicione um evento de clique ao botão de hambúrguer para alternar a exibição da lista colapsável
document.getElementById('toggleMenu').addEventListener('click', function () {
    document.querySelector('.navbar').classList.toggle('navbar-active');
});
