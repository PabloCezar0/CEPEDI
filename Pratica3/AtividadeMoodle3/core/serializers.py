from rest_framework import serializers
from .models import Livro, Autor, Categoria, Colecao

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nome']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']

class LivroSerializer(serializers.ModelSerializer):
    autor = AutorSerializer(read_only=True)  
    categoria = CategoriaSerializer(read_only=True) 
    autor_id = serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all(), source='autor', write_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), source='categoria', write_only=True)

    class Meta:
        model = Livro
        fields = ['id', 'titulo', 'autor', 'autor_id', 'categoria', 'categoria_id', 'publicado_em']


class ColecaoSerializer(serializers.ModelSerializer):
    colecionador = serializers.ReadOnlyField(source='colecionador.username')  
    class Meta:
        model = Colecao
        fields = '__all__'  
 
