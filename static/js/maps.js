// Função para inicializar o mapa
function initMap() {
    // Cria um mapa na div 'mapid' e define as coordenadas iniciais e o nível de zoom
    var map = L.map('mapid').setView([-2.50381, -54.95145], 13);

    // Adiciona os tiles do OpenStreetMap ao mapa
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© Contribuições do OpenStreetMap',
        maxZoom: 19
    }).addTo(map);

    // Adiciona um marcador no mapa
    var marker = L.marker([-2.50381, -54.95145]).addTo(map);
    marker.bindPopup("<b>Olá!</b><br>Alter do Chão.");
}

// Chama a função initMap() quando a janela é carregada
window.onload = initMap;
