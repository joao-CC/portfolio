from django.shortcuts import render
from core.models import BancoPessoal
from .models import Certificado, Projeto


def home(request):
    perfil = BancoPessoal.objects.first()
    certificados = Certificado.objects.all()
    contexto = {
        'perfil': perfil,
        'certificados': certificados,
    }
    return render(request, 'portfolio/home.html', contexto)


def projetos(request):
    lista_projetos = Projeto.objects.all()
    contexto = {
        'projetos': lista_projetos,
    }
    return render(request, 'portfolio/projetos.html', contexto)


def contato(request):
    perfil = BancoPessoal.objects.first()
    contexto = {
        'perfil': perfil,
    }
    return render(request, 'portfolio/contato.html', contexto)
