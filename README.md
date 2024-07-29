# msx-test-api

## Description

API RESTful para gerenciamento de veículos.

## Features

### Usuários
- [x] Criação de usuários - /api/users/register
- [x] Autenticação de usuários - /api/users/login

### Veículos
- [x] Criação de veículos - /api/vehicles
- [x] Listagem de veículos - /api/vehicles
- [x] Busca de veículos por ID - /api/vehicles/{id}
- [x] Atualização de veículos - /api/vehicles/{id}
- [x] Exclusão de veículos - /api/vehicles/{id}


## Tecnologias

- [x] Python3
- [x] Flask
- [x] sqlite3

## Estrutura do projeto

```
msx-test-api
├── src
│   ├── controllers
│   │   ├── __init__.py
│   │   ├── authcontroller.py
│   │   └── vehiclescontroller.py
│   ├── docs
│   │   ├── __init__.py
│   │   └── templates
│   │       └── __init__.py
│   │       └── swagger.html
│   ├── extensions
│   │   ├── __init__.py
│   │   └── flask_jwt.py
│   │   └── flask_marshmallow.py
│   │   └── flask_sqlalchemy.py
│   ├── models
│   │   ├── __init__.py
│   │   └── usersmodel.py
│   │   └── vehiclesmodel.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── swaggersroutes.py
│   │   └── usersroutes.py
│   │   └── vehiclesroutes.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── userschemas.py
│   │   └── vehiclesschemas.py
│   ├── __init__.py
│   ├── app.py
│   ├── settings.py
├── tests
│   ├── __init__.py
│   ├── test_routes.py
├── .env
├── main.py
├── requirements.txt
├── README.md
```

## Setup

1. Clone o repositório:
```bash
git clone https://github.com/danbsilva/msx-test-api.git
cd msx-test-api
```

2. Crie as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo e altere os valores das variáveis para os valores desejados:
```conf
FLASK_DEBUG=1
FLASK_ENV=development
FLASK_APP=main:server
APP_NAME=vehicles
APP_HOST=0.0.0.0
APP_PORT=52000

SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_DATABASE_URI=sqlite:///db_vehicles.db


TIMEZONE=America/Sao_Paulo


# KEYS
SECRET_KEY=SUA_CHAVE_SECRETA
```

3. Crie um ambiente virtual:
```bash
python -m venv venv
```

4. Ative o ambiente virtual:
```bash
source venv/bin/activate
```

5. Instale as dependências:
```bash
pip install -r requirements.txt
```

6. Execute o servidor:
```bash
python main.py
```

## Documentação

1. Acesse a documentação da API em:
```url
http://localhost:52000/api/docs
```

## Testes

1. Execute os testes:
```bash
python -m unittest discover -s tests
```
