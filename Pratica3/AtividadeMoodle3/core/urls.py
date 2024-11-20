from django.urls import path
from .views import LivroList, LivroDetail, AutorList, AutorDetail, CategoriaList, CategoriaDetail, ColecaoListCreate, ColecaoDetail  

urlpatterns = [


    path('livros/', LivroList.as_view(), name='livros-list'),
    path('livros/<int:pk>/', LivroDetail.as_view(), name='livro-detail'),


    path('autores/', AutorList.as_view(), name='autores-list'),
    path('autores/<int:pk>/', AutorDetail.as_view(), name='autor-detail'),


    path('categorias/', CategoriaList.as_view(), name='categorias-list'),
    path('categorias/<int:pk>/', CategoriaDetail.as_view(), name='categoria-detail'),

    path('colecoes/', ColecaoListCreate.as_view(), name='colecoes-list-create'),
    path('colecoes/<int:pk>/', ColecaoDetail.as_view(), name='colecao-detail'),
]
