from django.db import models


class Certificado(models.Model):
    descricao = models.CharField(max_length=200)

    def __str__(self):
        return self.descricao


class Projeto(models.Model):
    TIPO_CHOICES = [
        ('Pessoal', 'Pessoal'),
        ('Disciplina', 'Disciplina'),
    ]
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    nome = models.CharField(max_length=50)
    descricao = models.TextField()
    link_github = models.URLField(blank=True, max_length=200)

    def __str__(self):
        return self.nome
