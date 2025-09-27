import uuid
from django.db import models
from django.db.models import Sum
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError

class Perfil(AbstractUser):
    TIPOS = [
        ('Gerente', 'Gerente'),
        ('Professor', 'Professor'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False 
    )
    codigo = models.CharField(max_length=30 ,unique=True, blank=True)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(choices=TIPOS)
    
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    ativo = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        Group,
        related_name="perfil_groups",
        blank=True,
        help_text="Grupos do usuário",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="perfil_user_permissions",
        blank=True,
        help_text="Permissões do usuário",
        verbose_name="user permissions",
    )

    def save(self, *args, **kwargs):
        if self.email:
            self.username = self.email
            
        if not self.codigo:
            ano = now().year
            codigos = Perfil.objects.filter(codigo__startswith=f"MAT.{ano}.").values_list('codigo', flat=True)
            
            numeros = []
            for cod in codigos:
                try:
                    numeros.append(int(cod.split('.')[-1]))
                except:
                    pass
            
            numero = 1 if not numeros else max(numeros) + 1
            self.codigo = f"MAT.{ano}.{numero}"
        
        super().save(*args, **kwargs)

                
class Curso(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    sigla = models.CharField(max_length=4, help_text="ADS, MED, VET")
    codigo = models.CharField(max_length=30 ,unique=True, blank=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    carga_horaria_total = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.codigo:
            ano = now().year
            self.codigo = f"{self.sigla}{ano}"
        
        super().save(*args, **kwargs)

class Disciplina(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    sigla = models.CharField(max_length=5, help_text="BD, IA, RD")
    codigo = models.CharField(max_length=30 ,unique=True, blank=True)
    nome = models.CharField(max_length=80)
    carga_horaria = models.IntegerField()
    curso = models.ForeignKey("Curso", on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)

    def clean(self):
        if not self.curso.ativo:
            raise ValidationError("Não é possível adicionar uma disciplina a um curso inativo.")
        
        disciplinas_existentes_no_curso = Disciplina.objects.filter(curso=self.curso)
        if self.pk:
            disciplinas_existentes_no_curso = disciplinas_existentes_no_curso.exclude(pk=self.pk)

        carga_horaria_total_atual =  disciplinas_existentes_no_curso.aggregate(total=Sum('carga_horaria'))['total'] or 0
        carga_horaria_total_atual += self.carga_horaria
        
        if carga_horaria_total_atual > self.curso.carga_horaria_total:
            raise ValidationError(f"A soma das cargas horárias das disciplinas é {carga_horaria_total_atual} e ultrapassam a carga horária total do curso que é de {self.curso.carga_horaria_total}.")

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.codigo:
            ultimo_codigo = Disciplina.objects.filter(
                curso=self.curso,
                sigla=self.sigla
            ).order_by("id").last()
            
            numero = 1
            if ultimo_codigo:
                numero = int(ultimo_codigo.codigo.split('.')[-1]) + 1
            
            self.codigo = f"{self.curso.sigla}-{self.sigla}.{numero:03}"
        
        super().save(*args, **kwargs)