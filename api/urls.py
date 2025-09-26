from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PerfilViewSet, CursoViewSet, DisciplinaViewSet

router = DefaultRouter()
router.register(r'perfis', PerfilViewSet)
router.register(r'cursos', CursoViewSet)
router.register(r'disciplinas', DisciplinaViewSet)


urlpatterns = [
   path('', include(router.urls)),
]