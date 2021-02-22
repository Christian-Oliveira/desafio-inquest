from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import AssetsModel
from .serializers import AssetsSerializer

# Create your views here.

class AssetsList(APIView):
    """
    Recurso para listar e criar Ativos
    """
    def get(self, request):
        person_id = request.GET.get('person_id', None)

        if (person_id is not None):
            assets = AssetsModel.objects.filter(person=person_id)
        else:
            assets = AssetsModel.objects.all()

        serializer = AssetsSerializer(assets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AssetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssetDetail(APIView):
    """
    Recurso para buscar, atualizar e deletar um Ativo
    """
    def get(self, request, pk):
        person = get_object_or_404(AssetsModel, pk=pk)
        serializer = AssetsSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        asset = get_object_or_404(AssetsModel, pk=pk)
        serializer = AssetsSerializer(asset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        asset = get_object_or_404(AssetsModel, pk=pk)
        asset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
