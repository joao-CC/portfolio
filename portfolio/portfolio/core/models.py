from django.db import models
from django.conf import settings


class BancoPessoal(models.Model):
    # Vincula o perfil ao usuario do Django (1 usuario -> 1 perfil)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil',
        null=True,
        blank=True,
    )

    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    curso = models.CharField(max_length=100)
    periodo = models.IntegerField(default=0)
    email = models.CharField(blank=True, max_length=100)
    github = models.CharField(blank=True, max_length=50)
    linkedin = models.CharField(blank=True,max_length=50)
    url_imagem = models.URLField(blank=True,max_length=200)

    def __str__(self):
        return self.nome

# Create your models here.
