// tours.js

document.addEventListener("DOMContentLoaded", function () {
    let currentImageIndex = 0;
    const images = document.querySelectorAll('.slider-img');
    const totalImages = images.length;

    function showNextImage() {
        images[currentImageIndex].style.display = 'none';
        currentImageIndex = (currentImageIndex + 1) % totalImages;
        images[currentImageIndex].style.display = 'block';
    }

    setInterval(showNextImage, 2000);

    // Lógica para obter o preço do pacote (pode ser uma chamada AJAX, cálculo, etc.)
    const pacotePrice = 100.00; // Defina o preço real aqui

    // Elemento HTML onde o preço será exibido
    const priceElement = document.querySelector(".price");

    // Função para atualizar o preço exibido
    function updatePrice() {
        priceElement.textContent = `Preço: R$ ${pacotePrice.toFixed(2)}`;
    }

    // Chame a função inicialmente para definir o preço
    updatePrice();

    // Exemplo de como você pode atualizar o preço periodicamente (a cada 5 segundos, por exemplo)
    setInterval(updatePrice, 5000); // Atualiza a cada 5 segundos (5000 milissegundos)
});
