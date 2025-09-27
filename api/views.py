from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Perfil, Curso, Disciplina
from .serializers import PerfilSerializer, CursoSerializer, DisciplinaSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated

class IsGerente(BasePermission):
    message = "Acesso negado: é necessário ser Gerente."

    def has_permission(self, request, view):
        user = request.user

        print(getattr(user, 'tipo'))
        return bool(user and user.is_authenticated and getattr(user, 'tipo', '').lower() == 'gerente')


class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ativo', 'codigo']
    search_fields = ['nome', 'email']

    @action(detail=True, methods=['patch'])
    def inativar(self, request, pk=None):
        perfil = self.get_object()
        perfil.ativo = False
        perfil.save()
        return Response({'status': 'O perfil foi inativado'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'])
    def ativar(self, request, pk=None):
        perfil = self.get_object()
        perfil.ativo = True
        perfil.save()
        return Response({'status': 'O perfil foi ativado'}, status=status.HTTP_200_OK)

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['ativo', 'codigo']
    search_fields = ['nome', 'sigla']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'ativar', 'inativar']:
            return [IsGerente()]

        return [IsAuthenticated()]
    
    @action(detail=True, methods=['patch'])
    def inativar(self, request, pk=None):
        curso = self.get_object()
        curso.ativo = False
        curso.save()
        return Response({'status': 'O curso foi inativado'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'])
    def ativar(self, request, pk=None):
        curso = self.get_object()
        curso.ativo = True
        curso.save()
        return Response({'status': 'O curso foi ativado'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def resumo(self, request, pk=None):
        curso = self.get_object()
        disciplinas_ativas = curso.disciplina_set.filter(ativo=True)
        total_disciplinas = disciplinas_ativas.count()
        soma_carga_horaria = disciplinas_ativas.aggregate(total=Sum('carga_horaria'))['total'] or 0
        return Response(
                {
                    'total_disciplinas_ativas': f'{total_disciplinas}', 
                    'soma_carga_horaria_ativa': f'{soma_carga_horaria}'
                },
                status=status.HTTP_200_OK
            )

class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['curso', 'ativo']
    search_fields = ['nome','sigla']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'ativar', 'inativar']:
            return [IsGerente()]

        return [IsAuthenticated()]
    
    @action(detail=True, methods=['patch'])
    def inativar(self, request, pk=None):
        disciplina = self.get_object()
        disciplina.ativo = False
        disciplina.save()
        return Response({'status': 'A disciplina foi inativada'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['patch'])
    def ativar(self, request, pk=None):
        disciplina = self.get_object()
        disciplina.ativo = True
        disciplina.save()
        return Response({'status': 'A disciplina foi ativada'}, status=status.HTTP_200_OK)
