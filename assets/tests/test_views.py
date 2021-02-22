from django.test import TestCase
from django.urls import reverse
from rest_framework import status
import json

from people.models import PeopleModel
from ..models import AssetsModel
from ..serializers import AssetsSerializer

# Create your tests here.

URL_ASSETS_LIST = "assets:assets-list"
URL_ASSET_DETAIL = "assets:asset-detail"

ASSETS_TYPE = AssetsModel.AssetsType
ACQUISITION_FORM = AssetsModel.AcquisitionForm

class TestGetAssets(TestCase):
    """
    Esta classe testa a lista de varios Ativos e a visualização de um unico Ativo
    """
    def setUp(self):
        self.person1 = PeopleModel.objects.create(
            people_type='F', name='Christian Oliveira', cpf='36589614758', email='christian@gmail.com'
        )
        self.person2 = PeopleModel.objects.create(
            people_type='F', name='Maria Sousa', cpf='05089974521', email='maria@gmail.com'
        )

        self.asset1 = AssetsModel.objects.create(
            person=self.person1,
            assets_type=ASSETS_TYPE.INT,
            code=444,
            description="Ação na Bolsa de Valores",
            acquisition_form=ACQUISITION_FORM.HER,
        )

        self.asset2 = AssetsModel.objects.create(
            person=self.person1,
            assets_type=ASSETS_TYPE.MOV,
            code=222,
            description="Carro de Luxo",
            acquisition_form=ACQUISITION_FORM.COM,
            localization="Rio de Janeiro-RJ"
        )

        self.asset3 = AssetsModel.objects.create(
            person=self.person2,
            assets_type=ASSETS_TYPE.INT,
            code=777,
            description="Ações Imobiliarias",
            acquisition_form=ACQUISITION_FORM.COM,
        )

    ## Testa a busca por todos os Ativos
    def test_get_all_assets(self):
        response = self.client.get(reverse(URL_ASSETS_LIST))
        assets = AssetsModel.objects.all()
        serializer = AssetsSerializer(assets, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    ## Testa a busca por todos os Ativos de uma Pessoa pelo ID
    def test_get_all_assets_to_person_id(self):
        response = self.client.get(
            reverse(URL_ASSETS_LIST)+"?person_id="+str(self.person1.pk))
        assets = AssetsModel.objects.filter(person=self.person1.pk)
        serializer = AssetsSerializer(assets, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestPostSingleAsset(TestCase):
    """
    Esta classe testa a criação de um Ativo
    """
    def setUp(self):
        self.person = PeopleModel.objects.create(
            people_type='F', name='Christian Oliveira', cpf='03083236298', email='christian@gmail.com'
        )

        self.valid_data_asset = {
            "person": self.person.pk,
            "assets_type": ASSETS_TYPE.IMO,
            "code": 123,
            "description": "Apartamento de Vista ao Mar",
            "acquisition_form": ACQUISITION_FORM.DOA,
            "localization": "Brasil-Maranhão-São Luís"
        }

        self.invalid_data_asset = {
            "assets_type": ASSETS_TYPE.IMO,
            "code": "",
            "description": "Apartamento de Vista ao Mar",
            "acquisition_form": ACQUISITION_FORM.DOA,
            "localization": "Brasil-Maranhão-São Luís"
        }
    
    ## Testa cadastro de ativos com dados corretos
    def test_create_valid_asset(self):
        response = self.client.post(
            reverse(URL_ASSETS_LIST),
            data=json.dumps(self.valid_data_asset),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    ## Testa cadastro de ativos com dados incorretos
    def test_create_invalid_asset(self):
        response = self.client.post(
            reverse(URL_ASSETS_LIST),
            data=json.dumps(self.invalid_data_asset),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestPutSingleAsset(TestCase):
    """
    Esta classe testa a atualização de um unico Ativo
    """
    def setUp(self):
        self.person = PeopleModel.objects.create(
            people_type='F', name='Christian Oliveira', cpf='03083236298', email='christian@gmail.com'
        )

        self.asset = AssetsModel.objects.create(
            person=self.person,
            assets_type=ASSETS_TYPE.INT,
            code=444,
            description="Ação na Bolsa de Valores",
            acquisition_form=ACQUISITION_FORM.HER,
        )

        self.valid_asset = {
            "code": 466,
            "localization": "Site do Ibovesta"
        }

        self.invalid_asset = {
            "description": ""
        }

    def test_valid_update_asset(self):
        response = self.client.put(
            reverse(URL_ASSET_DETAIL, kwargs={'pk': self.asset.pk}),
            data=json.dumps(self.valid_asset),
            content_type='application/json'
        )
        self.assertEqual(response.data['code'], self.valid_asset['code'])
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_asset(self):
        response = self.client.put(
            reverse(URL_ASSET_DETAIL, kwargs={'pk': self.asset.pk}),
            data=json.dumps(self.invalid_asset),
            content_type='application/json'
        )
        self.assertNotEqual(response.data['description'], self.invalid_asset['description'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestDeleteSingleAsset(TestCase):
    """
    Esta classe testa a exclusão de um unico Ativo
    """
    def setUp(self):
        self.person = PeopleModel.objects.create(
            people_type='F', name='Christian Oliveira', cpf='03083236298', email='christian@gmail.com'
        )

        self.asset = AssetsModel.objects.create(
            person=self.person,
            assets_type=ASSETS_TYPE.INT,
            code=777,
            description="Ações da Infotech Brasil",
            acquisition_form=ACQUISITION_FORM.COM,
            localization="Sede na Avenida Paulista em São Paulo-SP/BR"
        )

    def test_valid_delete_asset(self):
        response = self.client.delete(
            reverse(URL_ASSET_DETAIL, kwargs={'pk': self.asset.pk})
        )
        asset = AssetsModel.objects.filter(pk=self.asset.pk)
        self.assertEqual(len(asset), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_asset(self):
        response = self.client.delete(
            reverse(URL_ASSET_DETAIL, kwargs={'pk': 99})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)