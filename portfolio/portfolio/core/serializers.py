from rest_framework import serializers
from .models import BancoPessoal


class BancoPessoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BancoPessoal
        fields = [
            'id', 'nome', 'descricao', 'curso',
            'periodo', 'email', 'github', 'linkedin', 'url_imagem',
        ]
        # 'usuario' nao aparece nos fields: quem esta logado define o perfil
        # automaticamente (via request.user), o cliente nao escolhe isso.
