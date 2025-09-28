from rest_framework import serializers
from .models import Perfil, Curso, Disciplina

class PerfilSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Perfil
        fields = ['id', 'codigo', 'nome', 'tipo', 'email', 'ativo', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Perfil(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id','sigla','codigo','nome','descricao','ativo', 'carga_horaria_total']

class DisciplinaSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True)
    curso_id = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(), write_only=True, source='curso'
    )

    class Meta:
        model = Disciplina
        fields = ['id','sigla','codigo','nome','ativo','curso','curso_id','carga_horaria']