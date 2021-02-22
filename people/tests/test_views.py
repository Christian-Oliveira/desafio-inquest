from django.test import TestCase
from django.urls import reverse
from rest_framework import status
import json

from ..models import PeopleModel
from ..serializers import PeopleSerializer

# Create your tests here.

URL_PEOPLE_LIST = "people:people-list"
URL_PERSON_DETAIL = "people:person-detail"

class TestGetPeople(TestCase):
    """
    Esta classe testa a lista de varias pessoas e a visualização de uma unica pessoa
    """
    def setUp(self):
        self.person1 = PeopleModel.objects.create(
            people_type='F', name='Christian Oliveira', cpf='03083236298', email='christian@gmail.com'
        )
        self.person2 = PeopleModel.objects.create(
            people_type='J', name='Inquest', cnpj='1234567891234', email='inquest@gmail.com'
        )
        self.person3 = PeopleModel.objects.create(
            people_type="J", name="Microsoft Brasil", cnpj="14785236978952", email="microsoft@outlook.com"
        )

    ## Testar listar todas as pessoas.
    def test_get_all_people(self):
        response = self.client.get(reverse(URL_PEOPLE_LIST))
        people = PeopleModel.objects.all()
        serializer = PeopleSerializer(people, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    ## Testar pegar uma pessoa valida.
    def test_get_valid_person(self):
        response = self.client.get(
            reverse(URL_PERSON_DETAIL, kwargs={'pk': self.person1.pk}))
        person = PeopleModel.objects.get(pk=self.person1.pk)
        serializer = PeopleSerializer(person)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Testar pegar uma pessoa invalida.
    def test_get_invalid_person(self):
        response = self.client.get(
            reverse(URL_PERSON_DETAIL, kwargs={'pk': 404}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TestPostSinglePerson(TestCase):
    """
    Esta classe testa a criação de uma unica pessoa
    """
    def setUp(self):
        self.person = PeopleModel.objects.create(
            people_type='F', name='Christian Oliveira', cpf='03083236298', email='christian@gmail.com'
        )

        self.valid_data = {
            "people_type": "F",
            "name": "Jose Silva",
            "cpf": "15326136418",
            "email": "jose@hotmail.com"
        }

        self.invalid_data = {
            "people_type": "F",
            "name": "Jose Silva",
            "cpf": "15326136418",
            "email": ""
        }

    def test_create_valid_person(self):
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_person(self):
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testa o NÂO cadastro de pessoas fisica com donos (proprietarios)
    def test_not_owners_in_person_cpf(self):
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.valid_data.update({"owners": [self.person.pk]})),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestPutSinglePerson(TestCase):
    """
    Esta classe testa a atualização de uma unica pessoa
    """

    def setUp(self):
        self.person = PeopleModel.objects.create(
            people_type='J', name='Empresa Test', cnpj='9876543214321', email='teste@hotmail.com'
        )
        self.valid_data = {
            "people_type": "J",
            "name": "Empresa Test 2",
            "cnpj": "9876543214321",
            "email": "teste2@hotmail.com"
        }

        self.invalid_data = {
            "people_type": "J",
            "name": "",
            "cnpj": "9876543214321",
            "email": "teste@hotmail.com"
        }

    def test_valid_update_person(self):
        response = self.client.put(
            reverse(URL_PERSON_DETAIL, kwargs={'pk': self.person.pk}),
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        self.assertEqual(response.data['name'], self.valid_data['name'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_person(self):
        response = self.client.put(
            reverse(URL_PERSON_DETAIL, kwargs={'pk': self.person.pk}),
            data=json.dumps(self.invalid_data),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDeleteSinglePerson(TestCase):
    """
    Esta classe testa a exclusão de uma unica pessoa
    """
    def setUp(self):
        self.person1 = PeopleModel.objects.create(
            people_type="J", name="Google Brasil", cnpj="15935725896314", email="google@gmail.com"
        )
        self.person2 = PeopleModel.objects.create(
            people_type="J", name="Microsoft Brasil", cnpj="14785236978952", email="microsoft@outlook.com"
        )

    def test_valid_delete_person(self):
        response = self.client.delete(
            reverse(URL_PERSON_DETAIL, kwargs={'pk': self.person2.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_person(self):
        response = self.client.delete(
            reverse(URL_PERSON_DETAIL, kwargs={'pk': 404}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
