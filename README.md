# Desafio Inquest   [![Build Status](https://travis-ci.org/Christian-Oliveira/desafio-inquest.svg?branch=master)](https://travis-ci.org/Christian-Oliveira/desafio-inquest)

## OBJETIVO 📝
Criar uma API Rest para as seguintes funções:
* Registro de pessoas, a partir do CPF;

* Registro de empresas e donos da empresa(podendo ser pessoas físicas e ou jurídicas, ou seja uma empresa que tem como dono uma outra empresa);

* Registro de bens e posses de um indivíduo.

## GERAR SECRET_KEY (Se Necessário) 🔒
1. Comando para gerar secret_key django.
    ~~~python
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
    ~~~

## COMO EXECUTAR 🔥
1. Para rodar é necessario ter o Docker e o docker-compose instalados.
2. Faça uma copia do arquivo _.env.exemple_ na raiz do projeto ou renomei o arquivo para _.env_
    > ex: .env.example --> .env
3. Após isso basta executar o comando na raiz do projeto.
    > `docker-compose up -d`
4. e os containeres serão criados e executados.
5. Assim que a aplicação estiver rodando, para executar comandos no container da aplicação.
6. execute comandos assim:
- 6.1. para criar as tabelas no banco de dados.
    > `docker-compose exec web python manage.py migrate`
- 6.2. assim que as tabelas forem migradas.
- 6.3. basta criar um superusuario com.
    > `docker-compose exec web python manage.py createsuperuser`
7. entrar com os dados e pronto, basta acessar o link.
    * <http://localhost:8000>

## EXECUTAR TESTES ✅
1. Para executar os testes basta dar o sequinte comando:
    > `docker-compose exec web python manage.py test`

## ROTAS DA API 🔀

### PEOPLE
* GET `/people`
* GET `/people/<int:id>`
* PUT `/people/<int:id>`
* DELETE `/people/<int:id>`
* POST `/people`
~~~json
{
    "people_type": "[F, J]",
    "name": "string",
    "cpf": "string",
    "cnpj": "string",
    "email": "string",
    "owners": ["people_id"],
    "assets": [
        {
            "assets_type": "[INT, MOV, IMO]",
            "code": "number",
            "description": "string",
            "acquisition_form": "[COM, DOA, HER]",
            "localization": "string",
            "acquisition_value": "number"
        }
    ]
}
~~~

### ASSETS
* GET `/assets`
* GET `/assets/<int:id>`
* PUT `/assets/<int:id>`
* DELETE `/assets/<int:id>`
* POST `/assets`
~~~json
{
    "person": "string",
    "assets_type": "[INT, MOV, IMO]",
    "code": "number",
    "description": "string",
    "acquisition_form": "[COM, DOA, HER]",
    "localization": "string",
    "acquisition_value": "number"
}
~~~