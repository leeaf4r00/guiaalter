"""
Script para adicionar mais tours ao banco de dados
"""
from app import create_app, db
from app.models.tours import Tour

def add_more_tours():
    app = create_app()
    with app.app_context():
        print("🌴 Adicionando mais tours ao banco de dados...")
        
        # Tours adicionais variados
        new_tours = [
            # Mais tours em destaque
            {
                "title": "Experiência Completa Alter 3 Dias",
                "description": "Pacote completo de 3 dias explorando o melhor de Alter do Chão. Inclui Lago Verde, Ilha do Amor, Ponta do Cururu, passeio de canoa, visita a comunidades, todas as refeições e hospedagem.",
                "price": 1200.00,
                "category": "destaque",
                "image_url": "/static/images/pacote-completo.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar a Experiência Completa Alter 3 Dias",
                "is_active": True
            },
            {
                "title": "Observação de Botos Cor-de-Rosa",
                "description": "Encontro mágico com os botos cor-de-rosa do Rio Tapajós. Passeio ao amanhecer quando eles estão mais ativos. Inclui guia especializado e equipamento fotográfico.",
                "price": 180.00,
                "category": "destaque",
                "image_url": "/static/images/botos-rosa.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar a Observação de Botos Cor-de-Rosa",
                "is_active": True
            },
            
            # Mais tours Lago Verde
            {
                "title": "Stand Up Paddle no Lago Verde",
                "description": "Explore o Lago Verde de uma forma diferente! Aula de SUP com instrutor, equipamentos inclusos. Perfeito para fotos incríveis!",
                "price": 100.00,
                "category": "lagoverde",
                "image_url": "/static/images/sup-lago-verde.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar o Stand Up Paddle no Lago Verde",
                "is_active": True
            },
            {
                "title": "Trilha Floresta Encantada",
                "description": "Caminhada guiada pela Floresta Encantada ao redor do Lago Verde. Aprenda sobre a flora e fauna local. Duração: 3 horas.",
                "price": 80.00,
                "category": "lagoverde",
                "image_url": "/static/images/trilha-floresta.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar a Trilha Floresta Encantada",
                "is_active": True
            },
            
            # Mais tours Subindo o Rio
            {
                "title": "Pirarucu Gigante - Pesca Esportiva",
                "description": "Experiência de pesca esportiva do famoso Pirarucu. Pesque e solte com guia experiente. Inclui equipamentos e almoço.",
                "price": 350.00,
                "category": "subindoorio",
                "image_url": "/static/images/pesca-pirarucu.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar o Pirarucu Gigante - Pesca Esportiva",
                "is_active": True
            },
            {
                "title": "Comunidade Indígena Borari",
                "description": "Visita cultural à comunidade indígena Borari. Conheça tradições, artesanato e culinária típica. Experiência autêntica e respeitosa.",
                "price": 150.00,
                "category": "subindoorio",
                "image_url": "/static/images/comunidade-borari.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar a Comunidade Indígena Borari",
                "is_active": True
            },
            
            # Mais tours Descendo o Rio
            {
                "title": "Praia do Cajueiro - Dia Completo",
                "description": "Dia inteiro na paradisíaca Praia do Cajueiro. Águas calmas, areia branca e sombra natural. Inclui almoço e bebidas.",
                "price": 140.00,
                "category": "descendoorio",
                "image_url": "/static/images/praia-cajueiro.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar a Praia do Cajueiro - Dia Completo",
                "is_active": True
            },
            {
                "title": "Mergulho com Snorkel",
                "description": "Explore o mundo subaquático do Rio Tapajós. Veja peixes coloridos e formações rochosas. Equipamentos e instrutor inclusos.",
                "price": 110.00,
                "category": "descendoorio",
                "image_url": "/static/images/snorkel.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar o Mergulho com Snorkel",
                "is_active": True
            },
            
            # Mais tours Rio Arapiuns
            {
                "title": "Acampamento Selvagem 2 Dias",
                "description": "Aventura de 2 dias acampando nas margens do Rio Arapiuns. Inclui barraca, refeições, fogueira e histórias locais. Máximo 6 pessoas.",
                "price": 450.00,
                "category": "rioarapiuns",
                "image_url": "/static/images/acampamento.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar o Acampamento Selvagem 2 Dias",
                "is_active": True
            },
            {
                "title": "Fotografia de Natureza",
                "description": "Tour especializado para fotógrafos. Melhores locais e horários para capturar a beleza do Arapiuns. Guia fotógrafo profissional.",
                "price": 280.00,
                "category": "rioarapiuns",
                "image_url": "/static/images/foto-natureza.jpg",
                "whatsapp_message": "Olá! Gostaria de reservar o tour de Fotografia de Natureza",
                "is_active": True
            }
        ]
        
        added_count = 0
        for tour_data in new_tours:
            try:
                # Verifica se já existe um tour com o mesmo título
                existing = Tour.query.filter_by(title=tour_data['title']).first()
                if existing:
                    print(f"⏭️  Pulado (já existe): {tour_data['title']}")
                    continue
                    
                tour = Tour(**tour_data)
                db.session.add(tour)
                added_count += 1
                print(f"✅ Adicionado: {tour_data['title']} ({tour_data['category']}) - R$ {tour_data['price']:.2f}")
            except Exception as e:
                print(f"❌ Erro ao adicionar {tour_data['title']}: {e}")
        
        if added_count > 0:
            db.session.commit()
            print(f"\n🎉 {added_count} novos tours adicionados com sucesso!")
        else:
            print(f"\n✅ Nenhum tour novo adicionado (todos já existem)")
            
        print(f"📊 Total de tours no banco: {Tour.query.count()}")
        
        # Mostra resumo por categoria
        print("\n📋 Resumo por categoria:")
        categories = ['destaque', 'lagoverde', 'subindoorio', 'descendoorio', 'rioarapiuns']
        for cat in categories:
            count = Tour.query.filter_by(category=cat).count()
            print(f"  - {cat}: {count} tours")

if __name__ == "__main__":
    add_more_tours()
