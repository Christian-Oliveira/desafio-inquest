from django.test import TestCase
from django.urls import reverse
from rest_framework import status
import json

from ..models import PeopleModel

# Create your tests here.

URL_PEOPLE_LIST = "people:people-list"

class TestUniqueCreatePerson(TestCase):
    """
    Esta classe testa a criação de uma pessoa com mesmo CPF ou CNPJ ou E-mail
    """
    def setUp(self):
        PeopleModel.objects.create(
            people_type="F",
            name="Jose Silva",
            cpf="15326136418",
            email="jose@hotmail.com"
        )
        PeopleModel.objects.create(
            people_type="J",
            name="Inquest",
            cnpj="1234567891234",
            email="inquest@gmail.com"
        )

        self.invalid_data_cpf = {
            "people_type": "F",
            "name": "Joãozinho",
            "cpf": "15326136418",
            "email": "joaozinho@gmail.com"
        }

        self.invalid_data_cnpj = {
            "people_type": "J",
            "name": "Umbrella",
            "cnpj": "1234567891234",
            "email": "umbrella@gmail.com"
        }

        self.invalid_data_email = {
            "people_type": "J",
            "name": "Inquest Enterprise",
            "cnpj": "9876541478523",
            "email": "inquest@gmail.com"
        }

        self.invalid_email = {
            "people_type": "J",
            "name": "Organização ZXY",
            "cnpj": "1582478521598",
            "email": "org_zxy.gmail.com"
        }

        self.invalid_data_people_type = {
            "people_type": "X",
            "name": "Empresa BBC",
            "cnpj": "7896541235555",
            "email": "empresa.bbc@gmail.com"
        }

    # Testar a criação de uma pessoa com o mesmo CPF
    def test_create_repeated_cpf(self):
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.invalid_data_cpf),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testar a criação de uma pessoa com o mesmo CNPJ
    def test_create_repeated_cnpj(self):
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.invalid_data_cnpj),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testar a criação de uma pessoa com o mesmo E-mail
    def test_create_repeated_email(self):
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.invalid_data_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testa a criação de uma pessoa com email invalido
    def test_invalid_email(self):
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.invalid_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Testa a criação de uma pessoa de tipo errado, ou seja, que não é Fisica, nem Juridica
    def test_invalid_people_type(self):
        response = self.client.post(
            reverse(URL_PEOPLE_LIST),
            data=json.dumps(self.invalid_data_people_type),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)