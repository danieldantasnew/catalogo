from rest_framework import serializers
from .models import Perfil, Curso, Disciplina

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = [ 'id' , 'codigo', 'nome', 'tipo', 'email' , 'ativo']

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id','sigla','codigo','nome','descricao','ativo', 'carga_horaria_total']

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = ['id','sigla','codigo','nome', 'ativo', 'curso', 'carga_horaria']
        depth = 1