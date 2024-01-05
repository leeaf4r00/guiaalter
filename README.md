# Guia de Alter

Este projeto é um aplicativo web Flask que fornece uma série de funcionalidades, incluindo autenticação de usuários, exibição de informações estáticas e dinâmicas, gerenciamento de conteúdo e apresenta informações turísticas sobre a região de Alter do Chão, no Brasil.

## Estrutura do Projeto

O projeto está estruturado como um pacote Python com vários módulos. A estrutura básica é a seguinte:

guiadealter/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── routes_tours.py
│   ├── paineladmin.py
│   ├── forms.py
│   ├── database.py
│   ├── models/
│   │   ├── user.py
│   │   ├── models.py
│   │   ├── models_clients.py
│   │   ├── db.py
│   │   ├── clients.py
│   │   ├── __init__.py
│   │   └── __pycache__/
│   ├── __pycache__/
│
├── data/
│
├── src/
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── main.css
│   │   ├── header.css
│   │   ├── footer.css
│   │   └── (outras folhas de estilo)
│   ├── js/
│   │   ├── user.js
│   │   ├── script.js
│   │   └── (outros arquivos JavaScript)
│   ├── img/
│   │   ├── topo1.jpg
│   │   ├── topo.jpg
│   │   ├── ruby2.png
│   │   ├── ruby1.png
│   │   ├── pontadavaleria2.jpg
│   │   ├── pontadavaleria1.jpg
│   │   ├── pontadavaleria.jpg
│   │   ├── piracaia2.jpg
│   │   ├── piracaia.jpg
│   │   ├── pindobal.jpg
│   │   ├── logoruby.png
│   │   ├── logo.png
│   │   ├── lagoverde4.jpg
│   │   ├── lagoverde3.jpg
│   │   ├── lagoverde2.jpg
│   │   ├── lagoverde1.jpg
│   │   ├── igarapemacaco3.jpg
│   │   ├── igarapemacaco2.jpg
│   │   ├── igarapemacaco1.jpg
│   │   ├── igarapecamarao.jpg
│   │   ├── florestaencantada.jpg
│   │   ├── flonadotapajos.jpg
│   │   ├── canaldojari.jpg
│   │   ├── alterdochao2.jpg
│   │   ├── alterdochao.jpg
│   │   ├── rioarapiuns/
│   │   │   ├── comunidadecoroca2.jpg
│   │   │   ├── comunidadecoroca1.jpg
│   │   │   ├── (outras imagens)
│   │   ├── descendoorio/
│   │   │   ├── pontadepedras3.jpg
│   │   │   ├── pontadepedras2.jpg
│   │   │   ├── pontadepedras1.jpg
│   │   │   ├── pontacururu3.jpg
│   │   │   ├── pontacururu2.jpg
│   │   │   ├── pontacururu1.jpg
│   │   │   ├── pedramoca3.JPG
│   │   │   ├── pedramoca2.jpg
│   │   │   ├── pedramoca1.jpg
│   │   │   ├── lagopreto3.jpg
│   │   │   ├── lagopreto2.jpg
│   │   │   ├── lagopreto1.jpg
│   │   │   ├── lagojacare2.jpg
│   │   │   ├── lagojacare1.jpg
│   │   │   ├── casadosaulo2.jpg
│   │   │   ├── casadosaulo1.jpg
│   │   │   ├── canaldojari3.jpg
│   │   │   ├── canaldojari2.jpg
│   │   │   ├── canaldojari1.jpg
│   │   │   ├── (outras imagens)
│
├── templates/
│   ├── veiculos.html
│   ├── tours.html
│   ├── tourdestaques.html
│   ├── top10para.html
│   ├── terms-of-use.html
│   ├── suporte.html
│   ├── subindoorio.html
│   ├── sobrenos.html
│   ├── rioarapiuns.html
│   ├── reservas.html
│   ├── privacy-policy.html
│   ├── passeiosnovos.html
│   ├── passeiosdestaque.html
│   ├── passeiosagendar.html
│   ├── passeios.html
│   ├── pacotesgastronomicos.html
│   ├── pacotes.html
│   ├── login.html
│   ├── lagoverde.html
│   ├── index.html
│   ├── hotels.html
│   ├── formulario.html
│   ├── explorealter.html
│   ├── descendoorio.html
│   ├── depoimentos.html
│   ├── contato.html
│   ├── cadastro.html
│   ├── buffets.html
│   ├── admin.html
│   └── 404.html
│
├── .gitattributes
├── app.py
├── database.py
├── models.py
├── Procfile
├── README.md
└── requirements.txt

