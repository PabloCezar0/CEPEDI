Este projeto é uma aplicação web de gerenciamento de biblioteca desenvolvida com Django e Django REST Framework.  Foi desenvolvido para uma ativdade de residência da CEPEDI pelos residentes Pablo Cezar Moreira Carvalho e Klaus Almeida Souza Santos.


Instalação:

1. Clone o repositório:
git clone https://github.com/KlausAlmeida1/biblioteca-django-v2

2. Entre na pasta:
cd biblioteca-django-v2

3. Crie  o ambiente virtual Python:
python -m venv venv

4. Ative o ambiente virtual:
venv\Scripts\activate

5. Instale as depedências:
pip install -r requirements.txt

6. Entre na pasta do projeto:
cd AtividadeMoodle2
   
7. Faça as migrações:
python manage.py migrate

8. Popule o banco de dados:
python manage.py populate_db

9. Inicie a aplicação:
python manage.py runserver



