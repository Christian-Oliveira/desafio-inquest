# Desafio Inquest [![Build Status](https://travis-ci.org/Christian-Oliveira/desafio-inquest.svg?branch=master)](https://travis-ci.org/Christian-Oliveira/desafio-inquest)

## Objetivo
Criar uma API Rest para as seguintes funções:
- Registro de pessoas, a partir do CPF;

- Registro de empresas e donos da empresa(podendo ser pessoas físicas e ou jurídicas, ou seja uma empresa que tem como dono uma outra empresa);

- Registro de bens e posses de um indivíduo.

## GERAR SECRET_KEY (Se Necessário)
1. Comando para gerar secret_key django
    ```python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'```
## COMO RODAR
1. Para rodar é necessario ter o Docker e o docker-compose instalados
2. Após isso basta executar o comando
    ```docker-compose up --build```
3. e os containeres serão criados e executados.
4. Assim que a aplicação estiver rodando, para executar comandos no container da aplicação
5. execute comandos assim
6. para criar as tabelas no banco de dados
    ```docker-compose exec web python manage.py migrate```
7. assim que as tabelas forem migradas
8. basta criar um superusuario com
    ```docker-compose exec web python manage.py createsuperuser```
9. entrar com os dados e pronto.