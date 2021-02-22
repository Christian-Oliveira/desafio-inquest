from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import PeopleModel
from .serializers import PeopleSerializer, PeopleCreateSerializer

# Create your views here.

class PeopleList(APIView):
    """
    Recurso para listar e criar Pessoas (Fisicas ou Juridicas)
    """
    def get(self, request):
        people = PeopleModel.objects.all()
        serializer = PeopleSerializer(people, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PeopleCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PeopleDetail(APIView):
    """
    Recurso para buscar, atualizar e deletar uma Pessoa (Fisicas ou Juridicas)
    """
    def get(self, request, pk):
        person = get_object_or_404(PeopleModel, pk=pk)
        serializer = PeopleSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        person = get_object_or_404(PeopleModel, pk=pk)
        serializer = PeopleCreateSerializer(person, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        person = get_object_or_404(PeopleModel, pk=pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)