### Descrição dos Arquivos

* guiadealter/
  │
  ├── app/ - Contém os principais arquivos relacionados à lógica da aplicação.
  │   ├── __init__.py - Arquivo vazio que indica que o diretório é um pacote Python.
  │   ├── routes.py - Define as rotas principais do aplicativo Flask.
  │   ├── routes_tours.py - Define as rotas relacionadas a passeios turísticos.
  │   ├── paineladmin.py - Arquivo para a administração do painel de controle (admin).
  │   ├── forms.py - Contém as classes de formulários para a aplicação.
  │   ├── database.py - Contém funções para interagir com o banco de dados SQLite.
  │   ├── models/ - Diretório que organiza os modelos de dados da aplicação.
  │   │   ├── user.py - Define o modelo de usuário para o sistema de autenticação Flask-Login.
  │   │   ├── models.py - Outros modelos de dados da aplicação, se aplicável.
  │   │   ├── models_clients.py - Modelos específicos de clientes, se aplicável.
  │   │   ├── db.py - Configurações do banco de dados.
  │   │   ├── clients.py - Lógica relacionada a clientes, se aplicável.
  │   │   ├── __init__.py - Arquivo vazio para indicar que este diretório é um pacote Python.
  │   │   └── __pycache__/ - Cache de bytecode Python.
  │   ├── __pycache__/ - Cache de bytecode Python para os arquivos do pacote "app".
  │
  ├── data/ - Diretório para armazenar dados ou recursos da aplicação.
  │
  ├── src/ - Diretório para código-fonte externo ou bibliotecas adicionais, se aplicável.
  │
  ├── static/ - Contém arquivos estáticos, como CSS, JavaScript e imagens.
  │   ├── css/ - Arquivos CSS para estilização.
  │   │   ├── style.css - Arquivo CSS principal.
  │   │   ├── main.css - Estilos gerais da aplicação.
  │   │   ├── header.css - Estilos do cabeçalho.
  │   │   ├── footer.css - Estilos do rodapé.
  │   │   └── (outros arquivos CSS, se aplicável).
  │   ├── js/ - Arquivos JavaScript para funcionalidades interativas.
  │   │   ├── user.js - JavaScript relacionado aos usuários.
  │   │   ├── script.js - Outros scripts JavaScript.
  │   │   └── (outros arquivos JavaScript, se aplicável).
  │   ├── img/ - Imagens e recursos gráficos.
  │   │   ├── (arquivos de imagens diversos).
  │
  ├── templates/ - Contém os arquivos HTML que compõem as páginas da aplicação.
  │   ├── (arquivos HTML para cada página da aplicação).
  │
  ├── .gitattributes - Arquivo Git para configuração de atributos.
  ├── app.py - Arquivo principal da aplicação Flask.
  ├── database.py - Configurações e funções relacionadas ao banco de dados.
  ├── models.py - Definição de modelos de dados da aplicação (se não estiver em "app/models/").
  ├── Procfile - Arquivo usado para implantação no Heroku (se aplicável).
  ├── README.md - Documentação do projeto (este arquivo).
  └── requirements.txt - Lista de dependências da aplicação para instalação.

## Configuração e Instalação

