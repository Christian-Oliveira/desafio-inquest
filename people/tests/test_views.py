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
            people_type='F', name='Christian Oliveira', cpf='12358877798', email='christian@gmail.com'
        )

        self.valid_data_person_cpf = {
            "people_type": "F",
            "name": "Jose Silva",
            "cpf": "15326136418",
            "email": "jose@hotmail.com"
        }

        self.valid_data_person_cnpj = {
            "people_type": "J",
            "name": "Empresa ABC",
            "cnpj": "15987425896312",
            "email": "empresa.abc@hotmail.com",
            "owners": [self.person.pk]
        }

    # Testa o cadastro de uma Pessoa Fisica com dados validos 
    def test_create_valid_person_cpf(self):
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.valid_data_person_cpf),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testa o cadastro de uma Pessoa Fisica com dados invalidos
    def test_create_invalid_person_cpf(self):
        self.valid_data_person_cpf.update({'cpf': ''})
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.valid_data_person_cpf),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testa o cadastro de uma Pessoa Juridica com dados validos 
    def test_create_valid_person_cnpj(self):
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.valid_data_person_cnpj),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Testa o cadastro de uma Pessoa Juridica com dados invalidos
    def test_create_invalid_person_cnpj(self):
        self.valid_data_person_cnpj.update({'cnpj': ''})
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.valid_data_person_cnpj),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testa o cadastro de uma Pessoa Fisica com CPF menor que o padrão 11
    def test_min_length_cpf(self):
        self.valid_data_person_cpf.update({'cpf': '15326'})
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.valid_data_person_cpf),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testa o cadastro de uma Pessoa Fisica com CPF maior que o padrão 11
    def test_max_length_cpf(self):
        self.valid_data_person_cpf.update({'cpf': '15326136418000'})
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.valid_data_person_cpf),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testa o cadastro de uma Pessoa Juridica com CNPJ menor que o padrão 14
    def test_min_length_cnpj(self):
        self.valid_data_person_cnpj.update({'cnpj': '159'})
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.valid_data_person_cnpj),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # Testa o cadastro de uma Pessoa Juridica com CNPJ maior que o padrão 14
    def test_max_length_cnpj(self):
        self.valid_data_person_cnpj.update({'cnpj': '15987425896312555'})
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.valid_data_person_cnpj),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testa o NÂO cadastro de pessoas fisica com donos (proprietarios)
    def test_not_owners_in_person_cpf(self):
        self.valid_data_person_cpf.update({"owners": [self.person.pk]})
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.valid_data_person_cpf),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testa a criação de uma pessoa com seus Ativos
    def test_create_person_with_assets(self):
        self.valid_data_person_cnpj.update({'assets': [
            {
                "assets_type": "IMO",
                "code": 123,
                "description": "Apartamento de Vista ao Mar",
                "acquisition_form": "DOA",
                "localization": "Brasil-Maranhão-São Luís"
            },
            {
                "assets_type": "MOV",
                "code": 43,
                "description": "Jato particular",
                "acquisition_form": "HER",
                "localization": "Brasil-Maranhão-São Luís"
            }
        ]})
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=self.valid_data_person_cnpj,
            content_type='application/json'
        )
        self.assertNotEqual(len(response.data['assets']), 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
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
            "cnpj": "99876543214321",
            "email": "teste2@hotmail.com"
        }

        self.invalid_data = {
            "people_type": "J",
            "name": "",
            "cnpj": "99876543214321",
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
            reverse(URL_PERSON_DETAIL, kwargs={'pk': self.person2.pk})
        )
        person2 = PeopleModel.objects.filter(pk=self.person2.pk)
        self.assertEqual(len(person2), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_person(self):
        response = self.client.delete(
            reverse(URL_PERSON_DETAIL, kwargs={'pk': 404}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
