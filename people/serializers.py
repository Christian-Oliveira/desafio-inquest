from rest_framework import serializers

from assets.models import AssetsModel
from .models import PeopleModel

class PeopleSerializer(serializers.ModelSerializer):
    owners = serializers.StringRelatedField(many=True)
    assets = serializers.StringRelatedField(many=True)

    class Meta:
        model = PeopleModel
        fields = [
            'id',
            'people_type',
            'name',
            'cpf',
            'cnpj',
            'email',
            'owners',
            'assets',
            'created_at',
            'updated_at',
            'active',
        ]
        read_only_fields = [
            'id', 
            'owners',
            'assets',
            'created_at', 
            'updated_at', 
            'active'
        ]

class PeopleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleModel
        fields = [
            'people_type',
            'name',
            'cpf',
            'cnpj',
            'email',
            'owners',
        ]

    def create(self, validated_data):
        if 'people_type' in validated_data:
            if validated_data.get('people_type') == PeopleModel.PeopleType.FISICA:
                if not(validated_data.get('cpf')):
                    raise serializers.ValidationError({
                        'cpf': 'Este campo é obrigatório.'
                    })
                else:
                    if validated_data.get('owners'):
                        raise serializers.ValidationError({
                            'owners': 'Pessoas não podem ser donas de Pessoa Física.'
                        })
            elif validated_data.get('people_type') == PeopleModel.PeopleType.JURIDICA:
                if not(validated_data.get('cnpj')):
                    raise serializers.ValidationError({
                        'cnpj': 'Este campo é obrigatório.'
                    })
        return PeopleModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if (validated_data.get('people_type') == PeopleModel.PeopleType.FISICA):
            if not(validated_data.get('cpf')):
                raise serializers.ValidationError({
                    'cpf': 'Este campo é obrigatório.'
                })
        elif (validated_data.get('people_type') == PeopleModel.PeopleType.JURIDICA):
            if not(validated_data.get('cnpj')):
                raise serializers.ValidationError({
                    'cnpj': 'Este campo é obrigatório.'
                })
        elif (instance.people_type == PeopleModel.PeopleType.FISICA):
            if validated_data.get('owners'):
                raise serializers.ValidationError({
                    'owners': 'Pessoa Física não pode ter donos.'
                })
        elif (validated_data.get('owners')):
            owners = validated_data.pop('owners')
            instance.owners.set(owners)
        for field_data in validated_data:
            setattr(instance, field_data, validated_data.get(field_data))
        instance.save()
        return instance
    