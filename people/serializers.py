from rest_framework import serializers

from .models import PeopleModel

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleModel
        fields = [
            'id',
            'people_type',
            'name',
            'cpf',
            'cnpj',
            'email',
            'created_at',
            'updated_at',
            'active',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'active',
        ]