"""
Script para popular o banco de dados com tours de exemplo
"""
from app import create_app, db
from app.models.tours import Tour

def populate_tours():
    app = create_app()
    with app.app_context():
        print("🌴 Populando banco de dados com tours de exemplo...")
        
        # Verifica se já existem tours
        existing_tours = Tour.query.count()
        if existing_tours > 0:
            print(f"⚠️  Já existem {existing_tours} tours no banco de dados.")
            response = input("Deseja adicionar mais tours mesmo assim? (s/n): ")
            if response.lower() != 's':
                print("❌ Operação cancelada.")
                return
        
        # Tours em Destaque
        tours_destaque = [
            {
                "title": "Pôr do Sol no Lago Verde",
                "description": "Experimente o espetáculo mais bonito de Alter do Chão! Assista ao pôr do sol nas águas cristalinas do Lago Verde, com cores que vão do dourado ao roxo intenso. Inclui passeio de canoa e parada para fotos.",
                "price": 150.00,
                "category": "destaque",
                "image_url": "/static/images/lago-verde-sunset.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar o passeio Pôr do Sol no Lago Verde",
                "is_active": True
            },
            {
                "title": "Combo Praias + Floresta",
                "description": "O melhor dos dois mundos! Manhã nas praias paradisíacas de Alter do Chão e tarde explorando a floresta amazônica. Inclui almoço típico, guia especializado e equipamentos.",
                "price": 280.00,
                "category": "destaque",
                "image_url": "/static/images/combo-praias-floresta.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar o Combo Praias + Floresta",
                "is_active": True
            },
            {
                "title": "Passeio de Lancha VIP",
                "description": "Conforto e exclusividade! Passeio privativo de lancha pelas principais atrações de Alter do Chão. Máximo 8 pessoas, com capitão experiente, cooler com bebidas e snacks inclusos.",
                "price": 800.00,
                "category": "destaque",
                "image_url": "/static/images/lancha-vip.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar o Passeio de Lancha VIP",
                "is_active": True
            }
        ]
        
        # Lago Verde
        tours_lago_verde = [
            {
                "title": "Lago Verde Clássico",
                "description": "Passeio tradicional pelo Lago Verde com paradas para banho nas águas cristalinas. Duração: 4 horas. Inclui colete salva-vidas e guia.",
                "price": 120.00,
                "category": "lagoverde",
                "image_url": "/static/images/lago-verde-classico.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar o Lago Verde Clássico",
                "is_active": True
            },
            {
                "title": "Caiaque no Lago Verde",
                "description": "Aventura de caiaque pelas águas calmas do Lago Verde. Perfeito para iniciantes! Inclui instrutor, equipamentos e seguro.",
                "price": 90.00,
                "category": "lagoverde",
                "image_url": "/static/images/caiaque-lago-verde.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar o Caiaque no Lago Verde",
                "is_active": True
            }
        ]
        
        # Subindo o Rio
        tours_subindo = [
            {
                "title": "Rio Tapajós Aventura",
                "description": "Suba o majestoso Rio Tapajós e descubra praias desertas e comunidades ribeirinhas. Dia completo com almoço incluído.",
                "price": 200.00,
                "category": "subindoorio",
                "image_url": "/static/images/tapajos-aventura.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar o Rio Tapajós Aventura",
                "is_active": True
            },
            {
                "title": "Cachoeira da Piraoca",
                "description": "Viagem até a linda Cachoeira da Piraoca. Trilha leve, banho de cachoeira e contato com a natureza. Inclui lanche e guia.",
                "price": 180.00,
                "category": "subindoorio",
                "image_url": "/static/images/cachoeira-piraoca.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar a Cachoeira da Piraoca",
                "is_active": True
            }
        ]
        
        # Descendo o Rio
        tours_descendo = [
            {
                "title": "Ponta do Cururu",
                "description": "Descida do rio até a famosa Ponta do Cururu. Águas calmas, areia branca e visual incrível. Meio dia de passeio.",
                "price": 100.00,
                "category": "descendoorio",
                "image_url": "/static/images/ponta-cururu.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar a Ponta do Cururu",
                "is_active": True
            },
            {
                "title": "Ilha do Amor Completo",
                "description": "Passeio completo pela Ilha do Amor com paradas estratégicas. Inclui almoço, bebidas e equipamentos de mergulho.",
                "price": 160.00,
                "category": "descendoorio",
                "image_url": "/static/images/ilha-amor.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar a Ilha do Amor Completo",
                "is_active": True
            }
        ]
        
        # Rio Arapiuns
        tours_arapiuns = [
            {
                "title": "Expedição Rio Arapiuns",
                "description": "Expedição de dia completo pelo místico Rio Arapiuns. Visite comunidades indígenas, veja botos cor-de-rosa e mergulhe em águas cristalinas.",
                "price": 350.00,
                "category": "rioarapiuns",
                "image_url": "/static/images/rio-arapiuns.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar a Expedição Rio Arapiuns",
                "is_active": True
            },
            {
                "title": "Ponta de Pedras",
                "description": "Visite a incrível Ponta de Pedras no Rio Arapiuns. Formações rochosas únicas e águas azul-turquesa. Inclui guia e lanche.",
                "price": 220.00,
                "category": "rioarapiuns",
                "image_url": "/static/images/ponta-pedras.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar a Ponta de Pedras",
                "is_active": True
            }
        ]
        
        # Adiciona todos os tours
        all_tours = tours_destaque + tours_lago_verde + tours_subindo + tours_descendo + tours_arapiuns
        
        added_count = 0
        for tour_data in all_tours:
            try:
                tour = Tour(**tour_data)
                db.session.add(tour)
                added_count += 1
                print(f"✅ Adicionado: {tour_data['title']} ({tour_data['category']})")
            except Exception as e:
                print(f"❌ Erro ao adicionar {tour_data['title']}: {e}")
        
        db.session.commit()
        print(f"\n🎉 {added_count} tours adicionados com sucesso!")
        print(f"📊 Total de tours no banco: {Tour.query.count()}")
        
        # Mostra resumo por categoria
        print("\n📋 Resumo por categoria:")
        categories = ['destaque', 'lagoverde', 'subindoorio', 'descendoorio', 'rioarapiuns']
        for cat in categories:
            count = Tour.query.filter_by(category=cat).count()
            print(f"  - {cat}: {count} tours")

if __name__ == "__main__":
    populate_tours()
