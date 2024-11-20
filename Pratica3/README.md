Este projeto é uma aplicação web de gerenciamento de biblioteca desenvolvida com Django e Django REST Framework.  Foi desenvolvido para uma ativdade de residência da CEPEDI pelos residentes Pablo Cezar Moreira Carvalho e Klaus Almeida Souza Santos.


Instalação e utilização:

1. Clone o repositório:
git clone https://github.com/PabloCezar0/CEPEDI/

2. Entre na pasta:
cd Pratica3

3. Crie  o ambiente virtual Python:
python -m venv venv

4. Ative o ambiente virtual:
venv\Scripts\activate

5. Entra na pasta:
cd AtividadeMoodle3
   
6. Instale as depedências:
pip install -r requirements.txt
  
7. Faça as migrações:
python manage.py migrate

8. Popule o banco de dados:
python manage.py populate_db

9. Crie um superusuário (admin):
python manage.py createsuperuser

10. Inicie a aplicação:
python manage.py runserver

11. Acesse a pagina de admin e entre com seu admin:
http://127.0.0.1:8000/admin/

12. Crie usuários para poder acessar a página de coleções.

13. Acesse a página de coleções e entre com seu usuario criado:
http://127.0.0.1:8000/api/colecoes/ 

