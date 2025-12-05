"""
Script para popular o banco de dados com tours de exemplo
"""
from app import create_app, db
from app.models.tours import Tour

"""
Script para popular o banco de dados com tours de exemplo usando imagens reais
"""
from app import create_app, db
from app.models.tours import Tour

def populate_tours():
    app = create_app()
    with app.app_context():
        print("🌴 Populando banco de dados com tours reais...")
        
        # Verifica se já existem tours
        existing_tours = Tour.query.count()
        if existing_tours > 0:
            print(f"⚠️  Já existem {existing_tours} tours no banco de dados. Verificando novos itens...")
            # Mantendo existentes e adicionando apenas novos

        
        # Tours em Destaque
        tours_destaque = [
            {
                "title": "Ilha do Amor",
                "description": "O cartão postal de Alter do Chão! Aproveite o dia na praia mais famosa, com águas cristalinas e areia branca. Travessia de catraia inclusa.",
                "price": 50.00,
                "category": "destaque",
                "image_url": "/static/img/alterdochao.jpg", # Imagem raiz
                "whatsapp_message": "Olá! Quero saber mais sobre a Ilha do Amor.",
                "is_active": True
            },
            {
                "title": "Pôr do Sol Mágico",
                "description": "Um espetáculo inesquecível! Contemple o pôr do sol no Rio Tapajós a bordo de uma lancha confortável. Inclui brinde com espumante.",
                "price": 180.00,
                "category": "destaque",
                "image_url": "/static/img/pordosol.jpg", # Imagem raiz
                "whatsapp_message": "Olá! Quero ver o Pôr do Sol.",
                "is_active": True
            },
            {
                "title": "Canal do Jari",
                "description": "Explore a biodiversidade amazônica! Navegue pelo Canal do Jari, observe pássaros, macacos e a vitória-régia. Natureza exuberante.",
                "price": 220.00,
                "category": "destaque",
                "image_url": "/static/img/canaldojari.jpg", # Imagem raiz
                "whatsapp_message": "Olá! Gostaria de ir ao Canal do Jari.",
                "is_active": True
            },
             {
                "title": "Flona do Tapajós",
                "description": "Imersão na floresta! Caminhada ecológica na Floresta Nacional do Tapajós com guias locais. Conheça as árvores centenárias.",
                "price": 300.00,
                "category": "destaque",
                "image_url": "/static/img/flonadotapajos.jpg", # Imagem raiz
                "whatsapp_message": "Olá! Tenho interesse na Flona do Tapajós.",
                "is_active": True
            }
        ]
        
        # Lago Verde (Floresta Encantada)
        tours_lago_verde = [
            {
                "title": "Floresta Encantada",
                "description": "Navegue por entre as árvores submersas na Floresta Encantada. Um cenário de contos de fadas com águas calmas e reflexos incríveis.",
                "price": 130.00,
                "category": "lagoverde",
                "image_url": "/static/img/lagoverde/florestaencantada.jpg",
                "whatsapp_message": "Olá! Quero conhecer a Floresta Encantada.",
                "is_active": True
            },
            {
                "title": "Igarapé do Macaco",
                "description": "Águas cristalinas e tranquilidade. O Igarapé do Macaco é perfeito para relaxar e curtir a natureza intocada.",
                "price": 140.00,
                "category": "lagoverde",
                "image_url": "/static/img/lagoverde/igarapedomacaco1.jpg",
                "whatsapp_message": "Olá! Quero ir ao Igarapé do Macaco.",
                "is_active": True
            },
            {
                "title": "Ponta da Valéria",
                "description": "Uma ponta de areia tranquila com vistas deslumbrantes. Ideal para quem busca sossego longe das multidões.",
                "price": 150.00,
                "category": "lagoverde",
                "image_url": "/static/img/lagoverde/pontadavaleria1.jpg",
                "whatsapp_message": "Olá! Gostaria de visitar a Ponta da Valéria.",
                "is_active": True
            }
        ]
        
        # Subindo o Rio (Pindobal, Cajutuba)
        tours_subindo = [
            {
                "title": "Praia do Pindobal",
                "description": "Cabanas de palha, peixe frito e um pôr do sol incrível. A Praia do Pindobal é perfeita para passar o dia com a família.",
                "price": 160.00,
                "category": "subindoorio",
                "image_url": "/static/img/subindoorio/pindobal1.jpg",
                "whatsapp_message": "Olá! Quero ir para Pindobal.",
                "is_active": True
            },
            {
                "title": "Praia de Cajutuba",
                "description": "Beleza rústica e tranquilidade. Cajutuba oferece extensas faixas de areia e águas mornas do Tapajós.",
                "price": 170.00,
                "category": "subindoorio",
                "image_url": "/static/img/subindoorio/cajutuba1.jpg",
                "whatsapp_message": "Olá! Quero conhecer Cajutuba.",
                "is_active": True
            },
            {
                "title": "Lago do Jucuruí",
                "description": "Observação de vida selvagem e pesca artesanal. Uma experiência autêntica no Lago do Jucuruí.",
                "price": 150.00,
                "category": "subindoorio",
                "image_url": "/static/img/subindoorio/lagodojucurui.jpg",
                "whatsapp_message": "Olá! Tenho interesse no Lago do Jucuruí.",
                "is_active": True
            },
             {
                "title": "Aramanai",
                "description": "Praia de águas calmas e límpidas. Ótima para banho e para apreciar a paisagem do Tapajós.",
                "price": 160.00,
                "category": "subindoorio",
                "image_url": "/static/img/subindoorio/aramanai1.jpg",
                "whatsapp_message": "Olá! Quero visitar Aramanai.",
                "is_active": True
            }
        ]
        
        # Descendo o Rio (Cururu, Ponta de Pedras)
        tours_descendo = [
            {
                "title": "Ponta do Cururu (Pôr do Sol)",
                "description": "O clássico encontro com os botos (se tiver sorte!) e um banco de areia perfeito para ver o sol se pôr.",
                "price": 100.00,
                "category": "descendoorio",
                "image_url": "/static/img/descendoorio/pontadocururu1.jpg",
                "whatsapp_message": "Olá! Quero ir na Ponta do Cururu.",
                "is_active": True
            },
            {
                "title": "Ponta de Pedras",
                "description": "Formações rochosas únicas na praia. Um visual diferente e encantador, com ótimos restaurantes locais.",
                "price": 180.00,
                "category": "descendoorio",
                "image_url": "/static/img/descendoorio/pontadepedras1.jpg",
                "whatsapp_message": "Olá! Gostaria de ir a Ponta de Pedras.",
                "is_active": True
            },
             {
                "title": "Lago Preto",
                "description": "Um espelho d'água na Amazônia. O Lago Preto reflete a floresta e o céu de forma espetacular.",
                "price": 190.00,
                "category": "descendoorio",
                "image_url": "/static/img/descendoorio/lagopreto1.jpg",
                "whatsapp_message": "Olá! Quero conhecer o Lago Preto.",
                "is_active": True
            },
            {
                "title": "Pedra Moca",
                "description": "Aventura e formações rochosas. Explore a região da Pedra Moca e desfrute de praias exclusivas.",
                "price": 180.00,
                "category": "descendoorio",
                "image_url": "/static/img/descendoorio/pedramoca1.jpg",
                "whatsapp_message": "Olá! Quero visitar a Pedra Moca.",
                "is_active": True
            }
        ]
        
        # Rio Arapiuns (Coroca, Icuxi, Toronó)
        tours_arapiuns = [
            {
                "title": "Ponta do Toronó",
                "description": "Um banco de areia quilométrico no meio do rio! Águas azuis turquesa que lembram o Caribe. Imperdível.",
                "price": 350.00,
                "category": "rioarapiuns",
                "image_url": "/static/img/rioarapiuns/pontadotorono1.jpg",
                "whatsapp_message": "Olá! Quero ir à Ponta do Toronó.",
                "is_active": True
            },
            {
                "title": "Comunidade Coroca (Tartarugas)",
                "description": "Turismo de base comunitária. Visite a criação de tartarugas, o apiário e conheça o artesanato local.",
                "price": 250.00,
                "category": "rioarapiuns",
                "image_url": "/static/img/rioarapiuns/comunidadecoroca1.jpg",
                "whatsapp_message": "Olá! Quero visitar a Comunidade Coroca.",
                "is_active": True
            },
            {
                "title": "Ponta do Icuxi",
                "description": "Praia deserta e águas profundas e azuis. O Icuxi é um paraíso escondido no Rio Arapiuns.",
                "price": 280.00,
                "category": "rioarapiuns",
                "image_url": "/static/img/rioarapiuns/icuxi1.jpg",
                "whatsapp_message": "Olá! Quero conhecer a Ponta do Icuxi.",
                "is_active": True
            },
            {
                "title": "Ponta Grande",
                "description": "Grandiosidade e beleza. A Ponta Grande oferece uma vista panorâmica incrível do encontro das águas e areias.",
                "price": 300.00,
                "category": "rioarapiuns",
                "image_url": "/static/img/rioarapiuns/pontagrande1.jpg",
                "whatsapp_message": "Olá! Quero ir para Ponta Grande.",
                "is_active": True
            }
        ]
        
        # Transfers e Embarcações
        tours_veiculos = [
            {
                "title": "Lancha Rápida (Privativo)",
                "description": "Agilidade e conforto para seu grupo. Lancha rápida para até 8 pessoas com marinheiro experiente. Perfeita para montar seu próprio roteiro.",
                "price": 800.00,
                "category": "veiculo_lancha",
                "image_url": "/static/img/veiculos/lancha.png",
                "whatsapp_message": "Olá! Gostaria de alugar uma Lancha Rápida.",
                "is_active": True
            },
            {
                "title": "Barco Regional (Gaiola)",
                "description": "Charme e tradição amazônica. Barco regional espaçoso, ideal para grupos grandes e passeios tranquilos contemplando a natureza.",
                "price": 1200.00,
                "category": "veiculo_barco",
                "image_url": "/static/img/veiculos/barco.png",
                "whatsapp_message": "Olá! Gostaria de alugar um Barco Regional.",
                "is_active": True
            },
            {
                "title": "Transfer Aeroporto (Privativo)",
                "description": "Chegue com tranquilidade. Transfer privativo do Aeroporto de Santarém para seu hotel em Alter do Chão. Carro com ar-condicionado.",
                "price": 150.00,
                "category": "veiculo_transfer",
                "image_url": "/static/img/veiculos/transfer.png",
                "whatsapp_message": "Olá! Preciso de um Transfer do Aeroporto.",
                "is_active": True
            },
             {
                "title": "Táxi Local",
                "description": "Deslocamento rápido dentro da vila ou para praias próximas acessíveis por terra. Segurança e preço justo.",
                "price": 30.00,
                "category": "veiculo_transfer",
                "image_url": "/static/img/veiculos/transfer.png",
                "whatsapp_message": "Olá! Preciso de um Táxi em Alter.",
                "is_active": True
            }
        ]
        
        # Adiciona todos os tours
        all_tours = tours_destaque + tours_lago_verde + tours_subindo + tours_descendo + tours_arapiuns + tours_veiculos
        
        added_count = 0
        for tour_data in all_tours:
            try:
                # Verifica duplicidade pelo título antes de adicionar
                if not Tour.query.filter_by(title=tour_data['title']).first():
                    tour = Tour(**tour_data)
                    db.session.add(tour)
                    added_count += 1
                    print(f"✅ Adicionado: {tour_data['title']}")
                else:
                    print(f"⏩ Pulado (já existe): {tour_data['title']}")
            except Exception as e:
                print(f"❌ Erro ao adicionar {tour_data['title']}: {e}")
        
        db.session.commit()
        print(f"\n🎉 Processo finalizado! {added_count} novos tours adicionados.")
        print(f"📊 Total de tours no banco: {Tour.query.count()}")

if __name__ == "__main__":
    populate_tours()
