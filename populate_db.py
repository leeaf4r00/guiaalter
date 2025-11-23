from app import create_app, db
from app.models.tours import Tour

app = create_app()

def populate_tours():
    """Popula o banco de dados com os passeios iniciais"""
    tours_data = [
        # Rio Arapiuns
        {
            'title': 'Alter do Chão',
            'description': 'Centro turístico principal',
            'price': 100.0,
            'image_url': '/static/img/rioarapiuns/alterdochao.jpg',
            'category': 'rioarapiuns',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre o passeio em Alter do Chão'
        },
        {
            'title': 'Comunidades Tradicionais',
            'description': 'Conheça a cultura ribeirinha',
            'price': 170.0,
            'image_url': '/static/img/rioarapiuns/canaldojari.jpg',
            'category': 'rioarapiuns',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre o passeio nas Comunidades Tradicionais'
        },
        {
            'title': 'Trilhas Ecológicas',
            'description': 'Explore a floresta amazônica',
            'price': 165.0,
            'image_url': '/static/img/rioarapiuns/flonatapajos.jpg',
            'category': 'rioarapiuns',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre as Trilhas Ecológicas'
        },
        # Lago Verde
        {
            'title': 'Lago Verde',
            'description': 'Águas cristalinas e praias paradisíacas',
            'price': 150.0,
            'image_url': '/static/img/lagoverde/lagoverde1.jpg',
            'category': 'lagoverde',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre o passeio no Lago Verde'
        },
        {
            'title': 'Ilha do Amor',
            'description': 'Areia branca e paisagens deslumbrantes',
            'price': 120.0,
            'image_url': '/static/img/lagoverde/alterdochao.jpg',
            'category': 'lagoverde',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre a Ilha do Amor'
        },
        {
            'title': 'Floresta Encantada',
            'description': 'Trilhas e natureza exuberante',
            'price': 140.0,
            'image_url': '/static/img/lagoverde/florestaencantada.jpg',
            'category': 'lagoverde',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre a Floresta Encantada'
        },
        {
            'title': 'Igarapé do Camarão',
            'description': 'Águas calmas e vida aquática',
            'price': 130.0,
            'image_url': '/static/img/lagoverde/igarapecamarao.jpg',
            'category': 'lagoverde',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre o Igarapé do Camarão'
        },
        # Subindo o Rio
        {
            'title': 'Aramã',
            'description': 'Comunidade tradicional ribeirinha',
            'price': 160.0,
            'image_url': '/static/img/subindoorio/aramana1.jpg',
            'category': 'subindoorio',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre o passeio em Aramã'
        },
        {
            'title': 'Cajutuba',
            'description': 'Floresta e cultura local',
            'price': 145.0,
            'image_url': '/static/img/subindoorio/cajutuba1.jpg',
            'category': 'subindoorio',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre o passeio em Cajutuba'
        },
        {
            'title': 'Lago do Jucurui',
            'description': 'Lago tranquilo e pesca',
            'price': 155.0,
            'image_url': '/static/img/subindoorio/lagodojucurui.jpg',
            'category': 'subindoorio',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre o Lago do Jucurui'
        },
        {
            'title': 'Pindobal',
            'description': 'Natureza preservada',
            'price': 150.0,
            'image_url': '/static/img/subindoorio/pindobal1.jpg',
            'category': 'subindoorio',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre o passeio em Pindobal'
        },
        # Descendo o Rio
        {
            'title': 'Pôr do Sol',
            'description': 'Vista espetacular do entardecer',
            'price': 135.0,
            'image_url': '/static/img/descendoorio/alterdochao.jpg',
            'category': 'descendoorio',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre o passeio Pôr do Sol'
        },
        {
            'title': 'Canal do Jari',
            'description': 'Navegação pelo canal',
            'price': 145.0,
            'image_url': '/static/img/descendoorio/canaldojari.jpg',
            'category': 'descendoorio',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre o Canal do Jari'
        },
        {
            'title': 'Lago do Jacaré',
            'description': 'Observação de jacarés',
            'price': 155.0,
            'image_url': '/static/img/descendoorio/lagodojacare.jpg',
            'category': 'descendoorio',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre o Lago do Jacaré'
        },
        {
            'title': 'Ponta do Cururu',
            'description': 'Praia paradisíaca',
            'price': 140.0,
            'image_url': '/static/img/descendoorio/pontadecururu.jpg',
            'category': 'descendoorio',
            'whatsapp_message': 'Olá, gostaria de saber mais sobre a Ponta do Cururu'
        }
    ]

    with app.app_context():
        # Verifica se já existem tours
        if Tour.query.first():
            print("Tours já populados.")
            return

        for data in tours_data:
            tour = Tour(**data)
            db.session.add(tour)
        
        db.session.commit()
        print(f"{len(tours_data)} tours adicionados com sucesso!")

if __name__ == '__main__':
    populate_tours()
