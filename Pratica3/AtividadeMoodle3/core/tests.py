from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Colecao, Livro, Categoria, Autor  


class ColecaoTests(APITestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

        self.categoria = Categoria.objects.create(nome="Categoria 1")
        self.autor = Autor.objects.create(nome="Autor 1")

        self.livro1 = Livro.objects.create(
            titulo="Livro 1", autor=self.autor, categoria=self.categoria, publicado_em="2023-01-01"
        )
        self.livro2 = Livro.objects.create(
            titulo="Livro 2", autor=self.autor, categoria=self.categoria, publicado_em="2023-01-01"
        )

        self.colecoes_url = "/api/colecoes/"

    def test_create_collection_auth(self):

        self.client.login(username="user1", password="password1")
        data = {
            "nome": "Minha Coleção",
            "descricao": "Descrição da coleção",
            "livros": [self.livro1.id, self.livro2.id],
        }
        response = self.client.post(self.colecoes_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["colecionador"], "user1")
        self.assertEqual(response.data["nome"], "Minha Coleção")

    def test_create_collection(self):
     
        data = {
            "nome": "Coleção Pública",
            "descricao": "Tentativa de criação sem autenticação",
            "livros": [self.livro1.id]
        }
        response = self.client.post(self.colecoes_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_user_collection(self):
  
        self.client.login(username="user1", password="password1")
        colecao = Colecao.objects.create(nome="Minha Coleção", descricao="Descrição", colecionador=self.user1)
        
        self.client.login(username="user2", password="password2")
        data = {"nome": "Nova Coleção"}
        url = f"{self.colecoes_url}{colecao.id}/"
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="user1", password="password1")
        data = {"nome": "Coleção Editada"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome"], "Coleção Editada")

    def test_delete_user_collection(self):

        self.client.login(username="user1", password="password1")
        colecao = Colecao.objects.create(nome="Minha Coleção", descricao="Descrição", colecionador=self.user1)
        
        self.client.login(username="user2", password="password2")
        url = f"{self.colecoes_url}{colecao.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="user1", password="password1")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Colecao.objects.filter(id=colecao.id).exists())

    def test_list_collections_auth(self):
        Colecao.objects.create(nome="Coleção 1", descricao="Descrição 1", colecionador=self.user1)
        Colecao.objects.create(nome="Coleção 2", descricao="Descrição 2", colecionador=self.user2)

        self.client.login(username="user1", password="password1")
        response = self.client.get(self.colecoes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)  # Deve incluir coleções de outros usuários

        response_data = response.data["results"]
        self.assertEqual(response_data[0]["nome"], "Coleção 1")
        self.assertEqual(response_data[1]["nome"], "Coleção 2")

    def test_list_collections(self):
 
        response = self.client.get(self.colecoes_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_collection_invalid_data(self):
        self.client.login(username="user1", password="password1")

        data = {"descricao": "Sem nome", "livros": [self.livro1.id]}
        response = self.client.post(self.colecoes_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"nome": "Coleção Inválida", "descricao": "Livro inexistente", "livros": [9999]}
        response = self.client.post(self.colecoes_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"nome": "Coleção Inválida", "descricao": "Sem livros", "livros": []}
        response = self.client.post(self.colecoes_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_database_persistence(self):
        self.client.login(username="user1", password="password1")
        data = {"nome": "Coleção Persistida", "descricao": "Teste", "livros": [self.livro1.id]}
        self.client.post(self.colecoes_url, data)

        colecao = Colecao.objects.get(nome="Coleção Persistida")
        self.assertEqual(colecao.descricao, "Teste")
        self.assertEqual(colecao.colecionador, self.user1)
        self.assertIn(self.livro1, colecao.livros.all())

    def test_user_can_access_other_collections(self):
        colecao = Colecao.objects.create(nome="Coleção Pública", descricao="Teste", colecionador=self.user2)

        self.client.login(username="user1", password="password1")
        url = f"{self.colecoes_url}{colecao.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome"], "Coleção Pública")
        self.assertEqual(response.data["colecionador"], "user2")

    def test_view_other_user_collection(self):
        colecao = Colecao.objects.create(nome="Coleção Pública", descricao="Visível", colecionador=self.user2)

        self.client.login(username="user1", password="password1")
        url = f"{self.colecoes_url}{colecao.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nome"], "Coleção Pública")
        self.assertEqual(response.data["descricao"], "Visível")
        self.assertEqual(response.data["colecionador"], "user2")

    def test_edit_other_user_collection_forbidden(self):
        colecao = Colecao.objects.create(nome="Coleção Pública", descricao="Visível", colecionador=self.user2)

        self.client.login(username="user1", password="password1")
        url = f"{self.colecoes_url}{colecao.id}/"
        data = {"nome": "Tentativa de Edição"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_other_user_collection_forbidden(self):
        colecao = Colecao.objects.create(nome="Coleção Pública", descricao="Visível", colecionador=self.user2)

        self.client.login(username="user1", password="password1")
        url = f"{self.colecoes_url}{colecao.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_model_str_methods(self):
        colecao = Colecao.objects.create(nome="Minha Coleção", descricao="Teste", colecionador=self.user1)
        self.assertEqual(str(colecao), "Minha Coleção - user1")

    def test_urls_resolve(self):
        from django.urls import reverse, resolve
        resolver = resolve(reverse("livros-list"))
        self.assertEqual(resolver.view_name, "livros-list")

    def test_autor_str(self):
        autor = Autor.objects.create(nome="Autor Teste")
        self.assertEqual(str(autor), "Autor Teste")

    def test_categoria_str(self):
        categoria = Categoria.objects.create(nome="Categoria Teste")
        self.assertEqual(str(categoria), "Categoria Teste")

    def test_colecao_str(self):
        colecao = Colecao.objects.create(
            nome="Minha Coleção",
            descricao="Descrição Teste",
            colecionador=self.user1
        )
        self.assertEqual(str(colecao), "Minha Coleção - user1")

    def test_livro_str(self):
        livro = Livro.objects.create(
            titulo="Livro Teste",
            autor=self.autor,
            categoria=self.categoria,
            publicado_em="2023-01-01"
        )
        self.assertEqual(str(livro), "Livro Teste")
