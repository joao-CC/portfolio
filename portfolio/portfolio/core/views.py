from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import BancoPessoal
from .serializers import BancoPessoalSerializer


class PerfilDetail(generics.RetrieveUpdateAPIView):
    """
    GET   /api/perfil/ -> Retorna o perfil do usuario logado
    PUT   /api/perfil/ -> Atualiza o perfil completo
    PATCH /api/perfil/ -> Atualiza parcialmente
    """

    serializer_class = BancoPessoalSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Em vez de buscar pelo pk da URL, busca pelo usuario logado.
        Se o perfil ainda nao existir, cria um vazio automaticamente.
        """
        perfil, created = BancoPessoal.objects.get_or_create(
            usuario=self.request.user,
            defaults={'nome': self.request.user.username},
        )
        return perfil
