from rest_framework import serializers

from .models import AssetsModel

class AssetsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetsModel
        fields = '__all__'