Para configurar e executar o projeto, siga estas etapas:

1. **Configuração do Ambiente Virtual:**
   * Recomenda-se criar um ambiente virtual para o projeto.
   * Execute `python -m venv venv` para criar um ambiente virtual.
   * Ative o ambiente virtual com `source venv/bin/activate` (Linux/macOS) ou `venv\Scripts\activate` (Windows).
2. **Instalação de Dependências:**
   * Instale as dependências necessárias com `pip install -r requirements.txt`.
3. **Execução do Aplicativo:**
   * Navegue até o diretório raiz do projeto.
   * Execute `python -m guiadealter.app` para iniciar o servidor de desenvolvimento.
   * Acesse o aplicativo através do navegador em `http://localhost:5000`.

## Funcionalidades

O Guia de Alter é um aplicativo web Flask abrangente que oferece uma variedade de funcionalidades para atender às necessidades dos usuários. Abaixo estão algumas das principais funcionalidades do projeto:

### Autenticação de Usuários:

* **Login e Logout de Usuários:** Os usuários podem fazer login e fazer logout de suas contas com segurança.
* **Registro de Conta:** Os usuários podem se registrar criando uma nova conta com informações pessoais.
* **Proteção de Rotas:** Rotas específicas são protegidas e exigem autenticação para acesso.
* **Painel de Administração:** Os administradores têm acesso a um painel de administração para gerenciar usuários e conteúdo.

### Gerenciamento de Conteúdo:

* **Visualização de Conteúdo Dinâmico e Estático:** Os usuários podem visualizar informações estáticas, como páginas de destino e informações de contato, bem como conteúdo dinâmico, como passeios e pacotes.
* **Explorar Passeios:** Os usuários podem explorar uma variedade de passeios turísticos disponíveis, incluindo descrições detalhadas e informações sobre destinos.
* **Reservas de Passeios:** Os usuários podem fazer reservas para passeios específicos e ver informações relevantes sobre disponibilidade e preços.
* **Páginas de Destaque:** Destaques de passeios e pacotes são exibidos para destacar as principais ofertas.
* **Depoimentos:** Os usuários podem ver depoimentos de outros clientes para obter feedback sobre as experiências.
* **Contato e Suporte:** Os usuários podem entrar em contato com a equipe de suporte através do formulário de contato.
* **Políticas e Termos:** Informações legais, como políticas de privacidade e termos de uso, estão disponíveis para consulta.
* **Página "Sobre Nós":** Os usuários podem aprender mais sobre a empresa e sua equipe.
* **Informações de Parceiros:** Informações sobre como se tornar um parceiro estão disponíveis.

### Estilo Visual Atraente:

* **Design Responsivo:** O aplicativo possui um design responsivo para se adaptar a dispositivos móveis e desktops.
* **CSS Personalizado:** O aplicativo utiliza arquivos CSS personalizados para estilização.
* **Imagens Atraentes:** Imagens de alta qualidade são usadas para aprimorar a experiência do usuário.

### Estrutura Modular:

* **Blueprints:** As rotas são organizadas em blueprints para facilitar a modularização e manutenção do código.
* **Organização de Arquivos:** Os arquivos são estruturados de forma organizada em diretórios para facilitar a localização e manutenção.

### Implantação Fácil:

* **Preparado para Heroku:** O projeto inclui um arquivo Procfile e uma lista de dependências no requirements.txt para facilitar a implantação no Heroku ou em outras plataformas de hospedagem.

O Guia de Alter oferece uma ampla gama de funcionalidades para atender às necessidades dos usuários que desejam explorar Alter do Chão e suas atrações turísticas.

### Gerenciamento de Conteúdo

* Visualização e interação com conteúdo dinâmico e estático.
* Páginas informativas sobre a região de Alter do Chão.
* Páginas de reservas, pacotes turísticos, buffets, hotéis e passeios.

### Informações Turísticas

* Informações detalhadas sobre diferentes passeios turísticos na região.
* Páginas dedicadas a destinos específicos, como Lago Verde, Alter do Chão e outros.

## Rotas Principais

### Rotas definidas em `routes.py`

* `/`: Página Inicial
* `/login`: Página de Login
* `/register`: Página de Registro
* `/reservas`: Página de Reservas
* `/pacotes`: Página de Pacotes Turísticos
* `/buffets`: Página de Buffets
* `/hotels`: Página de Hotéis
* `/passeios`: Página de Passeios
* `/contato`: Página de Contato
* `/veiculos`: Página de Veículos
* `/sobrenos`: Página "Sobre Nós"
* `/explorealter`: Página "Explore Alter"
* `/mapaalter`: Página "Mapa de Alter"
* `/pessoascompraram`: Página "Pessoas Compraram"
* `/conhecaalter`: Página "Conheça Alter"
* `/souvenir`: Página "Souvenir"
* `/sejanossoparceiro`: Página "Seja Nosso Parceiro"
* `/logout`: Página de Logout
* `/admin`: Página de Administração
* `/rioarapiuns`: Página "Rio Arapiuns"
* `/lagoverde`: Página "Lago Verde"
* `/descendoorio`: Página "Descendo o Rio"
* `/subindoorio`: Página "Subindo o Rio"
* `/tourdestaques`: Página de Destaques do Tour

### Rotas definidas em `routes_tours.py`

* `/tours`: Página de Tours
* `/tours/lagoverde`: Página do Tour "Lago Verde"
* `/tours/alterdochao`: Página do Tour "Alter do Chão"
* `/tours/florestaencantada`: Página do Tour "Floresta Encantada"
* `/tours/igarapedocamarao`: Página do Tour "Igarapé do Camarão"
* `/tours/igarapedomacaco`: Página do Tour "Igarapé do Macaco"
* `/tours/pontadavaleria`: Página do Tour "Ponta da Valéria"
* `/tours/subindoorio/pindobal`: Página do Tour "Pindobal"
* `/tours/subindoorio/mureta`: Página do Tour "Mureta"
* `/tours/subindoorio/jurucui`: Página do Tour "Jurucuí"
* `/tours/subindoorio/cajutuba`: Página do Tour "Cajutuba"
* `/tours/subindoorio/aramanai`: Página do Tour "Aramanai"
* `/tours/rioarapiuns/torono`: Página do Tour "Toronó"
* `/tours/rioarapiuns/pontagrande`: Página do Tour "Ponta Grande"
* `/tours/rioarapiuns/melipolinario`: Página do Tour "Melipolinário"
* `/tours/rioarapiuns/icuxi`: Página do Tour "Icuxi"
* `/tours/rioarapiuns/comunidadecoroca`: Página do Tour "Comunidade Coroca"
* `/tours/descendoorio/pontadocururu`: Página do Tour "Ponta do Cururu"
* `/tours/descendoorio/pontadepedras`: Página do Tour "Ponta de Pedras"
* `/tours/descendoorio/pedradamoca`: Página do Tour "Pedra da Moca"
* `/tours/descendoorio/lagopreto`: Página do Tour "Lago Preto"
* `/tours/descendoorio/lagodojacare`: Página do Tour "Lago do Jacaré"
* `/tours/descendoorio/encontrodasaguas`: Página do Tour "Encontro das Águas"
* `/tours/descendoorio/casadosaulo`: Página do Tour "Casa do Saulo"
* `/tours/descendoorio/canaldojari`: Página do Tour "Canal do Jari"

### Rotas de Depoimentos

* `/depoimentos`: Página de Depoimentos

## Contribuição

Contribuições para o projeto são bem-vindas. Para contribuir, por favor, siga as práticas padrão de desenvolvimento de software e faça pull requests para revisão.

## Licença

Este projeto está licenciado sob a [MIT License]().
